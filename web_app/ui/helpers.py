from enum import Enum
from functools import cache

from inventory.item import Item
from inventory.shoprite_api import ShopriteItemApi
from pantry_soft.api import PantrySoftApi
from scripts.helpers import get_detailed_description


def item_in_pantry(pantry_soft: PantrySoftApi, upc: str) -> bool:
    try:
        pantry_soft.read_item(upc)
        return True
    except ValueError:
        return False


def item_in_shoprite(shoprite: ShopriteItemApi, upc: str) -> bool:
    try:
        shoprite.get(upc)
        return True
    except Exception:
        return False


class AddItemResult(Enum):
    ITEM_ALREADY_EXISTS = 1
    ITEM_ADDED = 2
    ITEM_NOT_FOUND = 3


def add_item_to_pantry(
    pantry_soft: PantrySoftApi, shoprite: ShopriteItemApi, upc: str
) -> AddItemResult:

    if item_in_pantry(pantry_soft, upc):
        return AddItemResult.ITEM_ALREADY_EXISTS

    # Get item from Shoprite
    try:
        item = shoprite.get(upc)
        description = get_item_description(shoprite, upc)
        item.description = description
    except Exception:
        return AddItemResult.ITEM_NOT_FOUND

    # Add item to PantrySoft
    try:
        pantry_soft.create_item(item)
    except ValueError:
        return AddItemResult.ITEM_NOT_FOUND

    # Add image to PantrySoft
    pantry_soft.add_item_image(upc, shoprite.get_image(upc))
    return AddItemResult.ITEM_ADDED


def add_item_to_pantry_manual(pantry_soft: PantrySoftApi, upc: str, name: str) -> bool:

    item = Item(upc, name, "", "", 0, "Item added manually")
    try:
        pantry_soft.create_item(item)
    except ValueError:
        return False

    return True


@cache
def get_item_description(shoprite: ShopriteItemApi, upc: str) -> str:
    item_json = shoprite.get_json(upc)
    return get_detailed_description(item_json)


@cache
def get_item_image_url(shoprite: ShopriteItemApi, upc: str) -> str:
    item_json = shoprite.get_json(upc)
    return item_json["primaryImage"]["default"]
