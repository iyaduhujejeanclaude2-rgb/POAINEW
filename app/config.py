import os
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    database_url:str="postgresql+psycopg://poai:poai_change_me@db:5432/poai"
    api_key:str="change_this_long_random_key"
    telegram_bot_token:str=""
    telegram_chat_id:str=""
    upload_dir:str="/data/screenshots"
    max_upload_mb:int=8
    confidence_threshold:float=0.68
settings=Settings()
