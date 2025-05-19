"""Custom exceptions module for the ChemRxiv API wrapper."""


class ChemRxivError(Exception):
    """Base exception for ChemRxiv API errors."""

    url: str
    """The URL that triggered this error."""
    retry: int
    """The retry count when this error occurred."""
    message: str
    """Description of the error."""

    def __init__(self, url: str, retry: int, message: str):
        self.url = url
        self.retry = retry
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message} ({self.url})"


class HTTPError(ChemRxivError):
    """Error raised when an HTTP request fails."""

    status_code: int
    """The HTTP status code of the failed request."""

    def __init__(self, url: str, retry: int, status_code: int):
        self.status_code = status_code
        super().__init__(
            url, retry, f"HTTP request failed with status code {status_code}"
        )


class ItemWithdrawnError(ChemRxivError):
    """Error raised when trying to access a withdrawn item."""

    def __init__(self, url: str, retry: int):
        super().__init__(url, retry, "Item has been withdrawn")
