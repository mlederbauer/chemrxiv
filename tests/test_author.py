"""Tests for the Author class."""

from chemrxiv.author import Author


def test_author_creation():
    """Test basic author creation."""
    author = Author("John Doe")
    assert author.name == "John Doe"
    assert author.orcid_id is None
    assert author.affiliations == []


def test_author_with_orcid():
    """Test author creation with ORCID ID."""
    author = Author("Jane Smith", orcid_id="0000-0000-0000-0000")
    assert author.name == "Jane Smith"
    assert author.orcid_id == "0000-0000-0000-0000"


def test_author_with_affiliations():
    """Test author creation with affiliations."""
    affiliations = ["University A", "Institute B"]
    author = Author("Alice Brown", affiliations=affiliations)
    assert author.name == "Alice Brown"
    assert author.affiliations == affiliations


def test_author_string_representation():
    """Test string representation of author."""
    author = Author("John Doe")
    assert str(author) == "John Doe"
    assert (
        repr(author)
        == "Author(name='John Doe', orcid_id=None, affiliations=[])"
    )
