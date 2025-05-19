"""Tests for the ChemRxiv client."""

from chemrxiv.client import Client
from chemrxiv.search import Search


def test_client():
    """Test that the client is initialized correctly."""
    client = Client()
    assert client is not None


def test_categories():
    """Test that the categories are retrieved correctly."""
    client = Client()
    categories = client.categories()
    assert len(categories) > 0


def test_licenses():
    """Test that the licenses are retrieved correctly."""
    client = Client()
    licenses = client.licenses()
    assert len(licenses) > 0


def test_item():
    """Test that the item is retrieved correctly."""
    client = Client()
    item = client.item("6826a61850018ac7c5739260")
    assert item is not None


def test_results():
    """Test that the results are retrieved correctly."""
    client = Client()
    results = client.results(Search())
    assert results is not None


def test_item_by_doi():
    """Test that the item by DOI is retrieved correctly."""
    client = Client()
    item = client.item_by_doi("10.26434/chemrxiv-2025-5j4tn")
    assert item is not None
