from langchain_weaviate import WeaviateVectorStore

from modules.db.driver import LocalWeaviateDB
from modules.openai import DataVectorizer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from langchain_core.documents import Document
    from modules.db.driver import DatabaseBackendShape

import logging

__all__ = (
    'TextChunkDataToVectorizeUploader',
)


class TextChunkDataToVectorizeUploader:
    """A utility class helps upload vectorized data to Database.
    
    """

    def __init__(
            self, 
            database_client: "DatabaseBackendShape",
            vectorizer: "DataVectorizer"
    ) -> None:
        """
        
        :database_client: Set a database backend using in this class.
        :vectorizer: Data vectorizer instance.
        """
        self._db_client = database_client
        self._vectorizer = vectorizer
    
    async def async_weaviate_upload(
            self, 
            chunks: "list[Document]",
            index: str, 
            text_key: str='text'
    ):
        """
        Upload chunks(documents) to Vector Database (weaviate).

        First, transforms text data to `list[Document]` by using `TextDataChunker`  
        then input data to `chunks` parameter.
        """
        if not isinstance(self._db_client, LocalWeaviateDB):
            raise RuntimeError(
                f"Expected {LocalWeaviateDB.__name__}, but got {type(self._db_client)}"
            )
        try:
            vector_store = await WeaviateVectorStore.afrom_documents(
                chunks,
                self._vectorizer.embedding_model,
                client=self._db_client.conn,
                index_name=index,
                text_key=text_key
            )
            logging.info(f"Uploading text data to database(index: {index}, text_key: {text_key}, count: {len(chunks)} docs) is completed: {vector_store}")
        except Exception as e:
            logging.error(e)
            return None
        return vector_store



