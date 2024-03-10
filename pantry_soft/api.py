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

        try:
            pantry_soft_item = self.__pantry_soft.get_item(upc)
            return Item(
                upc,
                name=pantry_soft_item["name"],
                category=pantry_soft_item["itemTypeString"],
                unit=pantry_soft_item["unit"],
                size=float(pantry_soft_item["weight"]),
                description="",  # description is not available directly from the json response
            )

        except ValueError:
            raise ValueError(f"Item with UPC {upc} not found in the pantry")

    def create_item(self, item: Item) -> None:
        """
        Set an item in the pantry.

        Parameters:
        - item (Item): The item to set in the pantry.
        """
        try:
            self.read_item(item.upc)
        except ValueError:
            self.__pantry_soft.add_item(
                item_number=item.upc,
                name=item.name,
                size=item.size,
                description=item.description,
            )
            return

        raise ValueError(f"Item with UPC {item.upc} already exists in the pantry")

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
        try:
            item_id = self.__pantry_soft.get_item_id(upc)
            self.__pantry_soft.delete_item(item_id)
        except ValueError:
            raise ValueError(f"Item with UPC {upc} not found in the pantry")

    def add_item_image(self, upc: str, image_path: str) -> None:
        """
        Add image to an item in the pantry.
        Existing image will be overwritten.

        Parameters:
        - upc (str): The Universal Product Code of the item to upload an image for.
        - image_path (str): The path to the image file to upload.
        """

        try:
            pantry_soft_item = self.__pantry_soft.get_item(upc)
            self.__pantry_soft.add_item_image(pantry_soft_item, image_path)
        except ValueError:
            raise ValueError(f"Item with UPC {upc} not found in the pantry")
