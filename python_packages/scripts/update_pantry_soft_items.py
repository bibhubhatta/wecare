from inventory.shoprite_api import ShopriteItemApi
from pantry_soft.api import PantrySoftApi
from pantry_soft.credentials import (
    PANTRYSOFT_URL,
    PANTRYSOFT_USERNAME,
    PANTRYSOFT_PASSWORD,
)
from scripts.helpers import get_detailed_description


def main():
    print("Starting PantrySoft...")
    pantry_soft = PantrySoftApi(
        PANTRYSOFT_URL, PANTRYSOFT_USERNAME, PANTRYSOFT_PASSWORD
    )
    shoprite = ShopriteItemApi()

    print("Getting all items from PantrySoft...")
    for item in reversed(pantry_soft.read_all_items()):
        if not item.upc:
            continue
        try:
            item = shoprite.get(item.upc)
            item_json = shoprite.get_json(item.upc)
            detailed_description = get_detailed_description(item_json)
            item.description = detailed_description
            pantry_soft.update_item(item)
            image = shoprite.get_image(item.upc)

            print(f"Updating data for {item.upc} {item.name}")
            pantry_soft.update_item(item)
            print(f"Updated data for {item.upc} {item.name}")

            print(f"Adding image for {item.upc} {item.name}")
            pantry_soft.add_item_image(item.upc, image)
            print(f"Added image for {item.upc} {item.name}")

        except Exception as e:
            print(f"Error updating data and image for {item.upc}: {e}")


if __name__ == "__main__":
    main()
