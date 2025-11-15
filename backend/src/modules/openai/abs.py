from abc import ABC, abstractmethod
import logging
from typing import TYPE_CHECKING, TypeVar, Generic, Optional, Any, List

from langchain_openai.chat_models.base import BaseChatOpenAI
from langchain_openai.embeddings.base import OpenAIEmbeddings
from langchain_core.documents import Document
if TYPE_CHECKING:
    from modules.nlp import BaseDocParser


__all__ = (
    'BaseOpenAIEmbeddings',
    'BaseOpenAIConversation'
)

TEmbedModel = TypeVar('TEmbedModel', bound=OpenAIEmbeddings)
TModelChat = TypeVar('TModelChat', bound=BaseChatOpenAI)
TNaturalLanguage = TypeVar('TNaturalLanguage', list[str], list[Document])


class BaseOpenAIEmbeddings(
    ABC, Generic[TEmbedModel]
):
    def __init__(self, model: TEmbedModel) -> None:
        self.model = model

    def embed_query(self, text: str):
        return self.model.embed_query(text)

    def embed_documents(
            self, 
            docs: "TNaturalLanguage",
            content_parser_klass: "Optional[BaseDocParser]"=None
    ):
        parser_fn = lambda x: x
        if content_parser_klass:
            parser_fn = content_parser_klass

        texts = [
            parser_fn(doc) 
            for doc in docs
        ]
        return self.model.embed_documents(texts)

    # @abstractmethod
    # def embeded_query(self, text: str) -> list[float]:
    #     """Convert text to embeded query."""
    #     ...

    # @abstractmethod
    # def embed_documents(self, docs: TNaturalLanguage) -> list[list[float]]:
    #     ...


class BaseOpenAIConversation(
    ABC, Generic[TModelChat]
):
    def __init__(self, model: TModelChat) -> None:
        self.model = model

    def chat(self, message):
        """"""
        return self.model.invoke(message)
    
    async def async_chat(self, message):
        """"""
        result = await self.model.ainvoke(message)
        return result

    