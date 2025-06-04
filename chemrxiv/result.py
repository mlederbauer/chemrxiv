"""ChemRxiv API Wrapper.

A Python wrapper for the ChemRxiv API.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.request import Request, urlopen

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
        keywords: Optional[List[str]] = None,
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
        self.keywords = keywords or []
        self._raw = _raw

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"Result(id={self.id!r}, title={self.title!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Result):
            return self.id == other.id
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Result to a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "abstract": self.abstract,
            "doi": self.doi,
            "published_date": self.published_date,
            "updated_date": self.updated_date,
            "categories": self.categories,
            "license": self.license,
            "pdf_url": self.pdf_url,
            "views_count": self.views_count,
            "read_count": self.read_count,
            "citation_count": self.citation_count,
            "keywords": self.keywords,
            "raw": self._raw,
        }

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
                            orcid_id=author_data.get("id")
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
                keywords=data.get("keywords"),
                _raw=data,
            )
        except Exception as e:
            logger.error(f"Error creating Result object: {e!s}")
            raise

    def download_pdf(self, dirpath: str = "./", filename: str = "") -> str:
        if not self.pdf_url:
            raise ValueError("No PDF URL available for this result")

        # Build a filename under dirpath
        if not filename:
            filename = f"{self.id}.pdf"
        out_path = os.path.join(dirpath, filename)

        # Create a Request with a browser-like User-Agent
        req = Request(
            self.pdf_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/115.0.0.0 Safari/537.36"
                ),
            },
        )

        # Open + read + write to disk
        with urlopen(req) as response, open(out_path, "wb") as f:
            f.write(response.read())

        return out_path

    def download_si(self, dirpath: str = "./", filename: str = "") -> str:
        # pdf is in results[i]._raw.suppItems[j].asset.original.url. there are several suppItems possible; if there are multiple, attach _0 etc.

        if not self._raw:
            raise ValueError("No raw data available for this result")

        if not self._raw.get("suppItems"):
            raise ValueError(
                "No supplementary items available for this result"
            )

        for supp_item in self._raw["suppItems"]:
            if supp_item.get("asset") and supp_item["asset"].get("original"):
                pdf_url = supp_item["asset"]["original"].get("url")
                req = Request(
                    pdf_url,
                    headers={
                        "User-Agent": (
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/115.0.0.0 Safari/537.36"
                        ),
                    },
                )

                if not filename:
                    filename = f"{self.id}_si.pdf"

                out_path = os.path.join(dirpath, filename)

                with urlopen(req) as response, open(out_path, "wb") as f:
                    f.write(response.read())

        return out_path
