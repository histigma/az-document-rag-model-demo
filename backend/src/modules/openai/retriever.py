from langchain_weaviate import WeaviateVectorStore
from weaviate import WeaviateClient

from modules.db.driver import LocalWeaviateDB
from modules.openai import DataVectorizer

from typing import TYPE_CHECKING, Union, Literal, TypedDict, overload
from typing_extensions import Unpack
if TYPE_CHECKING:
    from langchain_core.documents import Document
    from modules.db.driver import DatabaseBackendShape
    from langchain_core.vectorstores.base import VectorStoreRetriever

import logging

__all__ = (
    'VectorstoreRetriever',
)

TSearch = Literal['mmr', 'similarity']

class SimilarityParams(TypedDict, total=False):
    top_k: int
    score_threshold: float

class MMRParams(TypedDict, total=False):
    top_k: int
    # score_threshold: float
    lambda_mult: float
    fetch_k: int


class VectorstoreRetriever:
    def __init__(
            self, 
            database_client: "Union[DatabaseBackendShape[WeaviateClient], DatabaseBackendShape]",
            vectorizer: DataVectorizer
    ) -> None:
        """
        **Supported: 'Weaviate DB'**

        :database_client: Set a database backend using in this class.  
        :vectorizer: Data vectorizer instance.
        """
        self._db_client = database_client
        self._vectorizer = vectorizer

    def _get_store(
            self,
            collection,
            key
    ):
        client = self._db_client.conn
        if isinstance(client, WeaviateClient):
            vector_store = WeaviateVectorStore(
                client,
                collection,
                key,
                self._vectorizer.embedding_model
            )
        else:
            raise NotImplementedError(
                f"Current database client is not supported yet: {type(client)}"
            )
        return vector_store

    def __build_similarity_retrieve_param(
            self,
            top_k: int=3,
            score_threshold: float=0.5,
    ):
        return {
            "search_type": 'similarity',
            "search_kwargs": {"k": top_k, "score_threshold": score_threshold}
        }
    
    def __build_mmr_retrieve_param(
            self,
            top_k: int=3,
            # score_threshold: float=0.5,
            lambda_mult: float=0.5,
            fetch_k: int=20,
    ):
        return {
            "search_type": 'mmr',
            "search_kwargs": {"k": top_k, "lambda_mult": lambda_mult, "fetch_k": fetch_k, } #"score_threshold": score_threshold}
        }

    @overload
    def get_retriever(
        self,
        search_type: Literal["similarity"],
        index: str,
        text_key: str = "text",
        **kwargs: Unpack[SimilarityParams]
    ) -> "VectorStoreRetriever": ...

    @overload
    def get_retriever(
        self,
        search_type: Literal["mmr"],
        index: str,
        text_key: str = "text",
        **kwargs: Unpack[MMRParams]
    ) -> "VectorStoreRetriever": ...

    def get_retriever(
            self,
            search_type: TSearch,
            index: str, 
            text_key: str='text',
            **kwargs
    ):
        """Get a retriever for vector searching.
        """
        if search_type == 'mmr':
            search_fn = self.__build_mmr_retrieve_param
        elif search_type == 'similarity':
            search_fn = self.__build_similarity_retrieve_param
        else:
            raise ValueError(f"Invalid search type: {search_type}")

        store = self._get_store(index, text_key)
        if isinstance(store, WeaviateVectorStore):
            return store.as_retriever(
                **search_fn(**kwargs)
            )
        raise NotImplementedError(f"Unsupported store: {type(store)}")

