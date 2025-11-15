from enum import Enum
from typing import Type, Union, TYPE_CHECKING

from modules.openai import VectorstoreRetriever, DataVectorizer
from modules.rag import ContextGenerator
from weaviate import WeaviateClient
if TYPE_CHECKING:
    from modules.db.driver import DatabaseBackendShape
    from langchain_core.documents import Document
from settings import RagPartition


__all__ = (
    'VectorstoreRetreivingService',
)

class VectorstoreRetreivingService:
    """Data Retreiving service.   
    """
    _SUPPORTS_DB_CLIENTS = (
        WeaviateClient, 
    )
    CONST_TEXT_KEY = 'text'
    # CONST_SCORE_THRESHOLD = 0.5
    CONST_LAMBDA_MULT = 0.5
    CONST_FETCH_K = 20

    def __init__(
        self, 
        db_client: "DatabaseBackendShape",
        vectorizer: "DataVectorizer"
    ) -> None:
        """
        Database Supports: `Weaviate Client`  
        """
        if isinstance(db_client.conn, self._SUPPORTS_DB_CLIENTS):
            self.__retriever = VectorstoreRetriever(
                db_client, vectorizer
            )
        else:
            raise NotImplementedError(
                f"Not supported: {type(db_client)}"
            )

    @property
    def retriever(self):
        return self.__retriever

    def retrieve(
        self,
        query: str,
        index: Union[RagPartition, str],
        top_k: int
    ):
        """Retrieve documents using VectorStoreRetriever...
        Args:
            query (str): Search text
            index (Union[RagPartition, str]): collection name
            top_k (int): select top k 

        Returns:
            list[Document]: documents list

            ```python
            from langchain_core.documents import Document

            document = Document(
                page_content="Hello, world!", metadata={"source": "https://example.com"}
            )
            ```
        """
        retriever = self.retriever.get_retriever(
            'mmr', 
            index=index.value if isinstance(index, Enum) else index,
            text_key=self.CONST_TEXT_KEY,
            top_k=top_k,
            lambda_mult=self.CONST_LAMBDA_MULT,
            fetch_k=self.CONST_FETCH_K
        )
        docs = retriever.invoke(query)
        return docs
    
    def retrieve_to_context(
        self,
        query: str,
        index: Union[RagPartition, str],
        top_k: int
    ):
        """Retrieve documents using VectorStoreRetriever...   
        and convert them to context (string)
        Args:
            query (str): Search text
            index (Union[RagPartition, str]): collection name
            top_k (int): select top k 

        Returns:
            str
        """
        
        docs = self.retrieve(query, index, top_k)
        context = ContextGenerator()
        return context.format_docs_with_metadata(docs)
