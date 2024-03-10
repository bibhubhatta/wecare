import pytest

from inventory.item import Item
from pantry_soft.api import PantrySoftApi
from pantry_soft.credentials import (
    PANTRYSOFT_URL,
    PANTRYSOFT_USERNAME,
    PANTRYSOFT_PASSWORD,
)


class TestPantrySoftApi:
    api = PantrySoftApi(PANTRYSOFT_URL, PANTRYSOFT_USERNAME, PANTRYSOFT_PASSWORD)

    def test_api_gets_item(self):
        test_item = Item(
            upc="99999999999",
            name="Test Item 9 -- Will be deleted",
            category="",  # Category is not implemented yet
            unit="",  # Unit is not implemented yet
            size=99.99,
            description="",  # description blank because adding description is not yet implemented
        )

        self.api.create_item(test_item)

        returned_item = self.api.read_item(test_item.upc)

        assert returned_item.upc == test_item.upc
        assert returned_item.name == test_item.name
        assert returned_item.size == test_item.size

        self.api.delete_item(test_item.upc)

    def test_api_creates_item(self):
        test_item = Item(
            upc="88888888888",
            name="Test Item 8 -- Will be deleted",
            category="",  # Category is not implemented yet
            unit="",  # Unit is not implemented yet
            size=88.88,
            description="lol",  # description blank because adding description is not yet implemented
        )

        self.api.create_item(test_item)

        returned_item = self.api.read_item(test_item.upc)

        assert returned_item.upc == test_item.upc
        assert returned_item.name == test_item.name
        assert returned_item.size == test_item.size

        self.api.delete_item(test_item.upc)

    def test_api_deletes_item(self):
        test_item = Item(
            upc="000000000000",
            name="One Piece",
            category="",  # Category is not implemented yet
            unit="",  # Unit is not implemented yet
            size=1.11111,
            description="lol",  # description blank because adding description is not yet implemented
        )

        self.api.create_item(test_item)

        returned_item = self.api.read_item(test_item.upc)

        assert returned_item.upc == test_item.upc

        self.api.delete_item(test_item.upc)

        with pytest.raises(ValueError):
            self.api.read_item(test_item.upc)
