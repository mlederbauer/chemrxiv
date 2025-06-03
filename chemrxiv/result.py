"""ChemRxiv API Wrapper.

A Python wrapper for the ChemRxiv API.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from .author import Author
from .category import Category
from .license import License

logger = logging.getLogger(__name__)


class Result:
    """A preprint in ChemRxiv's database."""

    id: str
    """The preprint's unique ID."""
    title: str
    """The preprint's title."""
    authors: List[Author]
    """The preprint's authors."""
    abstract: str
    """The preprint's abstract."""
    doi: Optional[str]
    """The preprint's DOI."""
    published_date: Optional[datetime]
    """When the preprint was published."""
    updated_date: Optional[datetime]
    """When the preprint was last updated."""
    categories: List[Category]
    """The preprint's categories."""
    license: Optional[License]
    """The preprint's license."""
    pdf_url: Optional[str]
    """URL for downloading the PDF."""
    views_count: Optional[int]
    """Number of views."""
    read_count: Optional[int]
    """Number of reads."""
    citation_count: Optional[int]
    """Number of citations."""

    def __init__(
        self,
        item_id: str,
        title: str = "",
        authors: List[Author] = None,
        abstract: str = "",
        doi: Optional[str] = None,
        published_date: Optional[datetime] = None,
        updated_date: Optional[datetime] = None,
        categories: List[Category] = None,
        license: Optional[License] = None,
        pdf_url: Optional[str] = None,
        views_count: Optional[int] = None,
        read_count: Optional[int] = None,
        citation_count: Optional[int] = None,
        _raw: Optional[Dict[str, Any]] = None,
    ):
        """Constructs a Result with the specified metadata."""
        self.id = item_id
        self.title = title
        self.authors = authors or []
        self.abstract = abstract
        self.doi = doi
        self.published_date = published_date
        self.updated_date = updated_date
        self.categories = categories or []
        self.license = license
        self.pdf_url = pdf_url
        self.views_count = views_count
        self.read_count = read_count
        self.citation_count = citation_count
        self._raw = _raw

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"Result(id={repr(self.id)}, title={repr(self.title)})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Result):
            return self.id == other.id
        return False

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> Result:
        """Constructs a Result from API response data."""
        try:
            authors = []
            for author_data in data.get("authors", []):
                # Handle different author data formats
                if isinstance(author_data, dict):
                    name = author_data.get("name", "")
                    if (
                        not name
                        and "firstName" in author_data
                        and "lastName" in author_data
                    ):
                        name = f"{author_data.get('firstName', '')} {author_data.get('lastName', '')}".strip()

                    affiliations = []
                    if "institutions" in author_data and isinstance(
                        author_data["institutions"], list
                    ):
                        affiliations = [
                            inst.get("name", "")
                            for inst in author_data["institutions"]
                            if isinstance(inst, dict)
                        ]

                    authors.append(
                        Author(
                            name=name,
                            author_id=author_data.get("id")
                            or author_data.get("orcid"),
                            affiliations=affiliations,
                        )
                    )

            categories = []
            for cat_data in data.get("categories", []):
                if isinstance(cat_data, dict):
                    categories.append(
                        Category(
                            category_id=cat_data.get("id", ""),
                            name=cat_data.get("name", ""),
                            description=cat_data.get("description"),
                        )
                    )

            license_data = data.get("license")
            license_obj = None
            if license_data and isinstance(license_data, dict):
                license_obj = License(
                    license_id=license_data.get("id", ""),
                    name=license_data.get("name", ""),
                    description=license_data.get("description"),
                    url=license_data.get("url"),
                )

            published_date = None
            if data.get("publishedDate"):
                try:
                    published_date = datetime.fromisoformat(
                        data["publishedDate"].replace("Z", "+00:00")
                    )
                except (ValueError, TypeError):
                    logger.warning(
                        f"Failed to parse published date: {data.get('publishedDate')}"
                    )

            updated_date = None
            if data.get("updatedDate"):
                try:
                    updated_date = datetime.fromisoformat(
                        data["updatedDate"].replace("Z", "+00:00")
                    )
                except (ValueError, TypeError):
                    logger.warning(
                        f"Failed to parse updated date: {data.get('updatedDate')}"
                    )

            # Extract PDF URL from asset data if available
            pdf_url = data.get("pdfUrl")
            if (
                not pdf_url
                and "asset" in data
                and isinstance(data["asset"], dict)
            ):
                if "original" in data["asset"] and isinstance(
                    data["asset"]["original"], dict
                ):
                    pdf_url = data["asset"]["original"].get("url")

            return cls(
                item_id=data.get("id", ""),
                title=data.get("title", ""),
                authors=authors,
                abstract=data.get("abstract", ""),
                doi=data.get("doi"),
                published_date=published_date,
                updated_date=updated_date,
                categories=categories,
                license=license_obj,
                pdf_url=pdf_url,
                views_count=data.get("viewsCount"),
                read_count=data.get("readCount"),
                citation_count=data.get("citationCount"),
                _raw=data,
            )
        except Exception as e:
            logger.error(f"Error creating Result object: {str(e)}")
            raise

    def download_pdf(self, dirpath: str = "./", filename: str = "") -> str:
        """Downloads the PDF for this result to the specified directory.

        Returns the path to the downloaded file.
        """
        if not self.pdf_url:
            raise ValueError("No PDF URL available for this result")

        import os
        from urllib.request import urlretrieve

        if not filename:
            filename = f"{self.id}.pdf"

        path = os.path.join(dirpath, filename)
        written_path, _ = urlretrieve(self.pdf_url, path)
        return written_path
