from typing import Type, Union, TYPE_CHECKING
from ..driver.abs import DatabaseBackendShape
from ..driver.weaviate_client import LocalWeaviateDB
from modules.openai.vectorize import DataVectorizer

from .models import WeaviateRepoQueryResult
from weaviate.classes.query import MetadataQuery

if TYPE_CHECKING:
    from weaviate.collections.classes.internal import QueryReturn, Object

__all__ = (
    'WeaviateVectorRepository',
)

class WeaviateVectorRepository:
    """Repository for accessing Weaviate-like database backends."""
    SUPPORT_CLASSES: tuple[Type[DatabaseBackendShape], ...] = (
        LocalWeaviateDB,
    )
    def __init__(
            self, 
            client: DatabaseBackendShape,
            vectorizer: DataVectorizer
    ):
        if not isinstance(client, self.SUPPORT_CLASSES):
            raise TypeError(
                f"Unsupported backend type: {type(client).__name__}. "
                f"Supported: {[cls.__name__ for cls in self.SUPPORT_CLASSES]}"
            )
        elif not isinstance(vectorizer, DataVectorizer):
            raise TypeError(f"Invalid vectorizer type: {type(vectorizer)}")
        self._client = client
        self._vectorizer = vectorizer

    def query(
            self, 
            database: str,
            query: Union[str, list[float]],
            top_k: int = 5,
            user_internal_vectorize_module: bool=False
    ) -> WeaviateRepoQueryResult:
        """Query for string or embedded data.
        (string --> vectorize --> query)

        ```python
        response = col.query.near_text(...)
        for o in response.objects:
            print(o.properties)
            print(o.metadata.distance)
        ```

        Args:
            database (str): Database name
            query (str): string query
            top_k (int, optional): Limit argument. Defaults to 5.
        """
        if isinstance(query, str):
            vectorized = self._vectorizer._embedder.embed_query(query)
        elif query and isinstance(query, list) and isinstance(query[0], float):
            vectorized = query
        else:
            raise ValueError(f"Unsupported query type: {type(query)}")
        session = self._client.conn.collections.use(
            database
        )
        q = {'near_vector': vectorized}
        query_fn = session.query.near_vector
        if user_internal_vectorize_module:
            q = {'query': vectorized}
            query_fn = session.query.near_text
        response: "QueryReturn" = query_fn(
            **q,
            limit=top_k,
            return_metadata=MetadataQuery(distance=True)
        )
        objects: "list[Object]" = response.objects
        return WeaviateRepoQueryResult(objects)
    
