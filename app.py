from fastapi import FastAPI, HTTPException
from apps.embeddings.vector_store import create_embeddings
import apps.embeddings.vector_store as vector_store_module

app = FastAPI()

@app.post("/build-embeddings")
def build_embeddings():
    if vector_store_module.vector_store_instance is not None:
        return {"message": "Embeddings already created"}

    try:
        vector_store_module.vector_store_instance = vector_store_module.create_embeddings()
        return {"message": "Embeddings created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))