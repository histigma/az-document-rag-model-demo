from fastapi import Header, Depends, APIRouter, HTTPException
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from typing import Optional
import logging 

from .models import RagQueryRequest, ChatRequest
from modules.rag.mime import check_content_length
from modules.openai import (
    get_az_llm, 
    get_az_embeddings,
    AzureOpenAIConversationAdapter,
    DataVectorizer,
    AzureOpenAIEmbeddingAdapter
)
from modules.db.driver import get_weaviate_db_client
from services.lang.conversation import GeneralPromptHandleClient
from services.lang.embeddings import TextChunkDataToVectorizeUploader
from modules.nlp.text_process import TextDataChunker
from settings import RagPartition


router = APIRouter()

@router.post("/chat")
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

@router.post("/vectorize/upload-text")
async def vectorize_txt(
    file: UploadFile = File(...),
    db_client=Depends(get_weaviate_db_client),
    embeddings=Depends(get_az_embeddings),
    _: Optional[int] = Depends(check_content_length)
):
    """Upload a text file (maxium size limit is to configurable) and 
    vectorize to weaviate database. 

    Args:
        file (UploadFile, optional): 
        _ (Optional[int], optional): 
    Raises:
        HTTPException: Invalid file type or not corrected encoding format.

    Returns:
        _type_: `JSONResponse`
    """
    rag_partition = RagPartition.DEFAULT

    # File type is must be 'text'
    if file.content_type not in (
        'text/plain', 'text/csv', 'application/octet-stream'
    ):
        raise HTTPException(400, 'Invalid file type. Expect text file.')
    
    # Read file and decoding to utf-8
    content_bytes = await file.read() 
    try:
        text = content_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(
            400, "Invalid file encoding. Expect 'UTF-8'"
        )
    
    # Load text and chunks 
    embedding_uploader = TextChunkDataToVectorizeUploader(
        db_client,
        DataVectorizer(
            AzureOpenAIEmbeddingAdapter(embeddings)
        )
    )
    # Get chunks from narrative text.
    documents = TextDataChunker().from_text(text)
    # (Async) Upload to database 
    wv_store = await embedding_uploader.async_weaviate_upload(
        documents, rag_partition
    )
    return JSONResponse(
        {
            "filename": file.filename, 
            "size": len(content_bytes), 
            "preview": text[ :200]
        }
    )

