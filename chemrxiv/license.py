"""Licenses available for ChemRxiv preprints."""

from typing import Any, Dict, Optional


class License:
    """A license available for ChemRxiv preprints."""

    id: str
    """The license's ID."""
    name: str
    """The license's name."""
    description: Optional[str]
    """The license's description."""
    url: Optional[str]
    """The license's URL."""

    def __init__(
        self,
        license_id: str,
        name: str,
        description: Optional[str] = None,
        url: Optional[str] = None,
    ):
        """Constructs a License with the specified metadata."""
        self.id = license_id
        self.name = name
        self.description = description
        self.url = url

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"License(id={repr(self.id)}, name={repr(self.name)})"

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]):
        """Constructs a License from API response data."""
        return cls(
            license_id=data["id"],
            name=data["name"],
            description=data.get("description"),
            url=data.get("url"),
        )
