from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any, List
from langchain_openai.chat_models.base import BaseChatOpenAI
import logging

__all__ = (
    'BaseOpenAIEmbeddings',
    'BaseOpenAIConversation'
)

TModel = TypeVar('TModel')
TModelChat = TypeVar('TModelChat', bound=BaseChatOpenAI)

class BaseOpenAIEmbeddings(
    ABC, Generic[TModel]
):
    def __init__(self, model: TModel) -> None:
        self.model = model

    @abstractmethod
    def embedding(self, text: str) -> list[float]:
        """Convert texts to embeddings"""
        ...
    
    def batch_embedding(self, texts: list[str]) -> list[list[float]]:
        """Convert texts to embeddings for batches"""
        return [
            self.embedding(t) 
            for t in texts
        ]

class BaseOpenAIConversation(
    ABC, Generic[TModelChat]
):
    def __init__(self, model: TModelChat) -> None:
        self.model = model

    def chat(self, message):
        """"""
        logging.info(
            f"Requested a chat message for invoke(): {message}"
        )
        return self.model.invoke(message)
    
    async def async_chat(self, message):
        """"""
        logging.info(
            f"Requested a chat message for invoke(): {message}"
        )
        result = await self.model.ainvoke(message)
        return result

    