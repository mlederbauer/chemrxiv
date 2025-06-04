"""Tests for the License class."""

from chemrxiv.license import License


def test_license_creation():
    """Test basic license creation."""
    license = License("cc-by", "Creative Commons Attribution")
    assert license.id == "cc-by"
    assert license.name == "Creative Commons Attribution"
    assert license.description is None
    assert license.url is None


def test_license_with_optional_fields():
    """Test license creation with optional fields."""
    license = License(
        "cc-by-nc",
        "Creative Commons Attribution-NonCommercial",
        description="Allows reuse with attribution, no commercial use",
        url="https://creativecommons.org/licenses/by-nc/4.0/",
    )
    assert license.id == "cc-by-nc"
    assert license.name == "Creative Commons Attribution-NonCommercial"
    assert (
        license.description
        == "Allows reuse with attribution, no commercial use"
    )
    assert license.url == "https://creativecommons.org/licenses/by-nc/4.0/"


def test_license_from_api_response():
    """Test creating license from API response."""
    data = {
        "id": "cc-by-sa",
        "name": "Creative Commons Attribution-ShareAlike",
        "description": "Allows reuse with attribution and share-alike",
        "url": "https://creativecommons.org/licenses/by-sa/4.0/",
    }
    license = License.from_api_response(data)
    assert license.id == "cc-by-sa"
    assert license.name == "Creative Commons Attribution-ShareAlike"
    assert (
        license.description == "Allows reuse with attribution and share-alike"
    )
    assert license.url == "https://creativecommons.org/licenses/by-sa/4.0/"


def test_license_string_representation():
    """Test string representation of license."""
    license = License("cc-by", "Creative Commons Attribution")
    assert str(license) == "Creative Commons Attribution"
    assert (
        repr(license)
        == "License(id='cc-by', name='Creative Commons Attribution')"
    )
