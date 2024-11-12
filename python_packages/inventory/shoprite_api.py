from functools import cache
from typing import Any, Dict

import requests

from inventory.item import Item, ItemApi


class ShopriteItemApi(ItemApi):
    """Shoprite API for retrieving item data."""

    def __init__(self):
        """Initialize a ShopriteItemApi object."""
        headers = {"x-site-host": "https://www.shoprite.com"}
        self.endpoint = (
            "https://storefrontgateway.brands.wakefern.com/api/stores/3000/products/"
        )
        self.client = requests.Session()
        self.client.headers.update(headers)

    @cache
    def get_json(self, upc: str) -> Dict[str, Any]:
        """
        Retrieve item data in JSON format from the Shoprite API.

        Parameters:
        - upc (str): The Universal Product Code of the item to retrieve.

        Returns:
        Dict[str, Any]: The retrieved item data in JSON format.
        """
        endpoint = f"{self.endpoint}{upc.zfill(14)}"
        response = self.client.get(endpoint)
        response.raise_for_status()
        return response.json()

    def get(self, upc: str) -> Item:
        """
        Retrieve an item from the Shoprite API.

        Parameters:
        - upc (str): The Universal Product Code of the item to retrieve.

        Returns:
        Item: The retrieved item object.
        """
        json_data = self.get_json(upc)
        name = json_data["name"]
        category = json_data["defaultCategory"]
        unit = json_data["unitsOfSize"]["label"]
        size = json_data["unitsOfSize"]["size"]
        description = json_data["description"]
        return Item(upc, name, category, unit, size, description)

    def get_image(self, upc: str) -> bytes:
        """
        Retrieve an item image from the Shoprite API.

        Parameters:
        - upc (str): The Universal Product Code of the item to retrieve.

        Returns:
        bytes: The retrieved item image.
        """
        json_data = self.get_json(upc)
        image_url = json_data["primaryImage"]["default"]
        response = self.client.get(image_url)
        response.raise_for_status()
        return response.content
