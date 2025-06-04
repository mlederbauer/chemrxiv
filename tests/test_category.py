"""Tests for the Category class."""

from chemrxiv.category import Category


def test_category_creation():
    """Test basic category creation."""
    category = Category("cat1", "Organic Chemistry")
    assert category.id == "cat1"
    assert category.name == "Organic Chemistry"
    assert category.description is None
    assert category.count is None
    assert category.parent_id is None


def test_category_with_optional_fields():
    """Test category creation with optional fields."""
    category = Category(
        "cat2",
        "Inorganic Chemistry",
        description="Study of inorganic compounds",
        count=100,
        parent_id="cat1",
    )
    assert category.id == "cat2"
    assert category.name == "Inorganic Chemistry"
    assert category.description == "Study of inorganic compounds"
    assert category.count == 100
    assert category.parent_id == "cat1"


def test_category_from_api_response():
    """Test creating category from API response."""
    data = {
        "id": "cat3",
        "name": "Physical Chemistry",
        "description": "Study of physical principles",
        "count": 50,
        "parentId": "cat1",
    }
    category = Category.from_api_response(data)
    assert category.id == "cat3"
    assert category.name == "Physical Chemistry"
    assert category.description == "Study of physical principles"
    assert category.count == 50
    assert category.parent_id == "cat1"


def test_category_string_representation():
    """Test string representation of category."""
    category = Category("cat1", "Organic Chemistry")
    assert str(category) == "Organic Chemistry"
    assert repr(category) == "Category(id='cat1', name='Organic Chemistry')"
