import os
from pathlib import Path
from dotenv import load_dotenv
from google.oauth2 import service_account

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]

gemini_model = os.getenv("GEMINI_MODEL")
embedding_model = os.getenv("EMBEDDING_MODEL")

gemini_api_key = os.getenv("GEMINI_API_KEY")
location = os.getenv("LOCATION")
credentials = service_account.Credentials.from_service_account_file(os.getenv("SERVICE_ACCOUNT_FILE"),scopes=["https://www.googleapis.com/auth/cloud-platform"])

tavily_api_key = os.getenv("TAVILY_API_KEY")