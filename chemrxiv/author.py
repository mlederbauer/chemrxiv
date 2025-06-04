"""Authors of ChemRxiv preprints."""

from typing import List, Optional


class Author:
    """An author of a ChemRxiv preprint."""

    name: str
    """The author's name."""
    orcid_id: Optional[str]
    """The author's ORCID ID."""
    affiliations: List[str]
    """The author's affiliations."""

    def __init__(
        self,
        name: str,
        orcid_id: Optional[str] = None,
        affiliations: List[str] = None,
    ):
        """Constructs an `Author` with the specified metadata."""
        self.name = name
        self.orcid_id = orcid_id
        self.affiliations = affiliations or []

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Author(name={self.name!r}, orcid_id={self.orcid_id!r}, affiliations={self.affiliations!r})"
