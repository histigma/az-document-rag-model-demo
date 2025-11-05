"""

Azure Cosmos DB connector.

"""
from .abs import DatabaseBackendShape
from typing import Any
from contextlib import contextmanager

from azure.cosmos import CosmosClient

__all__ =(
    'CosmosDB',
)

class CosmosDB(
        DatabaseBackendShape[CosmosClient]
):
    def __init__(
            self, 
            endpoint: str, 
            key: str, 
            database_name: str
    ):
        client = CosmosClient(
            endpoint, 
            key
        )
        super().__init__(client)
        self._database_name = database_name

    @property
    def conn(self) -> CosmosClient:
        return self._client

    @contextmanager
    def cursor(self, container_name: str) -> Any:
        """Context-managed access to a specific container."""
        container = None
        try:
            container = (
                self.conn
                .get_database_client(self._database_name)
                .get_container_client(container_name)
            )
            yield container
        finally:
            container = None
