from fastapi import Depends, APIRouter, HTTPException
from .models import RagQueryRequest, ChatRequest

from services.lang.conversation import GeneralPromptHandleClient
from modules.openai import get_az_llm, AzureOpenAIConversationAdapter


router = APIRouter()


@router.post("/chat")
def conversation(request: ChatRequest, llm=Depends(get_az_llm)):
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

