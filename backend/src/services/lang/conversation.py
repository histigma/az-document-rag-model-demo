from modules.openai import BaseOpenAIConversation
import logging

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
            # 채팅 완성 API 호출
            message = self._openai_client.chat(
                messages
            )
        except Exception as e:
            logging.error(e)
            return None
        
        return message


