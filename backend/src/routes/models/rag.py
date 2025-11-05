from typing import Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    
class RagQueryRequest(BaseModel):
    question: str
    k: Optional[int] = 3

