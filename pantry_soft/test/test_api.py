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
    one_piece = Item(
        upc="000000000000",
        name="One Piece",
        category="Anime",
        unit="",  # Unit is not implemented yet
        size=1.11111,
        description="",  # description blank because adding description is not yet implemented
    )

    def test_api_gets_item(self):
        test_item = Item(
            upc="99999999999",
            name="Test Item 9 -- Will be deleted",
            category="Test Category 9",
            unit="",  # Unit is not implemented yet
            size=99.99,
            description="",  # description blank because adding description is not yet implemented
        )

        self.api.create_item(test_item)
        returned_item = self.api.read_item(test_item.upc)
        self.api.delete_item(test_item.upc)
        self.api.delete_item_category(test_item.category)

        assert returned_item.upc == test_item.upc
        assert returned_item.name == test_item.name
        assert returned_item.size == test_item.size
        assert returned_item.category == test_item.category

    def test_api_creates_item(self):
        test_item = Item(
            upc="88888888888",
            name="Test Item 8 -- Will be deleted",
            category="Test Category 8",
            unit="",  # Unit is not implemented yet
            size=88.88,
            description="lol",  # description blank because adding description is not yet implemented
        )

        self.api.create_item(test_item)
        returned_item = self.api.read_item(test_item.upc)
        self.api.delete_item(test_item.upc)
        self.api.delete_item_category(test_item.category)

        assert returned_item.upc == test_item.upc
        assert returned_item.name == test_item.name
        assert returned_item.size == test_item.size
        assert returned_item.category == test_item.category

    def test_api_deletes_item(self):
        test_item = self.one_piece

        self.api.create_item(test_item)
        returned_item = self.api.read_item(test_item.upc)
        self.api.delete_item(test_item.upc)
        self.api.delete_item_category(test_item.category)

        assert returned_item.upc == test_item.upc

        with pytest.raises(ValueError):
            self.api.read_item(test_item.upc)

    def test_api_duplicate_item(self):
        test_item = self.one_piece

        self.api.create_item(test_item)
        with pytest.raises(ValueError):
            self.api.create_item(test_item)
        self.api.delete_item(test_item.upc)
        self.api.delete_item_category(test_item.category)

    def test_image_upload(self):
        test_item = self.one_piece

        self.api.create_item(test_item)
        self.api.add_item_image(test_item.upc, open("meat.jpg", "rb").read())
        self.api.delete_item(test_item.upc)

    def test_api_creates_category(self):
        test_category = "Test Category 7"

        self.api.create_item_category(test_category)
        all_categories = self.api.read_all_categories()
        self.api.delete_item_category(test_category)

        assert test_category in all_categories

    def test_api_deletes_category(self):
        test_category = "Test Category 6"

        self.api.create_item_category(test_category)
        all_categories_before = self.api.read_all_categories()
        self.api.delete_item_category(test_category)
        all_categories_after = self.api.read_all_categories()

        assert test_category in all_categories_before
        assert test_category not in all_categories_after
