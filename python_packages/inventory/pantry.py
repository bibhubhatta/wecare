from abc import ABC, abstractmethod

from inventory.item import Item


class PantryApi(ABC):
    """Abstract base class representing a Pantry API."""

    @abstractmethod
    def read_item(self, upc: str) -> Item:
        """
        Abstract method to retrieve an item by UPC.

        Parameters:
        - upc (str): The Universal Product Code of the item to retrieve.

        Returns:
        Item: The retrieved item object.
        """
        pass

    @abstractmethod
    def create_item(self, item: Item) -> None:
        """
        Abstract method to set an item in the pantry.

        Parameters:
        - item (Item): The item to set in the pantry.
        """
        pass

    @abstractmethod
    def update_item(self, item: Item) -> None:
        """
        Abstract method to update an item in the pantry.

        Parameters:
        - item (Item): The item to update in the pantry.
        """
        pass

    @abstractmethod
    def delete_item(self, upc: str) -> None:
        """
        Abstract method to delete an item from the pantry.

        Parameters:
        - upc (str): The Universal Product Code of the item to delete.
        """
        pass
