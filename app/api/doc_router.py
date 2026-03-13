from fastapi import APIRouter
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.embeddings.vector_store import create_embeddings

router = APIRouter(prefix="/document", tags=["Documents"])

@router.post("/load-documents")
async def load_documents():

    docs = (
        PyPDFLoader("app/data/Company_Policies.pdf").load()
        + PyPDFLoader("app/data/Company_Profile.pdf").load()
        + PyPDFLoader("app/data/Product_and_Pricing.pdf").load()
    )

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=150
    ).split_documents(docs)

    vector_store = create_embeddings()
    vector_store.add_documents(chunks)
    vector_store.save_local("faiss_index")

    return {"message": "Embeddings built successfully"}

