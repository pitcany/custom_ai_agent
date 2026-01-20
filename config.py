import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY")
    MODEL_NAME = "glm-4"
    TEMPERATURE = 0.01
    MAX_ITERATIONS = 5
    MAX_EXECUTION_TIME = 300
    VERBOSE = True

    SEARCH_PROVIDER = os.getenv("SEARCH_PROVIDER", "duckduckgo")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    LANGCHAIN_TRACING = os.getenv("LANGCHAIN_TRACING", "false").lower() == "true"
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "starter-agent")
    LANGCHAIN_ENDPOINT = os.getenv(
        "LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"
    )

    @classmethod
    def get_search_provider(cls):
        provider_name = cls.SEARCH_PROVIDER.lower()

        if provider_name == "tavily":
            if not cls.TAVILY_API_KEY:
                raise ValueError("TAVILY_API_KEY required for Tavily provider")
            from tools.search_providers.tavily import TavilyProvider

            return TavilyProvider(cls.TAVILY_API_KEY)

        elif provider_name == "duckduckgo":
            from tools.search_providers.duckduckgo import DuckDuckGoProvider

            return DuckDuckGoProvider()

        else:
            raise ValueError(f"Unknown search provider: {provider_name}")
