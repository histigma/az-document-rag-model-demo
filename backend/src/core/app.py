__all__ = (
    'CoreApp',
)
import logging
from fastapi import FastAPI
from routes import eventhub, rag


class CoreApp(
    FastAPI
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def register_routes(self):
        self.include_router(rag.router, prefix="/rag", tags=["Items"])
        self.include_router(eventhub.router, prefix="/eventhub", tags=["Event Hub"])

