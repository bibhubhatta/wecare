from abc import ABC, abstractmethod


class Item:
    """Class representing an item."""

    def __init__(
        self,
        upc: str,
        name: str,
        category: str,
        unit: str,
        size: float,
        description: str,
    ):
        """
        Initialize an Item object.

        Parameters:
        - upc (str): The Universal Product Code of the item.
        - name (str): The name of the item.
        - category (str): The category of the item.
        - unit (str): The unit of measurement for the item.
        - size (float): The size or quantity of the item.
        - description (str): Description of the item.
        """
        self.upc = upc
        self.name = name
        self.category = category
        self.unit = unit
        self.size = size
        self.description = description


class ItemApi(ABC):
    """Abstract base class representing an Item API."""

    @abstractmethod
    def get(self, upc: str) -> Item:
        """
        Abstract method to retrieve an item by UPC.

        Parameters:
        - upc (str): The Universal Product Code of the item to retrieve.

        Returns:
        Item: The retrieved item object.
        """
        pass
