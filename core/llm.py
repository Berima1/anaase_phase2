"""LLM Adapter (production-ready)
Priority order:
1. HUGGINGFACE_INFERENCE_API (set HUGGINGFACE_API_TOKEN and HF_MODEL)
2. Local transformers model (set TRANSFORMERS_MODEL and have transformers installed)
3. OpenAI (optional if OPENAI_API_KEY set and LLM_BACKEND=openai)
4. Stub fallback (safe)
"""
import os, requests, json

def llm_generate_hf_inference(prompt: str, model: str = None, timeout: int = 60) -> str:
    token = os.getenv('HUGGINGFACE_API_TOKEN')
    if not token:
        raise RuntimeError('HUGGINGFACE_API_TOKEN not set for HF Inference API')
    model = model or os.getenv('HF_MODEL', 'google/flan-t5-small')  # small by default
    url = f'https://api-inference.huggingface.co/models/{model}'
    headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
    payload = {'inputs': prompt, 'options': {'wait_for_model': True}}
    r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=timeout)
    r.raise_for_status()
    out = r.json()
    # HF inference can return text or generated_text depending on model
    if isinstance(out, dict):
        # try common keys
        return out.get('generated_text') or out.get('text') or json.dumps(out)
    if isinstance(out, list) and len(out)>0:
        first = out[0]
        if isinstance(first, dict):
            return first.get('generated_text') or first.get('summary_text') or json.dumps(first)
        return str(first)
    return str(out)

def llm_generate_transformers(prompt: str, model_name: str = None, max_length: int = 256) -> str:
    try:
        from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
    except Exception as e:
        raise RuntimeError('transformers not installed') from e
    model_name = model_name or os.getenv('TRANSFORMERS_MODEL', 'google/flan-t5-small')
    # choose seq2seq if contains 'flan' or 't5'; otherwise causal
    if 'flan' in model_name or 't5' in model_name or 'bart' in model_name:
        pipe = pipeline('text2text-generation', model=model_name, device=0 if (os.getenv('USE_CUDA','0')=='1') else -1)
    else:
        pipe = pipeline('text-generation', model=model_name, device=0 if (os.getenv('USE_CUDA','0')=='1') else -1)
    out = pipe(prompt, max_length=max_length, do_sample=False)
    if isinstance(out, list) and len(out)>0:
        if isinstance(out[0], dict):
            return out[0].get('generated_text') or out[0].get('text') or json.dumps(out[0])
        return str(out[0])
    return str(out)

def llm_generate_openai(prompt: str) -> str:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('OPENAI_API_KEY not set')
    import requests, json
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    payload = {'model':'gpt-4o-mini','messages':[{'role':'system','content':'You are Anaasɛ Portal Assistant'},{'role':'user','content':prompt}], 'max_tokens':512}
    r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
    r.raise_for_status()
    data = r.json()
    return data['choices'][0]['message']['content']

def llm_generate_stub(prompt: str) -> str:
    # safe deterministic fallback: concise synthesized answer using heuristics
    lines = prompt.split('\n')[:8]
    preview = ' '.join(lines)[:400]
    return '[ANAASƐ STUB] ' + preview + ' ... (provide HUGGINGFACE_API_TOKEN or local transformers for full answers)'

def llm_generate(prompt: str) -> str:
    backend = os.getenv('LLM_BACKEND','hf').lower()  # default to Hugging Face inference
    # preference order enforced by backend selection, but will try fallbacks
    if backend == 'openai' and os.getenv('OPENAI_API_KEY'):
        try:
            return llm_generate_openai(prompt)
        except Exception as e:
            print('OpenAI error:', e)
    if backend in ('hf','huggingface','hf_inference','huggingface_inference') or os.getenv('HUGGINGFACE_API_TOKEN'):
        try:
            return llm_generate_hf_inference(prompt)
        except Exception as e:
            print('HF inference error, falling back:', e)
    # try local transformers
    try:
        return llm_generate_transformers(prompt)
    except Exception as e:
        print('Local transformers error, falling back to stub:', e)
    return llm_generate_stub(prompt)
