from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    API_V1_STR: str = "/api/v1"
    # change this in production!
    SECRET_KEY = "replace-with-your-secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_SECRET_KEY = "replace-with-your-refresh-secret-key"
    REFRESH_TOKEN_EXPIRE_DAYS = 7

settings = Settings()
