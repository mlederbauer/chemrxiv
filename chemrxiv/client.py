"""ChemRxiv API Wrapper.

A Python wrapper for the ChemRxiv API.
"""

from __future__ import annotations

import logging
import time
from typing import Generator, List
from urllib.parse import urlencode

import requests

from .category import Category
from .exceptions import ChemRxivError, HTTPError, ItemWithdrawnError
from .license import License
from .result import Result
from .search import Search

logger = logging.getLogger(__name__)


class Client:
    """A client for accessing the ChemRxiv API."""

    base_url = "https://chemrxiv.org/engage/chemrxiv/public-api/v1"
    """The base URL for the ChemRxiv API."""

    def __init__(
        self,
        page_size: int = 10,
        delay_seconds: float = 1.0,
        num_retries: int = 3,
    ):
        """Constructs a ChemRxiv API client with the specified options."""
        self.page_size = min(page_size, 50)  # API maximum is 50
        self.delay_seconds = delay_seconds
        self.num_retries = num_retries
        self._last_request_time = None
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": "chemrxiv.py/0.1.0"})

    def __repr__(self) -> str:
        return f"Client(page_size={repr(self.page_size)}, delay_seconds={repr(self.delay_seconds)}, num_retries={repr(self.num_retries)})"

    def categories(self) -> List[Category]:
        """Retrieves all available categories from the ChemRxiv API."""
        url = f"{self.base_url}/categories"
        response = self._request(url)

        if response.status_code != 200:
            raise HTTPError(url, 0, response.status_code)

        data = response.json()
        categories = []

        for category_data in data.get("categories", []):
            categories.append(Category.from_api_response(category_data))

        return categories

    def licenses(self) -> List[License]:
        """Retrieves all available licenses from the ChemRxiv API."""
        url = f"{self.base_url}/licenses"
        response = self._request(url)

        if response.status_code != 200:
            raise HTTPError(url, 0, response.status_code)

        data = response.json()
        licenses = []

        for license_data in data.get("licenses", []):
            licenses.append(License.from_api_response(license_data))

        return licenses

    def item(self, item_id: str) -> Result:
        """Retrieves a specific item by its ID."""
        url = f"{self.base_url}/items/{item_id}"
        response = self._request(url)

        if response.status_code == 410:
            raise ItemWithdrawnError(url, 0)
        elif response.status_code != 200:
            raise HTTPError(url, 0, response.status_code)

        data = response.json()
        return Result.from_api_response(data)

    def item_by_doi(self, doi: str) -> Result:
        """Retrieves a specific item by its DOI."""
        url = f"{self.base_url}/items/doi/{doi}"
        response = self._request(url)

        if response.status_code == 410:
            raise ItemWithdrawnError(url, 0)
        elif response.status_code != 200:
            raise HTTPError(url, 0, response.status_code)

        data = response.json()
        return Result.from_api_response(data)

    def results(self, search: Search) -> Generator[Result, None, None]:
        """Executes a search and yields Result objects."""
        current_skip = search.skip
        total_retrieved = 0
        max_results = float("inf") if search.limit is None else search.limit

        while total_retrieved < max_results:
            # Adjust the search limit for the current page
            current_search = Search(
                term=search.term,
                skip=current_skip,
                limit=min(self.page_size, max_results - total_retrieved),
                sort=search.sort,
                author=search.author,
                search_date_from=search.search_date_from,
                search_date_to=search.search_date_to,
                search_license=search.search_license,
                category_ids=search.category_ids,
                subject_ids=search.subject_ids,
            )

            url = f"{self.base_url}/items"
            params = current_search.url_args()
            full_url = url + "?" + urlencode(params)

            logger.info(f"Making search request: {full_url}")
            response = self._request(full_url)

            if response.status_code != 200:
                raise HTTPError(full_url, 0, response.status_code)

            try:
                data = response.json()
                logger.info(
                    f"API returned total count: {data.get('totalCount', 0)}"
                )

                # Get items array from response
                items = data.get("itemHits", [])
                logger.info(f"Found {len(items)} items in response")

                if not items:
                    break

                # Process each item
                for item_data in items:
                    # Extract the actual item data from the nested structure
                    if "item" in item_data:
                        item_obj = item_data["item"]
                        result = Result.from_api_response(item_obj)
                        yield result
                        total_retrieved += 1
                        logger.info(
                            f"Processed item: {result.id} - {result.title}"
                        )
                    else:
                        logger.warning(
                            f"Item missing 'item' field: {item_data.keys()}"
                        )

                    if total_retrieved >= max_results:
                        break

                current_skip += len(items)

                if len(items) < current_search.limit:
                    # We've reached the end of results
                    break

            except Exception as e:
                logger.error(f"Error processing search results: {e}")
                raise

    def _request(self, url: str, retry_count: int = 0) -> requests.Response:
        """Makes a request to the ChemRxiv API with rate limiting and
        retries."""
        # Implement rate limiting
        if self._last_request_time is not None:
            elapsed = time.time() - self._last_request_time
            if elapsed < self.delay_seconds:
                time.sleep(self.delay_seconds - elapsed)

        try:
            logger.info(f"Requesting URL (retry {retry_count}): {url}")
            response = self._session.get(url)
            self._last_request_time = time.time()

            if response.status_code == 429:
                # Too many requests - implement backoff
                if retry_count < self.num_retries:
                    backoff = (retry_count + 1) * 2  # Exponential backoff
                    logger.warning(
                        f"Rate limited, backing off for {backoff} seconds"
                    )
                    time.sleep(backoff)
                    return self._request(url, retry_count + 1)
                else:
                    raise HTTPError(url, retry_count, response.status_code)

            return response
        except requests.exceptions.RequestException as e:
            if retry_count < self.num_retries:
                logger.warning(
                    f"Request failed ({e}), retrying ({retry_count + 1}/{self.num_retries})"
                )
                return self._request(url, retry_count + 1)
            else:
                raise ChemRxivError(url, retry_count, str(e))
