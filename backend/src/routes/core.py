from fastapi import Depends, APIRouter, HTTPException

from .models import ChatRequest
from modules.openai import (
    get_az_llm, 
    AzureOpenAIConversationAdapter,
)
from services.lang.conversation import GeneralPromptHandleClient

router = APIRouter()

@router.post("/chat/test")
def conversation(request: ChatRequest, llm=Depends(get_az_llm)):
    # Create a conversation client
    conversation = AzureOpenAIConversationAdapter(llm)
    prompt_handler = GeneralPromptHandleClient(
        conversation,
        "You are genius chat bot."
    )
    query = request.question
    answer = prompt_handler.chat_user_query(
        query
    )
    return {
        "message": answer.content if answer else 'null'
    }
