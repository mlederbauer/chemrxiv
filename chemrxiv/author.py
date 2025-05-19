"""Authors of ChemRxiv preprints."""

from typing import List, Optional


class Author:
    """An author of a ChemRxiv preprint."""

    name: str
    """The author's name."""
    id: Optional[str]
    """The author's ID."""
    affiliations: List[str]
    """The author's affiliations."""

    def __init__(
        self,
        name: str,
        author_id: Optional[str] = None,
        affiliations: List[str] = None,
    ):
        """Constructs an `Author` with the specified metadata."""
        self.name = name
        self.id = author_id
        self.affiliations = affiliations or []

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Author(name={repr(self.name)}, id={repr(self.id)}, affiliations={repr(self.affiliations)})"
