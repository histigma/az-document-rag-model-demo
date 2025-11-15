from modules.openai import BaseOpenAIConversation
import logging

__all__ = (
    'GeneralPromptHandleClient',
    'RAG_GENERAL_SYSTEM_CONTEXT'
)

RAG_GENERAL_SYSTEM_CONTEXT = """
SYSTEM:
You are a Retrieval-Augmented Generation (RAG) assistant designed to answer questions 
based strictly on the given context.

RULES:
1. Use ONLY the provided documents to answer.
2. If the answer is not in the documents, say:
   “The provided context does not contain the answer.”
3. Do NOT hallucinate. Do NOT add external knowledge.
4. Keep the answer factual, concise, and based on the documents.
5. If multiple documents conflict, list all possibilities without resolving them.
6. Do NOT output the context itself unless asked.
7. Maintain the user’s language in your response.

"""

class GeneralPromptHandleClient:
    """
    Makes a prompt for llm fit to subject by your configuration.
    """
    def __init__(
            self, 
            openai_client: BaseOpenAIConversation,
            system_context: str='',
    ):
        self._openai_client = openai_client
        self._system_context = system_context

    def chat_user_query(
            self, 
            user_query_question: str,
            context_internal: str=''
    ):
        # messages = [
        #     {
        #         "role": "system", 
        #         "content": self._system_context
        #     },
        #     {
        #         "role": "user", 
        #         "content": (
        #             f"Question: {user_query_question}\n\n"
        #             f"Context: {context_internal}"
        #         )
        #     }
        # ]
        messages = [
            (
                "system",
                self._system_context,
            ),
            (
                "human", 
                f"Question: {user_query_question}\n\n{'Context: ' if context_internal else ''}{context_internal}"
            ),
        ]
        try:
            message = self._openai_client.chat(
                messages
            )
        except Exception as e:
            logging.error(e)
            return None
        
        return message


