from fastapi import Header, HTTPException
from typing import Optional
from settings import api_settings

__all__ = (
    'check_content_length',
)

def check_content_length(
        content_length: Optional[int] = Header(None)
    ):
    if content_length is not None and content_length > api_settings.MAX_CONTENT_LENGTH:
        raise HTTPException(
            status_code=413, 
            detail="File too large"
        )
    return content_length

