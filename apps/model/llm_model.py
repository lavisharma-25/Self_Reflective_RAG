from langchain_google_genai import ChatGoogleGenerativeAI
import os
from ..config import gemini_api_key

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=gemini_api_key,
    temperature=0
)