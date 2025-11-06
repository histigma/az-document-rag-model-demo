"""
Connect to Weaviate Database.

But Cloud Weaviate is not supported yet in this module.

"""
from .abs import DatabaseBackendShape
from typing import Any, Optional, Callable
from contextlib import contextmanager

import weaviate as wv
import weaviate.classes as wvc
from weaviate.exceptions import WeaviateInvalidInputError

from settings import api_settings

__all__ =(
    'LocalWeaviateDB',
    'get_weaviate_db_client'
)

def get_weaviate_db_client():
    """
    Get instance of get_weaviate_db_client

    """
    
    if not hasattr(get_weaviate_db_client, "instance"):
        print(
            f"Creating a new instance of Weaviate DB client"
        )
        get_weaviate_db_client.instance = LocalWeaviateDB(
            host=api_settings.WEAVIATE_DB_HOST,
            port=api_settings.WEAVIATE_DB_PORT,
            grpc_port=api_settings.WEAVIATE_DB_GRPC_PORT

        )
    return get_weaviate_db_client.instance


class LocalWeaviateDB(
        DatabaseBackendShape[wv.WeaviateClient]
):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        grpc_port: int = 50051,
        headers: Optional[dict] = None,
        auth_credentials: Optional[Any] = None,
        connector: Optional[Callable[..., wv.WeaviateClient]] = None,
        test_mode: bool = False,
    ):
        if test_mode:
            client = None
            self.connected = False
        else:
            connect_fn = connector or wv.connect_to_local
            client = connect_fn(
                host=host,
                port=port,
                grpc_port=grpc_port,
                headers=headers,
                auth_credentials=auth_credentials,
            )
            self.connected = True
        super().__init__(client)

    @property
    def conn(self) -> wv.WeaviateClient:
        if not self._client:
            raise ConnectionError("Client not initialized (test_mode=True?)")
        return self._client

    def __enter__(self):
        if not self.conn.is_ready():
            raise ConnectionError("Weaviate not ready")
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn.is_connected():
            self.conn.close()

    @contextmanager
    def cursor(self) -> Any:
        """Weaviate does not support cursors; use context manager instead."""
        raise NotImplementedError("Cursor not supported")

    def _create_schema(self, schema_data: dict):
        if not self.conn:
            raise RuntimeError("Client not initialized")
        questions = self.conn.collections.create_from_dict(**schema_data)
        print("Schema created:", questions)
        return questions
