from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    API_V1_STR: str = "/api/v1"

settings = Settings()
