from langchain_community.tools import DuckDuckGoSearchRun
from . import SearchProvider


class DuckDuckGoProvider(SearchProvider):
    """DuckDuckGo search provider (free, no API key)."""

    def __init__(self):
        self._search = DuckDuckGoSearchRun()

    def search(self, query: str, num_results: int = 3) -> str:
        """Search using DuckDuckGo."""
        try:
            results = self._search.run(query)
            return f"Search results for '{query}':\n{results}"
        except Exception as e:
            return f"Error searching: {str(e)}"
