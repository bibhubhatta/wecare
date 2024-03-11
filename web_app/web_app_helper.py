import os
from time import sleep

import django

from inventory.item import Item
from inventory.shoprite_api import ShopriteItemApi
from pantry_soft.api import PantrySoftApi
from pantry_soft.credentials import (
    PANTRYSOFT_URL,
    PANTRYSOFT_USERNAME,
    PANTRYSOFT_PASSWORD,
)
from scripts.helpers import get_detailed_description


def add_to_message(add_request, message):
    print(message)
    add_request.message += message + "\n"
    add_request.save()


def item_in_shoprite(shoprite, item_upc) -> bool:
    try:
        shoprite_item = shoprite.get(item_upc)
        return shoprite_item is not None
    except Exception:
        return False


def get_pantry_soft_item(pantry_soft, item_upc) -> bool or Item:
    try:
        pantrysoft_item = pantry_soft.read_item(item_upc)
        return pantrysoft_item
    except ValueError:
        return False


def process_request(add_request, shoprite, pantry_soft):
    upc = add_request.upc

    add_to_message(add_request, "Checking PantrySoft...")
    if item := get_pantry_soft_item(pantry_soft, upc):
        add_request.success = True
        add_to_message(add_request, "Item already in PantrySoft.")
        add_request.item_description = item.description

        if item_in_shoprite(shoprite, upc):
            item_json = shoprite.get_json(upc)
            add_request.item_image_url = item_json["primaryImage"]["default"]
        add_request.save()
        return

    add_to_message(add_request, "Checking Shoprite...")
    if item_in_shoprite(shoprite, upc):
        add_to_message(add_request, "Item found in Shoprite. Adding to PantrySoft...")

        item = shoprite.get(upc)
        item_json = shoprite.get_json(upc)

        item_description = get_detailed_description(item_json)
        item.description = item_description

        pantry_soft.create_item(item)
        add_request.item_description = item_description
        add_request.item_image_url = item_json["primaryImage"]["default"]
        image = shoprite.get_image(upc)

        add_to_message(add_request, "Adding item image to PantrySoft...")
        pantry_soft.add_item_image(upc, image)

        add_request.success = True

        add_to_message(add_request, "Item added to PantrySoft.")

    else:
        add_request.success = False
        add_to_message(add_request, "Item not found in Shoprite.")


def process_manual_request(add_request, pantry_soft):
    add_to_message(add_request, "Checking PantrySoft...")

    upc = add_request.upc
    if item := get_pantry_soft_item(pantry_soft, upc):
        add_request.success = True
        add_to_message(add_request, "Item already in PantrySoft.")
        add_request.item_description = item.description
        add_request.save()
        return

    item = Item(
        upc, add_request.item_name, "Manual Entry", "", 0.0, "Manually added item."
    )
    add_to_message(add_request, "Adding item to PantrySoft...")
    pantry_soft.create_item(item)
    add_to_message(add_request, "Item added to PantrySoft.")
    add_request.item_description = f"{item.description} {add_request.item_name}"
    add_request.success = True
    add_request.save()


def main():
    print("Starting...")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_app.settings")
    django.setup()
    from ui.models import AutoAddRequest, ManualAddRequest

    print("Loading Shoprite API...")
    shoprite = ShopriteItemApi()
    print("Loading PantrySoft API...")
    pantry_soft = PantrySoftApi(
        PANTRYSOFT_URL, PANTRYSOFT_USERNAME, PANTRYSOFT_PASSWORD
    )

    print("Processing requests...")
    while True:
        auto_add_requests = AutoAddRequest.objects.filter(success=None)

        if not auto_add_requests:
            sleep(0.5)
            continue

        print(f"Found {len(auto_add_requests)} requests to process.")

        for add_request in auto_add_requests:
            print(f"Processing request {add_request.id}...")

            # Check if the request is also of type ManualAddRequest
            try:
                manual_add_request = ManualAddRequest.objects.get(pk=add_request.id)
                print(f"Processing manual request {add_request.id}...")
                process_manual_request(manual_add_request, pantry_soft)
                continue
            except ManualAddRequest.DoesNotExist:
                print(f"Processing auto request {add_request.id}...")

            process_request(add_request, shoprite, pantry_soft)
            sleep(0.5)


if __name__ == "__main__":
    main()
