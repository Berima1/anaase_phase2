# Anaasɛ Phase 2 Production-Ready Bundle

This repository is production-ready and defaults to using the Hugging Face Inference API (no OpenAI key required).

## LLM Options
- **Hugging Face Inference API** (recommended): set HUGGINGFACE_API_TOKEN and optionally HF_MODEL.
- **Local transformers**: set TRANSFORMERS_MODEL and install transformers & torch.
- **OpenAI**: if you prefer, set OPENAI_API_KEY and LLM_BACKEND=openai.

## Quickstart
1. Create venv and install deps:

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

2. Set HF token (recommended):

```bash
export HUGGINGFACE_API_TOKEN=your_token
export HF_MODEL=google/flan-t5-small
```

3. Start backend:

```bash
bash run.sh
```

4. Run UI locally:

```bash
cd ui
npm install
npm run dev
```

## Deploy
- Backend: Render/ Railway/ Fly.io. Use `bash run.sh` as start command.
- Frontend: Deploy `ui/` to Vercel (set Project Root = `ui`) and set NEXT_PUBLIC_BACKEND_URL.
