"""Categories available for ChemRxiv preprints."""

from typing import Any, Dict, Optional


class Category:
    """A category from ChemRxiv's classification system."""

    id: str
    """The category's ID."""
    name: str
    """The category's name."""
    description: Optional[str]
    """The category's description."""
    count: Optional[int]
    """Number of preprints in this category."""
    parent_id: Optional[str]
    """The parent category's ID, if applicable."""

    def __init__(
        self,
        category_id: str,
        name: str,
        description: Optional[str] = None,
        count: Optional[int] = None,
        parent_id: Optional[str] = None,
    ):
        """Constructs a Category with the specified metadata."""
        self.id = category_id
        self.name = name
        self.description = description
        self.count = count
        self.parent_id = parent_id

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Category(id={repr(self.id)}, name={repr(self.name)})"

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]):
        """Constructs a Category from API response data."""
        return cls(
            category_id=data["id"],
            name=data["name"],
            description=data.get("description"),
            count=data.get("count"),
            parent_id=data.get("parentId"),
        )
