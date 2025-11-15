from langchain_openai.embeddings.base import OpenAIEmbeddings
from modules.openai import BaseOpenAIEmbeddings

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from langchain_core.documents import Document


class DataVectorizer:
    """
    Makes vectorized data to store in Vector DB or 
    another No SQL (supports Vector Search) Database.
    
    """
    def __init__(
            self, 
            embedding_adapter: BaseOpenAIEmbeddings,
    ) -> None:
        self._embedder = embedding_adapter
        if not isinstance(embedding_adapter, BaseOpenAIEmbeddings):
            raise TypeError(
                f"Invalid embedding adapter: {type(embedding_adapter)}, expected {type(BaseOpenAIEmbeddings)}"
            )

    @property
    def embedding_model(self) -> "OpenAIEmbeddings":
        if not isinstance(self._embedder.model, OpenAIEmbeddings):
            raise TypeError(f"Invalid embedder model: {self._embedder.model}")
        return self._embedder.model

    def vectorize_documents(self, documents: list["Document"]):
        """Vectorizes text data such as list[list[float]]
        
        This vector data can be uploads to Vector DB.

        """
        return self._embedder.embed_documents(documents)
    