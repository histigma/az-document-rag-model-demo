from .abs import BaseOpenAIConversation
from langchain_openai import AzureChatOpenAI
from settings import api_settings

__all__ = (
    'get_az_llm',
    'BaseOpenAIConversation',
    'AzureOpenAIConversationAdapter'
)

def get_az_llm():
    """
    Get instance of AzureChatOpenAI

    **Attention**:
    You must set and load the following environments variables:  
        - `AZURE_OPENAI_API_KEY` or `AZURE_OPENAI_AD_TOKEN`  
        - `AZURE_OPENAI_ENDPOINT`  

    """
    max_retries = 2
    timeout = None
    max_completion_tokens=None
    if not hasattr(get_az_llm, "_instance"):
        print(
            f"Creating a new instance of Azure OpenAI: {api_settings.OPENAI_GPT_MODEL}, {api_settings.OPENAI_API_VERSION}"
        )
        get_az_llm._instance = AzureChatOpenAI(
            azure_deployment=api_settings.OPENAI_GPT_MODEL,
            api_version=api_settings.OPENAI_API_VERSION,
            temperature=api_settings.LLM_TEMPERATURE,
            max_completion_tokens=max_completion_tokens,
            timeout=timeout,
            max_retries=max_retries,
        )
    return get_az_llm._instance

#   Create a instance once server starts.
if __name__ != '__main__':
    get_az_llm()


class AzureOpenAIConversationAdapter(
    BaseOpenAIConversation[AzureChatOpenAI]
):
    ...
    


