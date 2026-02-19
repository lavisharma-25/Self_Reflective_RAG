from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from ..config import gemini_api_key
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class Create_Embedding():
    def __

def create_embeddings():
    global vector_store_instance
    docs = (
        PyPDFLoader("../data/Company_Policies.pdf").load()
        + PyPDFLoader("../data/Company_Profile.pdf").load()
        + PyPDFLoader("../data/Product_and_Pricing.pdf").load()
    )

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=600, chunk_overlap=150
        ).split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        api_key=gemini_api_key
        )

    
    return vector_store_instance

