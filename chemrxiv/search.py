"""Search criteria for ChemRxiv."""

from typing import Dict, List, Optional

from .sort import SortCriterion


class Search:
    """A specification for a search of ChemRxiv's database."""

    term: str
    """The search query string."""
    skip: int
    """Number of results to skip (for pagination)."""
    limit: int
    """Maximum number of results to return."""
    sort: SortCriterion
    """The sort criterion for results."""
    author: Optional[str]
    """Filter by author name."""
    search_date_from: Optional[str]
    """Start date for search filter."""
    search_date_to: Optional[str]
    """End date for search filter."""
    search_license: Optional[str]
    """Filter by license."""
    category_ids: List[str]
    """Filter by category IDs."""
    subject_ids: List[str]
    """Filter by subject IDs."""

    def __init__(
        self,
        term: str = "",
        skip: int = 0,
        limit: int = 10,
        sort: SortCriterion = SortCriterion.PUBLISHED_DATE_DESC,
        author: Optional[str] = None,
        search_date_from: Optional[str] = None,
        search_date_to: Optional[str] = None,
        search_license: Optional[str] = None,
        category_ids: List[str] = None,
        subject_ids: List[str] = None,
    ):
        """Constructs a search with the specified criteria."""
        self.term = term
        self.skip = skip

        self.limit = limit

        self.sort = sort
        self.author = author
        self.search_date_from = search_date_from
        self.search_date_to = search_date_to
        self.search_license = search_license
        self.category_ids = category_ids or []
        self.subject_ids = subject_ids or []

    def __str__(self) -> str:
        return f"Search(term='{self.term}')"

    def __repr__(self) -> str:
        return (
            f"Search(term={self.term!r}, skip={self.skip!r}, "
            f"limit={self.limit!r}, sort={self.sort!r})"
        )

    def url_args(self) -> Dict[str, str]:
        """Returns a dict of search parameters for API requests."""
        args = {}

        if self.term:
            args["term"] = self.term

        if self.skip:
            args["skip"] = str(self.skip)

        if self.limit:
            args["limit"] = str(self.limit)

        if self.sort:
            args["sort"] = self.sort.value

        if self.author:
            args["author"] = self.author

        if self.search_date_from:
            args["searchDateFrom"] = self.search_date_from

        if self.search_date_to:
            args["searchDateTo"] = self.search_date_to

        if self.search_license:
            args["searchLicense"] = self.search_license

        if self.category_ids:
            args["categoryIds"] = ",".join(self.category_ids)

        if self.subject_ids:
            args["subjectIds"] = ",".join(self.subject_ids)

        return args
