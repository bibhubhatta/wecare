from inventory.item import Item
from inventory.shoprite_api import ShopriteItemApi

test_item = Item(
    upc="070275000098",
    name="Whink Rust Stain Remover, 16 fl oz",
    category="Surface Cleaners",
    unit="Ounce",
    size=16.0,
    description="Whink Rust Stain Remover, 16 fl oz",
)


def test_gets_item():
    api = ShopriteItemApi()
    returned_item = api.get(test_item.upc)

    assert test_item.upc == returned_item.upc
    assert test_item.name == returned_item.name
    assert test_item.category == returned_item.category
    assert test_item.unit == returned_item.unit
    assert test_item.size == returned_item.size
    assert test_item.description == returned_item.description


def test_gets_image():
    api = ShopriteItemApi()
    image = api.get_image(test_item.upc)
    assert image == open("test_image_whink_rust_stain_remover.jpg", "rb").read()
