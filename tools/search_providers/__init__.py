from abc import ABC, abstractmethod


class SearchProvider(ABC):
    """Abstract base class for search providers."""

    @abstractmethod
    def search(self, query: str, num_results: int = 3) -> str:
        """Execute search and return formatted results.

        Args:
            query: Search query.
            num_results: Number of results to return.

        Returns:
            Formatted search results.
        """
        pass
