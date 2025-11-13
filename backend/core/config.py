from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import logging
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
  #jwt
  ALGORITHM: str = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 7*24*60
  SECRET_KEY : str = os.getenv("secret_key", "your-secret-key-change-in-production")
  MONGO_URI : str = os.getenv("mongo_uri", "mongodb://localhost:27017")
  DATABASE_NAME: str = os.getenv("database_name", "eduneuro")
  
  
  model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
