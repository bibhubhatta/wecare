from inventory.item import Item
from inventory.shoprite_api import ShopriteItemApi


def test_gets_item():
    test_item = Item(
        upc="070275000098",
        name="Whink Rust Stain Remover, 16 fl oz",
        category="Surface Cleaners",
        unit="Ounce",
        size=16.0,
        description="Whink Rust Stain Remover, 16 fl oz"
    )

    api = ShopriteItemApi()
    returned_item = api.get(test_item.upc)

    assert test_item.upc == returned_item.upc
    assert test_item.name == returned_item.name
    assert test_item.category == returned_item.category
    assert test_item.unit == returned_item.unit
    assert test_item.size == returned_item.size
    assert test_item.description == returned_item.description
