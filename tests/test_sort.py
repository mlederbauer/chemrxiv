"""Tests for the SortCriterion enum."""

from chemrxiv.sort import SortCriterion


def test_sort_criterion_values():
    """Test that sort criteria have correct values."""
    assert SortCriterion.VIEWS_COUNT_ASC.value == "VIEWS_COUNT_ASC"
    assert SortCriterion.VIEWS_COUNT_DESC.value == "VIEWS_COUNT_DESC"
    assert SortCriterion.CITATION_COUNT_ASC.value == "CITATION_COUNT_ASC"
    assert SortCriterion.CITATION_COUNT_DESC.value == "CITATION_COUNT_DESC"
    assert SortCriterion.READ_COUNT_ASC.value == "READ_COUNT_ASC"
    assert SortCriterion.READ_COUNT_DESC.value == "READ_COUNT_DESC"
    assert SortCriterion.RELEVANT_ASC.value == "RELEVANT_ASC"
    assert SortCriterion.RELEVANT_DESC.value == "RELEVANT_DESC"
    assert SortCriterion.PUBLISHED_DATE_ASC.value == "PUBLISHED_DATE_ASC"
    assert SortCriterion.PUBLISHED_DATE_DESC.value == "PUBLISHED_DATE_DESC"


def test_sort_criterion_comparison():
    """Test that sort criteria can be compared."""
    assert SortCriterion.VIEWS_COUNT_ASC != SortCriterion.VIEWS_COUNT_DESC
    assert (
        SortCriterion.PUBLISHED_DATE_DESC == SortCriterion.PUBLISHED_DATE_DESC
    )
