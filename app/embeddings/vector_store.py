import os
import faiss
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore

from app.config import gemini_api_key, embedding_model
from logs import setup_logger

logger = setup_logger()


def create_embeddings():

    index_path = "faiss_index"

    embeddings = GoogleGenerativeAIEmbeddings(
        model=embedding_model,
        api_key=gemini_api_key
    )

    # If index exists → load
    if os.path.exists(index_path):
        logger.info("Loading existing FAISS index...")
        return FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True
        )

    # Else → create empty index safely
    logger.info("Creating new FAISS index...")

    embedding_dim = len(embeddings.embed_query("dummy text"))
    index = faiss.IndexFlatL2(embedding_dim)

    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore({}),
        index_to_docstore_id={}
    )

    vector_store.save_local(index_path)

    return vector_store

