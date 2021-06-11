from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    api_token: str = Field(..., env="NOTION_API_KEY")
    database_id: str = Field(..., env="DATABASE_ID")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings(_env_file="./.env")
