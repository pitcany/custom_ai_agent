from langchain.tools import tool


class SearchManager:
    """Manages search provider swapping."""

    def __init__(self, provider=None):
        if provider is None:
            from tools.search_providers.duckduckgo import DuckDuckGoProvider

            provider = DuckDuckGoProvider()
        self.provider = provider

    def search(self, query: str, num_results: int = 3) -> str:
        """Delegate to current provider."""
        return self.provider.search(query, num_results)


_search_manager = SearchManager()


@tool
def search_web(query: str, num_results: int = 3) -> str:
    """Search the web for information.

    Args:
        query: Search query.
        num_results: Number of results to return (default: 3).

    Returns:
        Formatted search results with summaries.
    """
    return _search_manager.search(query, num_results)
