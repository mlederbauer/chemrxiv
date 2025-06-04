# ChemRxiv

A Python wrapper for accessing the ChemRxiv preprint server Open Engage API. ChemRxiv is a preprint server launched in 2016. This library provides programmatic access to preprints. Note: Usage is subject to ChemRxiv's licensing terms and attribution requirements which may restrict commercial and non-commercial use of the retrieved data. The publications might have been retracted or are not yet peer-reviewed.

## Installation

```
pip install chemrxiv
```

## Usage

### Initialize Client

### Search publications according to keywords

###

Python wrapper for the ChemRxiv API.

ChemRxiv is the free preprint repository for chemistry, providing open access to early research outputs in chemistry and related fields. This package provides a convenient Python interface to search, download, and interact with ChemRxiv content.

## Installation

```bash
pip install chemrxiv
```

## Quick Start

In your Python script, include the line:

```python
import chemrxiv
```

## Usage Examples

### Basic Search

```python
import chemrxiv

# Create the default API client
client = chemrxiv.Client()

# Search for papers about catalysis
search = chemrxiv.Search(
    term="catalysis",
    limit=10,
    sort=chemrxiv.SortCriterion.PUBLISHED_DATE_DESC
)

results = list(client.results(search))

# Print titles of found papers
for paper in results:
    print(f"Title: {paper.title}")
    print(f"Authors: {', '.join(str(author) for author in paper.authors)}")
    print(f"DOI: {paper.doi}")
    print("---")
```

### Advanced Search with Filters

```python
import chemrxiv
from datetime import datetime

# Search with date range and license filters
filtered_search = chemrxiv.Search(
    term="ammonia decomposition",
    limit=5,
    search_date_from="2023-01-01T00:00:00.000Z",
    search_date_to="2025-05-19T00:00:00.000Z",
    search_license="CC-BY-4.0",
    category_ids=["605c72ef153207001f6470d4"]  # Specific chemistry category
)

results = list(client.results(filtered_search))
print(f"Found {len(results)} papers matching criteria")
```

### Retrieving Papers by ID or DOI

```python
import chemrxiv

client = chemrxiv.Client()

# Get paper by ChemRxiv ID
paper_id = "6826a61850018ac7c5739260"
paper = client.item(paper_id)
print(f"Title: {paper.title}")
print(f"Abstract: {paper.abstract[:200]}...")

# Get paper by DOI
doi = "10.26434/chemrxiv-2025-5j4tn"
paper = client.item_by_doi(doi)
print(f"Title: {paper.title}")
print(f"Authors: {', '.join(str(author) for author in paper.authors)}")
```

### Downloading Papers

Download PDFs directly from search results or individual papers:

```python
import chemrxiv

client = chemrxiv.Client()
search = chemrxiv.Search(term="catalysis", limit=1)
paper = next(client.results(search))

# Download PDF with default filename
paper.download_pdf()

# Download PDF with custom filename
paper.download_pdf(filename="my-paper.pdf")

# Download PDF to specific directory
paper.download_pdf(dirpath="./downloads", filename="catalysis-paper.pdf")
```

### Exploring Categories and Licenses

```python
import chemrxiv

client = chemrxiv.Client()

# Get all available categories
categories = client.categories()
print(f"Available categories ({len(categories)}):")
for category in categories[:5]:  # Show first 5
    print(f"- {category.name} (ID: {category.id})")
    if category.description:
        print(f"  Description: {category.description}")
    if category.count:
        print(f"  Papers: {category.count}")

# Get all available licenses
licenses = client.licenses()
print(f"\\nAvailable licenses ({len(licenses)}):")
for license in licenses:
    print(f"- {license.name} (ID: {license.id})")
    if license.url:
        print(f"  URL: {license.url}")
```

**Note on licenses:** There exist different licenses for open source publications determining the downstream use. Please refer to the licenses for details.

### Custom Client Configuration

