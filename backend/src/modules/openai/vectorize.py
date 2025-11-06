from modules.openai import BaseOpenAIEmbeddings
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .abs import OpenAIEmbeddings
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

    @property
    def embedding_model(self) -> "OpenAIEmbeddings":
        return self._embedder.model

    def vectorize_documents(self, documents: list["Document"]):
        """Vectorizes text data such as list[list[float]]
        
        This vector data can be uploads to Vector DB.

        """
        return self._embedder.embed_documents(documents)
    