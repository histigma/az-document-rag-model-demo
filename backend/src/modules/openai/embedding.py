from .abs import BaseOpenAIEmbeddings
from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings
from settings import api_settings

__all__ = (
    'get_az_embeddings',
    'BaseOpenAIEmbeddings',
    'OpenAIEmbeddingAdapter',
    'AzureOpenAIEmbeddingAdapter',
)

def get_az_embeddings():
    """Return a singleton Azure OpenAI Embedding model instance
    """
    if not api_settings.OPENAI_EMBEDDINGS_DEPLOYMENT:
        raise EnvironmentError(
            f"{repr(api_settings.OPENAI_EMBEDDINGS_DEPLOYMENT)} is not defined!"
        )
    if not hasattr(get_az_embeddings, "_instance"):
        print(
            "Creating a new instance of Azure OpenAI Embedding Model: "
            f"{api_settings.OPENAI_GPT_MODEL}, {api_settings.OPENAI_API_VERSION}"
        )
        embeddings = AzureOpenAIEmbeddings(
            model=api_settings.OPENAI_EMBEDDINGS_DEPLOYMENT,
        )
        get_az_embeddings._instance = embeddings
    return get_az_embeddings._instance

#   Create a instance once server starts.
if __name__ != '__main__':
    get_az_embeddings()    

class OpenAIEmbeddingAdapter(
    BaseOpenAIEmbeddings[OpenAIEmbeddings]
):
    """Vetorizing text data using Open AI Embedding of Langchain"""
    ...


class AzureOpenAIEmbeddingAdapter(
    BaseOpenAIEmbeddings[AzureOpenAIEmbeddings]
):
    """[Azure] Vetorizing text data using Azure Open AI of Langchain"""
    ...