```python
import chemrxiv

# Create a client with custom settings
custom_client = chemrxiv.Client(
    page_size=50,        # Fetch 50 results per API call
    delay_seconds=1.0,   # Wait 1 second between requests
    num_retries=5        # Retry failed requests up to 5 times
)

# Use custom client for searches
search = chemrxiv.Search(term="organic synthesis", limit=100)
results = list(custom_client.results(search))
print(f"Retrieved {len(results)} papers with custom client")
```

### Debugging with Logging

To inspect network behavior and API interactions:

```python
import logging
import chemrxiv

# Configure DEBUG-level logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Set ChemRxiv logger to DEBUG
chemrxiv_logger = logging.getLogger("chemrxiv")
chemrxiv_logger.setLevel(logging.DEBUG)

# Now API calls will show detailed logging
client = chemrxiv.Client()
search = chemrxiv.Search(term="catalysis", limit=5)
results = list(client.results(search))
```

## API Reference

### Client

The `Client` class provides a reusable interface for making requests to the ChemRxiv API.

```python
client = chemrxiv.Client(
    page_size=10,        # Number of results per API request (default: 10)
    delay_seconds=0,     # Delay between requests in seconds (default: 0)
    num_retries=3        # Number of retry attempts for failed requests (default: 3)
)
```

**Methods:**

- `results(search)` - Execute a search and return an iterator of Result objects
- `item(item_id)` - Retrieve a specific paper by ChemRxiv ID
- `item_by_doi(doi)` - Retrieve a specific paper by DOI
- `categories()` - Get all available categories
- `licenses()` - Get all available licenses

### Search

The `Search` class defines search parameters for querying ChemRxiv.

```python
search = chemrxiv.Search(
    term="search+keywords",                    # Search term (required)
    limit=10,                                 # Maximum number of results
    sort=chemrxiv.SortCriterion.PUBLISHED_DATE_DESC,  # Sort criterion
    search_date_from="2023-01-01T00:00:00.000Z",      # Start date filter
    search_date_to="2025-12-31T00:00:00.000Z",        # End date filter
    search_license="CC-BY-4.0",                       # License filter
    category_ids=["category_id_1", "category_id_2"]   # Category filters
)
```

**Sort Criteria:**

- `chemrxiv.SortCriterion.PUBLISHED_DATE_DESC` - Newest first
- `chemrxiv.SortCriterion.PUBLISHED_DATE_ASC` - Oldest first
- `chemrxiv.SortCriterion.RELEVANCE` - Most relevant first

### Result

The `Result` class represents a paper from ChemRxiv with metadata and download capabilities.

**Properties:**

- `title` - Paper title
- `authors` - List of author objects
- `abstract` - Paper abstract
- `doi` - Digital Object Identifier
- `id` - ChemRxiv paper ID
- `published_date` - Publication date
- `pdf_url` - Direct URL to PDF
- `categories` - List of associated categories
- `license` - License information

**Methods:**

- `download_pdf(filename=None, dirpath=".")` - Download the paper as PDF
- `download_source(filename=None, dirpath=".")` - Download source files if available

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

This library was created by Magdalena Lederbauer @mlederbauer and heavily inspired by the [arXiV Python Wrapper](https://github.com/lukasschwab/arxiv.py) and the [ChemRxiv Dashboard](https://github.com/chemrxiv-dashboard/chemrxiv-dashboard.github.io/). Thanks to Anamaria Leonescu @analeonescu for the support with accessing the API. Thanks to `fxcoudert` who open sourced the [scripts](https://github.com/fxcoudert/tools/blob/master/chemRxiv/chemRxiv.py) used for accessing the ChemRxiv via the Figshare API. As [ChemRxiv migrated to Open Engage in 2021](https://axial.acs.org/publishing/chemrxiv-open-engage-platform), the script is deprecated and this library is intended to replace and streamline it.
Contributions are welcome! Please feel free to submit a Pull Request.
