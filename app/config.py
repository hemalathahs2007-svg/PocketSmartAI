import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "PocketSmart AI")
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pocketsmart.db")
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "5"))
