"""Tests for custom exceptions."""

from chemrxiv.exceptions import ChemRxivError, HTTPError, ItemWithdrawnError


def test_chemrxiv_error():
    """Test basic ChemRxivError creation and string representation."""
    error = ChemRxivError("https://example.com", 2, "Test error")
    assert error.url == "https://example.com"
    assert error.retry == 2
    assert error.message == "Test error"
    assert str(error) == "Test error (https://example.com)"


def test_http_error():
    """Test HTTPError creation and attributes."""
    error = HTTPError("https://example.com", 1, 404)
    assert error.url == "https://example.com"
    assert error.retry == 1
    assert error.status_code == 404
    assert "404" in str(error)


def test_item_withdrawn_error():
    """Test ItemWithdrawnError creation and message."""
    error = ItemWithdrawnError("https://example.com", 0)
    assert error.url == "https://example.com"
    assert error.retry == 0
    assert "withdrawn" in str(error).lower()
