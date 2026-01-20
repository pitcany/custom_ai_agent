from langchain_community.tools.tavily_search import TavilySearchResults
from . import SearchProvider


class TavilyProvider(SearchProvider):
    """Tavily search provider (higher quality, requires API key)."""

    def __init__(self, api_key: str):
        self._search = TavilySearchResults(max_results=5)
        self.api_key = api_key

    def search(self, query: str, num_results: int = 3) -> str:
        """Search using Tavily."""
        try:
            results = self._search.invoke({"query": query})
            formatted = []
            for item in results.get("results", []):
                formatted.append(
                    f"- {item.get('title', '')}: {item.get('content', '')}"
                )
            return f"Search results for '{query}':\n" + "\n".join(formatted)
        except Exception as e:
            return f"Error searching: {str(e)}"
