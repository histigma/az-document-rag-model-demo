import weaviate.classes as wvc

all = (
    'STOCK_SCHEMA',
)

STOCK_SCHEMA = {
    "name": "StockData",
    "vector_config":     wvc.config.Configure.Vectors.text2vec_openai(),    # Set the vectorizer to "text2vec-openai" to use the OpenAI API for vector-related operations
    # "generative_config": wvc.config.Configure.Generative.cohere(),          # Set the generative module to "generative-cohere" to use the Cohere API for RAG
    "properties": [
        wvc.config.Property(
            name      = "question",
            data_type = wvc.config.DataType.TEXT,
        ),
    ]
}
