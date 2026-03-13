import os
import faiss
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore

from app.graph.prompts import context_prompt
from app.llm.llm_model import llm
from app.config import gemini_api_key, embedding_model
from logs import setup_logger

logger = setup_logger()


def generate_context_for_doc():
    
    DATA_DIR = Path("app/data")

    docs = []
    for file in DATA_DIR.glob("*.pdf"):
        loader = PyPDFLoader(str(file))
        docs.extend(loader.load())
    
    # Combine all document text
    documents_text = "\n\n".join([doc.page_content for doc in docs])

    response = llm.invoke(
        context_prompt.format_messages(
            documents=documents_text
        )
    )

    # Save output
    output_file = DATA_DIR / "context.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(response.content)

    return response.content


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

    generate_context_for_doc()

    return vector_store

