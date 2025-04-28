import os
from langchain_openai import ChatOpenAI
def get_openai_api_key() -> str:
    """
    Retrieve the OpenAI API key from environment variables.
    Raises an exception if the key is not found.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("❌ OPENAI_API_KEY not found. Please check your .env file.")
    else:
        print(f"✅ OPENAI_API_KEY loaded successfully!!!")
        return openai_api_key
    
def get_llm() -> ChatOpenAI:
    """
    Get the LLM instance.
    """
    return ChatOpenAI(model="gpt-4o", temperature=0.2, api_key=get_openai_api_key())