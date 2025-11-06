from .abs import BaseDocParser
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from langchain_core.documents import Document

__all__ = (
    'BaseDocParser',
    'ContextSearchDocParser',
    'SentenceLevelAnalysisDocParser',
)

class ContextSearchDocParser(
    BaseDocParser
):
    """Parsing a document for context search. (contains meta data)
    """
    def parse(self, document: "Document") -> str:
        title = document.metadata.get("title", "")
        lang = document.metadata.get("lang", "")
        return f"{title}\nLanguage: {lang}\n{document.page_content}"
    

class SentenceLevelAnalysisDocParser(
    BaseDocParser
):
    """Parsing a document for sentence level anaylsis such as 
    emotion analysis, meaning compares and clustering sentences.
    """
    def parse(self, document: "Document") -> str:
        return document.page_content

