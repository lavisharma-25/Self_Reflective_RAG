import os
from google.oauth2 import service_account
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
gemini_model = os.getenv("GEMINI_MODEL")
gemini_api_key = os.getenv("GEMINI_API_KEY")
credentials = service_account.Credentials.from_service_account_file(os.getenv("SERVICE_ACCOUNT_FILE"),scopes=["https://www.googleapis.com/auth/cloud-platform"])
location = os.getenv("LOCATION")