
from modules.db.driver import DatabaseBackendShape
from typing import Generic, TypeVar

from .wv_schema_registry import *


Connector = TypeVar('Connector', bound=DatabaseBackendShape)

class StockDataLoader(
    Generic[Connector]
):
    def __init__(self, db_connector: Connector) -> None:
        self._db_connector = db_connector


    def create_if_not_exists_schema(self):
        schema = {
            "class": "StockData",
            "vectorizer": "none",       # 'Vectorizer' is needed set to none when external creating...
            "properties": [
                {"name": "symbol", "dataType": ["string"]},
                {"name": "date",   "dataType": ["date"]},
                {"name": "open",   "dataType": ["number"]},
                {"name": "close",  "dataType": ["number"]},
                {"name": "volume", "dataType": ["number"]},
                {"name": "embedded_vector", "dataType": ["number[]"]}
            ]
        }

