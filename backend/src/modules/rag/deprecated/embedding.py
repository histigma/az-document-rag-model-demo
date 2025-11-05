raise NotImplementedError(
    f"{__name__} is a deprecated Module"
)

import os
from openai import AzureOpenAI
import logging


class EmbeddingGenerator:
    BATCH_SIZE = 20

    def __init__(
            self, 
            openai_instance: AzureOpenAI,
            openai_embedding_deployment_name: str
    ):
        self._openai_instance = openai_instance
        self._openai_embedding_deployment_name = openai_embedding_deployment_name

    def _gen_embedding(self, text: list[str]) -> list:
        """Generates vectorized data (embeddings)  
        
        Args:
            text (list[str]):

        Returns:
            list: A list contains embeded dump data by open ai
        """
        try:
            res = self._openai_instance.embeddings.create(
                input=text,
                model=self._openai_embedding_deployment_name
            )
            data = res.model_dump()
            results = [
                data['embedding'] 
                for data in data['data']
            ]
            return results
        except Exception as e:
            logging.error(
                f"An error occured during create a embedding data {e}"
            )
            return [
                [0] * 1536
            ] * len(text)
    
    def batch(
            self,
            texts: list[str], 
    ):
        """Generates vectorized data for batches"""
        result = []
        for i in range(0, len(texts), self.BATCH_SIZE):
            chunk = texts[i : i+self.BATCH_SIZE]
            data = self._gen_embedding(
                chunk
            )
            result.extend(data)
        return result

