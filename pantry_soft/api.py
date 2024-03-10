from inventory.item import Item
from inventory.pantry import PantryApi

from pantry_soft.pantrysoft import PantrySoft


class PantrySoftApi(PantryApi):
    """PantrySoft API for interacting with the pantry."""

    def __init__(self, url: str, username: str, password: str):
        """Initialize a PantrySoftApi object."""
        self.__pantry_soft = PantrySoft(url, username, password)

    def read_item(self, upc: str) -> Item:
        """
        Retrieve an item from the pantry.

        Parameters:
        - upc (str): The Universal Product Code of the item to retrieve.

        Returns:
        Item: The retrieved item object.
        """

        inventory_codes_json = self.__pantry_soft.get_all_inventory_codes_json()
        inventory_items_json = self.__pantry_soft.get_all_items_json()

        for item_code_data in inventory_codes_json["data"]:
            if item_code_data["codeNumber"] == upc:
                for item in inventory_items_json["data"]:
                    if item["id"] == item_code_data["itemId"]:
                        return Item(
                            upc,
                            name=item["name"],
                            category=item["itemTypeString"],
                            unit=item["unit"],
                            size=float(item["weight"]),
                            description="",  # description is not available directly from the json response
                        )

        raise ValueError(f"Item with UPC {upc} not found in the pantry")

    def create_item(self, item: Item) -> None:
        """
        Set an item in the pantry.

        Parameters:
        - item (Item): The item to set in the pantry.
        """
        try:
            self.read_item(item.upc)
            raise ValueError(f"Item with UPC {item.upc} already exists in the pantry")
        except ValueError:
            self.__pantry_soft.add_item(
                item_number=item.upc,
                name=item.name,
                size=item.size,
                description=item.description,
            )

    def update_item(self, item: Item) -> None:
        """
        Update an item in the pantry.

        Parameters:
        - item (Item): The item to update in the pantry.
        """
        raise NotImplementedError("PantrySoft API does not support updating items")

    def delete_item(self, upc: str) -> None:
        """
        Delete an item from the pantry.

        Parameters:
        - upc (str): The Universal Product Code of the item to delete.
        """
        inventory_codes_json = self.__pantry_soft.get_all_inventory_codes_json()
        inventory_items_json = self.__pantry_soft.get_all_items_json()

        for item_code_data in inventory_codes_json["data"]:
            if item_code_data["codeNumber"] == upc:
                for item in inventory_items_json["data"]:
                    if item["id"] == item_code_data["itemId"]:
                        self.__pantry_soft.delete_item(item["id"])
                        return

        raise ValueError(f"Item with UPC {upc} not found in the pantry")
