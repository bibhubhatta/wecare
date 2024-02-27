from inventory.item import Item
from pantry_soft.api import PantrySoftApi


def test_api_gets_item():
    test_item = Item(
        upc="044000882105",
        name="RITZ Peanut Butter Sandwich Crackers, 8 - 1.38 oz Snack Packs",
        category="Food",
        unit="Ounces",
        size=11.04,
        description=""
    )

    api = PantrySoftApi()
    returned_item = api.read_item(test_item.upc)

    assert test_item.upc == returned_item.upc
    assert test_item.name == returned_item.name
    assert test_item.category == returned_item.category
    assert test_item.unit == returned_item.unit
    assert test_item.size == returned_item.size
    assert test_item.description == returned_item.description
