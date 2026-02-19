import faiss
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from ..config import gemini_api_key
import os

def create_embeddings():

    index_path = "faiss_index"

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        api_key=gemini_api_key
    )

    # If index exists → load
    if os.path.exists(index_path):
        print("Loading existing FAISS index...")
        return FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True
        )

    # Else → create empty index safely
    print("Creating new FAISS index...")

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

