from foodpantry.item import Item
from foodpantry.pantry import PantryApi

from pantrysoft.pantrysoft import PantrySoft


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
            item_description = self.__pantry_soft.get_item_description(upc)
            return Item(
                upc,
                name=pantry_soft_item["name"],
                category=pantry_soft_item["itemTypeString"],
                unit=pantry_soft_item["unit"],
                size=float(pantry_soft_item["weight"]),
                description=item_description,
            )

        except ValueError:
            raise ValueError(f"Item with UPC {upc} not found in the pantry")

    def read_all_items(self) -> list[Item]:
        """
        Retrieve all items from the pantry.

        Returns:
        list[Item]: The retrieved items.
        """
        pantry_soft_items = self.__pantry_soft.get_all_items_json()["data"]
        items = []
        for pantry_soft_item in pantry_soft_items:
            items.append(
                Item(
                    pantry_soft_item["itemNumber"],
                    name=pantry_soft_item["name"],
                    category=pantry_soft_item["itemTypeString"],
                    unit=pantry_soft_item["unit"],
                    size=float(pantry_soft_item["weight"]),
                    description="",  # description is not available directly from the json response
                )
            )
        return items

    def create_item(self, item: Item) -> None:
        """
        Set an item in the pantry.

        Parameters:
        - item (Item): The item to set in the pantry.
        """

        if item.category == "":
            raise ValueError("Item category cannot be empty")

        try:
            self.read_item(item.upc)
        except ValueError:
            self.__pantry_soft.add_item(
                item_number=item.upc,
                name=item.name,
                size=item.size,
                description=item.description,
                item_type=item.category,
            )
            return

        raise ValueError(f"Item with UPC {item.upc} already exists in the pantry")

    def update_item(self, item: Item) -> None:
        """
        Update an item in the pantry.

        Parameters:
        - item (Item): The item to update in the pantry.
        """
        if item.category == "":
            raise ValueError("Item category cannot be empty")

        try:
            pantry_soft_item = self.__pantry_soft.get_item(item.upc)
            self.__pantry_soft.update_item(
                pantry_soft_item,
                name=item.name,
                size=item.size,
                description=item.description,
                item_type=item.category,
            )
        except ValueError:
            raise ValueError(f"Item with UPC {item.upc} not found in the pantry")

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

    def create_item_category(self, category: str) -> None:
        """
        Create a new category in the pantry.

        Parameters:
        - category (str): The category to create.
        """
        try:
            self.__pantry_soft.get_item_type_id(category)
        except ValueError:
            self.__pantry_soft.create_item_type(category)
            return

        raise ValueError(f"Category {category} already exists in the pantry")

    def read_all_categories(self) -> list[str]:
        """
        Retrieve all categories from the pantry.

        Returns:
        list[str]: The retrieved categories.
        """
        pantry_soft_categories = self.__pantry_soft.get_all_item_types_json()["data"]
        categories = []
        for pantry_soft_category in pantry_soft_categories:
            categories.append(pantry_soft_category["name"])
        return categories

    def delete_item_category(self, category: str) -> None:
        """
        Delete all items from the pantry with a given category.

        Parameters:
        - category (str): The category of the items to delete.
        """
        try:
            item_type_id = self.__pantry_soft.get_item_type_id(category)
            self.__pantry_soft.delete_item_type(item_type_id)
        except ValueError:
            raise ValueError(f"No items found in the pantry with category {category}")

    def add_item_image(self, upc: str, image: bytes) -> None:
        """
        Add image to an item in the pantry.
        Existing image will be overwritten.

        Parameters:
        - upc (str): The Universal Product Code of the item to upload an image for.
        - image_path (str): The path to the image file to upload.
        """

        try:
            pantry_soft_item = self.__pantry_soft.get_item(upc)
            self.__pantry_soft.add_item_image(pantry_soft_item, image)
        except ValueError:
            raise ValueError(f"Item with UPC {upc} not found in the pantry")
