from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic
from contextlib import contextmanager

Td = TypeVar('Td')

class DatabaseBackendShape(
        ABC, 
        Generic[Td]
):
    def __init__(self, client: Td) -> None:
        self.__client = client

    @property
    def _client(self):
        return self.__client

    @property
    @abstractmethod
    def conn(self) -> Td:
        ...

    @contextmanager
    @abstractmethod
    def cursor(self, *args, **kwargs) -> Any:
        """Return a cursor context"""
        ...
