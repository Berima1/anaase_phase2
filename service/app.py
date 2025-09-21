from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.vector_connector import semantic_search
from core.llm import llm_generate

app = FastAPI(title='Anaasɛ Portal')

class Query(BaseModel):
    q: str
    lang: str = 'en'
    top_k: int = 5

@app.get('/health')
def health():
    return {'status':'ok'}

@app.post('/search')
def search(q: Query):
    try:
        hits = semantic_search(q.q, top_k=q.top_k)
        return {'query': q.q, 'hits': hits}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/ask')
def ask(q: Query):
    try:
        hits = semantic_search(q.q, top_k=4)
        context = '\n'.join(hits)
        prompt = f"Answer concisely and cite sources. Context:\n{context}\nQuestion:\n{q.q}"
        answer = llm_generate(prompt)
        return {'answer': answer, 'sources': hits}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
