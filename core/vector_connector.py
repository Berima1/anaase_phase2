import os

def index_documents_chroma(docs, collection_name='anaase'):
    try:
        import chromadb
        from chromadb.config import Settings
        client = chromadb.Client(Settings(chroma_db_impl='duckdb+parquet', persist_directory=os.getenv('CHROMA_PERSIST_DIR','./.chromadb')))
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embs = model.encode([d['text'] for d in docs]).tolist()
        except Exception:
            embs = None
        collection = client.get_or_create_collection(collection_name)
        ids = [d.get('id', str(i)) for i,d in enumerate(docs)]
        metadatas = [{'source': d.get('source','local')} for d in docs]
        if embs:
            collection.add(ids=ids, metadatas=metadatas, documents=[d['text'] for d in docs], embeddings=embs)
        else:
            collection.add(ids=ids, metadatas=metadatas, documents=[d['text'] for d in docs])
        client.persist()
        return True
    except Exception as e:
        print('Chroma indexing failed or not available:', e)
        return False


def index_documents_faiss(docs):
    try:
        from sentence_transformers import SentenceTransformer
        import faiss
        import numpy as np
        model = SentenceTransformer('all-MiniLM-L6-v2')
        texts = [d['text'] for d in docs]
        embs = model.encode(texts)
        embs = np.array(embs).astype('float32')
        d = embs.shape[1]
        index = faiss.IndexFlatIP(d)
        faiss.normalize_L2(embs)
        index.add(embs)
        faiss.write_index(index, 'faiss.index')
        import json
        with open('faiss_docs.json','w',encoding='utf-8') as f:
            json.dump(docs,f,ensure_ascii=False,indent=2)
        return True
    except Exception as e:
        print('FAISS indexing failed:', e)
        return False


def index_documents(docs):
    ok = index_documents_chroma(docs)
    if ok:
        return {'backend':'chroma','ok':True}
    ok2 = index_documents_faiss(docs)
    return {'backend':'faiss' if ok2 else 'none', 'ok': ok2}


def semantic_search(query, top_k=5, collection_name='anaase'):
    try:
        import chromadb
        from chromadb.config import Settings
        client = chromadb.Client(Settings(chroma_db_impl='duckdb+parquet', persist_directory=os.getenv('CHROMA_PERSIST_DIR','./.chromadb')))
        collection = client.get_collection(collection_name)
        res = collection.query(query_texts=[query], n_results=top_k)
        docs = res['documents'][0]
        return docs
    except Exception as e:
        print('Chroma query failed or not present:', e)
    try:
        import json
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import linear_kernel
        with open('faiss_docs.json','r',encoding='utf-8') as f:
            docs = json.load(f)
        texts = [d['text'] for d in docs]
        vec = TfidfVectorizer().fit_transform(texts + [query])
        cosine_similarities = linear_kernel(vec[-1], vec[:-1]).flatten()
        idx = cosine_similarities.argsort()[-top_k:][::-1]
        return [texts[i] for i in idx]
    except Exception as e:
        print('TF-IDF fallback failed:', e)
    return []
