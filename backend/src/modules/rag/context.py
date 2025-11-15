from langchain_core.documents import Document

class ContextGenerator:

    def format_docs_with_metadata(self, docs: list[Document]) -> str:
        """"""
        formatted_docs = []
        for doc in docs:
            source = doc.metadata.get("source", "Unknown Source")
            content = doc.page_content
            formatted_docs.append(f"Source: {source}\nContent:\n{content}")
        
        return "\n\n---\n\n".join(formatted_docs)
