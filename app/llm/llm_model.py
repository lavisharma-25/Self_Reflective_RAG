from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import credentials, gemini_model, location

llm = ChatGoogleGenerativeAI(
    model=gemini_model,
    project=credentials.project_id,
    credentials=credentials,
    location=location,
    vertexai=True
)