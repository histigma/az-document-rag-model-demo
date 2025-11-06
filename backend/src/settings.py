from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from enum import Enum
from dotenv import load_dotenv

load_dotenv()   # For another libraries having more security conditions...


class RagPartition(str, Enum):
    DEFAULT = 'textDataPartition01'

class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',  # extra=forbid (default)
        frozen=True  
    )
    WEAVIATE_DB_HOST: str       = 'localhost'
    WEAVIATE_DB_PORT: int       = 8080
    WEAVIATE_DB_GRPC_PORT: int  = 50051

    OPENAI_ENDPOINT: Optional[str]      = None
    OPENAI_KEY: Optional[str]           = None
    OPENAI_API_VERSION: Optional[str]   = None
    OPENAI_GPT_MODEL: Optional[str]     = None
    OPENAI_EMBEDDINGS_DEPLOYMENT: Optional[str] = None

    LLM_TEMPERATURE: float = 0.3

    MAX_CONTENT_LENGTH: int = 5 * 1024 * 1024      # 5MB


api_settings = ApiSettings()

