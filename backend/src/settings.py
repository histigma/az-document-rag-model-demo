from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from dotenv import load_dotenv

load_dotenv()   # For another libraries having more security conditions...

class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',  # extra=forbid (default)
        frozen=True  
    )

    OPENAI_ENDPOINT: Optional[str]      = None
    OPENAI_KEY: Optional[str]           = None
    OPENAI_API_VERSION: Optional[str]   = None
    OPENAI_GPT_MODEL: Optional[str]     = None
    OPENAI_EMBEDDINGS_DEPLOYMENT: Optional[str] = None

    LLM_TEMPERATURE: float = 0.3


api_settings = ApiSettings()

