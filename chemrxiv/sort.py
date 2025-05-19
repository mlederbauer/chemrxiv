"""Sorting criteria for ChemRxiv search results."""

from enum import Enum


class SortCriterion(Enum):
    """A SortCriterion identifies a property by which search results can be
    sorted."""

    VIEWS_COUNT_ASC = "VIEWS_COUNT_ASC"
    VIEWS_COUNT_DESC = "VIEWS_COUNT_DESC"
    CITATION_COUNT_ASC = "CITATION_COUNT_ASC"
    CITATION_COUNT_DESC = "CITATION_COUNT_DESC"
    READ_COUNT_ASC = "READ_COUNT_ASC"
    READ_COUNT_DESC = "READ_COUNT_DESC"
    RELEVANT_ASC = "RELEVANT_ASC"
    RELEVANT_DESC = "RELEVANT_DESC"
    PUBLISHED_DATE_ASC = "PUBLISHED_DATE_ASC"
    PUBLISHED_DATE_DESC = "PUBLISHED_DATE_DESC"
