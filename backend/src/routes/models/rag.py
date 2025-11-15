from typing import Optional, Literal
from pydantic import BaseModel


TRagCategory = Literal['document']

class ChatRequest(BaseModel):
    question: str
    
class RagQueryRequest(BaseModel):
    question: str
    k: int = 5
    category: Optional[TRagCategory] = None

