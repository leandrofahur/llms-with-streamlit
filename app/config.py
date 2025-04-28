import os

def get_openai_api_key() -> str:
    """
    Retrieve the OpenAI API key from environment variables.
    Returns None if not found.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        print(f"✅ OPENAI_API_KEY loaded successfully!!!")
    else:
        print(f"⚠️ No OPENAI_API_KEY found. Using default model instead.")
    
    return openai_api_key

def get_llm():
    """
    Get the LLM instance.
    This is a stub that doesn't actually load a model, since we're not using the AI functions.
    """
    return None