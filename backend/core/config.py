from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import logging
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


class Settings(BaseSettings):
  #jwt
  ALGORITHM: str = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 7*24*60
  SECRET_KEY : str = os.getenv("secret_key")
  #supabase connection
  url: str = os.getenv("project_url")
  anon_key: str = os.getenv("anon_key")
  service_role_key: str = os.getenv("service_role_key")
  
  
  model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


# Client for user operations (with anon key)
supabase: Client = create_client(settings.url, settings.anon_key)

# Client for admin operations (with service role key) - bypasses RLS
# If service role key is not provided, fall back to anon client
supabase_admin: Client = create_client(settings.url, settings.service_role_key) if settings.service_role_key else supabase