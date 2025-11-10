import pytest
from modules.db.repository import WeaviateVectorRepository
from modules.db.driver.weaviate_client import LocalWeaviateDB
from modules.openai.vectorize import DataVectorizer
from modules.openai.embedding import get_az_embeddings, AzureOpenAIEmbeddingAdapter
from modules.db.repository.models import WeaviateRepoQueryResult
from settings import RagPartition

def test_db_repo_wv():
    vectorizer = DataVectorizer(
        AzureOpenAIEmbeddingAdapter(get_az_embeddings())
    )

    db = LocalWeaviateDB()
    repo = WeaviateVectorRepository(
        db, vectorizer=vectorizer
    )
    result = repo.query(
        RagPartition.DEFAULT.value,
        'test'
    )
    print(result, type(result))
    assert isinstance(vectorizer, DataVectorizer)
    assert isinstance(result, WeaviateRepoQueryResult)



