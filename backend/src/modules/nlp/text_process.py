from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from typing import List, Optional, TypeVar, Iterable
import logging

__all__ = (
    'TDocuments',
    'TextDataChunker'
)

TDocuments = TypeVar('TDocuments', str, Iterable[Document], Document)

class TextDataChunker:
    """
    An untility class load texts and chunkizes them.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        encoding: str = "utf-8",
        separator: str= "\n\n"
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = encoding
        self.separator = separator

    def _split(
            self, 
            documents: TDocuments,
            metadata: Optional[dict] = None
    ):
        """Split and chunks the documents"""
        if isinstance(documents, str):
            docs = [
                Document(page_content=documents, metadata=metadata or {})
            ]
        elif isinstance(documents, Document):
            if metadata:
                # shallow merge;
                merged = {**documents.metadata, **metadata}
                docs = [Document(page_content=documents.page_content, metadata=merged)]
            else:
                docs = [documents]
        elif isinstance(documents, Iterable):
            docs = []
            for item in documents:
                if isinstance(item, Document):
                    docs.append(item)
                elif isinstance(item, str):
                    docs.append(Document(page_content=item, metadata=metadata or {}))
                else:
                    raise TypeError(f"Iterable contains unsupported item type: {type(item)}")
        else:
            raise TypeError(f"Invalid document type: {type(documents)}")

        splitter = CharacterTextSplitter(
            separator=self.separator,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        logging.info(f"[{__class__.__name__}] Ready to split {len(docs)} documents (logical)...")
        chunks = splitter.split_documents(docs)
        logging.info(f"[{__class__.__name__}] A job spliting documents ({len(docs)}) is completed.")
        return chunks

    def from_text(
        self, 
        text: str, 
        metadata: Optional[dict] = None
    ) -> List[Document]:
        return self._split(text, metadata)        


