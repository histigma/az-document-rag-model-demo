from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from langchain_core.documents import Document

class BaseDocParser(ABC):
    def __init__(self, document: Optional["Document"] = None):
        self.parsed = self.parse(
            document
        ) if document else None

    @abstractmethod
    def parse(self, document) -> str:
        ...

    def __call__(self, document):
        return self.parse(document)
    
    def __str__(self):
        return self.parsed or ""
