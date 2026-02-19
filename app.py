from fastapi import FastAPI, HTTPException
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from apps.embeddings.vector_store import create_embeddings

app = FastAPI()

@app.post("/build-embeddings")
def build_embeddings():

    docs = (
        PyPDFLoader("apps/data/Company_Policies.pdf").load()
        + PyPDFLoader("apps/data/Company_Profile.pdf").load()
        + PyPDFLoader("apps/data/Product_and_Pricing.pdf").load()
    )

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=150
    ).split_documents(docs)

    vector_store = create_embeddings()
    vector_store.add_documents(chunks)
    vector_store.save_local("faiss_index")

    return {"message": "Embeddings built successfully"}


@app.post("/run")
def initiate_self_rag():
    "Todo"
    return