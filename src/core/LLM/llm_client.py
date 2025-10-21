import os
from pathlib import Path
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from src.core.utils.constants import PROVIDER_GROQ, PROVIDER_OPENAI, DEFAULT_GROQ_MODEL, DEFAULT_OPENAI_MODEL
from dotenv import load_dotenv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
print("Base Directory:", BASE_DIR)
load_dotenv(os.path.join(BASE_DIR, ".env"))
class LLMFactory:
    def __init__(self):
        pass

    def get_llm_model(self, provider: str, llm_name: str = None):
        """
        Return an LLM instance based on provider (groq or openai).
        """
        try:
            if provider.lower() == PROVIDER_GROQ:
                return self._get_groq_model(llm_name)
            elif provider.lower() == PROVIDER_OPENAI:
                return self._get_openai_model(llm_name)
            else:
                raise ValueError(f"Unsupported provider: {provider}")
        except Exception as e:
            raise ValueError(f"Error initializing {provider} LLM: {e}")

    def _get_groq_model(self, llm_name: str = None) -> ChatGroq:
        groq_api_key = os.environ.get("GROQ_API_KEY")
        #print("Groq API Key:", groq_api_key)
        if not groq_api_key:
            raise ValueError("Groq API key is missing. Set GROQ_API_KEY environment variable.")

        if not llm_name:
            llm_name = DEFAULT_GROQ_MODEL  # default Groq model

        return ChatGroq(api_key=groq_api_key, model=llm_name,temperature=0.3)

    def _get_openai_model(self, llm_name: str = None) -> ChatOpenAI:
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OpenAI API key is missing. Set OPENAI_API_KEY environment variable.")

        if not llm_name:
            llm_name =DEFAULT_OPENAI_MODEL  # default OpenAI model

        return ChatOpenAI(api_key=openai_api_key, model=llm_name,temperature=0.3)
