"""
Connect to Weaviate Database.

But Cloud Weaviate is not supported yet in this module.

"""
from .abs import DatabaseBackendShape
from typing import Any
from contextlib import contextmanager

import weaviate as wv
import weaviate.classes as wvc
from weaviate.exceptions import WeaviateInvalidInputError

__all__ =(
    'LocalWeaviateDB',
)

class LocalWeaviateDB(
        DatabaseBackendShape[wv.WeaviateClient]
):
    def __init__(
            self, 
            host='localhost',
            port=8080,
            grpc_port=50051,
            headers=None,
            auth_credentials=None,
    ):
        client = wv.connect_to_local(
            host=host,
            port=port,
            grpc_port=grpc_port,
            headers=headers,
            auth_credentials=auth_credentials
        )
        super().__init__(client)
        self.connected = True

    @property
    def conn(self) -> wv.WeaviateClient:
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
        """
        Not implemented: Weaviate DB is not supported Cursor. 
        Use `with` statement for this client class.
        """
        raise NotImplementedError(
            "Cursor not supported"
        )

    def _create_schema(self, schema_data: dict):
        questions = self.conn.collections.create_from_dict(**schema_data)
        print('SChema created: ', questions)
        return questions
