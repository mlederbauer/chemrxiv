"""Tests for the Search class."""

from chemrxiv.search import Search
from chemrxiv.sort import SortCriterion


def test_search_creation():
    """Test basic search creation."""
    search = Search()
    assert search.term == ""
    assert search.skip == 0
    assert search.limit == 10
    assert search.sort == SortCriterion.PUBLISHED_DATE_DESC
    assert search.author is None
    assert search.search_date_from is None
    assert search.search_date_to is None
    assert search.search_license is None
    assert search.category_ids == []
    assert search.subject_ids == []


def test_search_with_parameters():
    """Test search creation with parameters."""
    search = Search(
        term="catalysis",
        skip=20,
        limit=50,
        sort=SortCriterion.VIEWS_COUNT_DESC,
        author="John Doe",
        search_date_from="2023-01-01",
        search_date_to="2023-12-31",
        search_license="cc-by",
        category_ids=["cat1", "cat2"],
        subject_ids=["sub1"],
    )
    assert search.term == "catalysis"
    assert search.skip == 20
    assert search.limit == 50
    assert search.sort == SortCriterion.VIEWS_COUNT_DESC
    assert search.author == "John Doe"
    assert search.search_date_from == "2023-01-01"
    assert search.search_date_to == "2023-12-31"
    assert search.search_license == "cc-by"
    assert search.category_ids == ["cat1", "cat2"]
    assert search.subject_ids == ["sub1"]


def test_search_url_args():
    """Test URL argument generation."""
    search = Search(
        term="catalysis",
        skip=10,
        limit=20,
        sort=SortCriterion.CITATION_COUNT_DESC,
        author="Jane Smith",
        category_ids=["cat1", "cat2"],
    )
    args = search.url_args()
    assert args["term"] == "catalysis"
    assert args["skip"] == "10"
    assert args["limit"] == "20"
    assert args["sort"] == "CITATION_COUNT_DESC"
    assert args["author"] == "Jane Smith"
    assert args["categoryIds"] == "cat1,cat2"


def test_search_string_representation():
    """Test string representation of search."""
    search = Search(term="catalysis")
    assert str(search) == "Search(term='catalysis')"
    assert (
        repr(search)
        == "Search(term='catalysis', skip=0, limit=10, sort=<SortCriterion.PUBLISHED_DATE_DESC: 'PUBLISHED_DATE_DESC'>)"
    )
