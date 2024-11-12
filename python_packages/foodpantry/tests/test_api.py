import copy
import os

import pytest

from foodpantry.item import Item
from foodpantry.pantrysoft_api import PantrySoftApi
from pantrysoft import (
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
        size=1.11,
        description="The One Piece! The treasure that is worth everything in the world!",
    )

    def test_api_gets_item(self):
        test_item = Item(
            upc="99999999999",
            name="Test Item 9 -- Will be deleted",
            category="Test Category 9",
            unit="",  # Unit is not implemented yet
            size=99.99,
            description="This is a test item and will be deleted.",
        )

        self.api.create_item(test_item)
        returned_item = self.api.read_item(test_item.upc)
        self.api.delete_item(test_item.upc)
        self.api.delete_item_category(test_item.category)

        assert returned_item.upc == test_item.upc
        assert returned_item.name == test_item.name
        assert returned_item.size == test_item.size
        assert returned_item.category == test_item.category
        assert returned_item.description == test_item.description

    def test_api_creates_item(self):
        test_item = Item(
            upc="88888888888",
            name="Test Item 8 -- Will be deleted",
            category="Test Category 8",
            unit="",  # Unit is not implemented yet
            size=88.88,
            description="This is a test item and will be deleted.",
        )

        self.api.create_item(test_item)
        returned_item = self.api.read_item(test_item.upc)
        self.api.delete_item(test_item.upc)
        self.api.delete_item_category(test_item.category)

        assert returned_item.upc == test_item.upc
        assert returned_item.name == test_item.name
        assert returned_item.size == test_item.size
        assert returned_item.category == test_item.category
        assert returned_item.description == test_item.description

    def test_api_updates_item(self):
        test_item = Item(
            upc="77777777777",
            name="Test Item 7 -- Will be deleted",
            category="Test Category 7",
            unit="",  # Unit is not implemented yet
            size=77.77,
            description="This is a test item and will be deleted.",
        )

        self.api.create_item(test_item)
        updated_item = copy.deepcopy(test_item)
        updated_item.name = "Two Piece"
        updated_item.size = 2.22
        updated_item.category = "Manga"
        updated_item.description = (
            "The Two Piece! The treasure that is worth twice the world!"
        )

        self.api.update_item(updated_item)
        returned_item = self.api.read_item(test_item.upc)
        self.api.delete_item(test_item.upc)
        self.api.delete_item_category(test_item.category)

        assert returned_item.upc == updated_item.upc
        assert returned_item.name == updated_item.name
        assert returned_item.size == updated_item.size
        assert returned_item.category == updated_item.category
        assert returned_item.description == updated_item.description

    def test_api_deletes_item(self):
        test_item = Item(
            upc="66666666666",
            name="Test Item 6 -- Will be deleted",
            category="Test Category 6",
            unit="",  # Unit is not implemented yet
            size=66.66,
            description="This is a test item and will be deleted.",
        )

        self.api.create_item(test_item)
        returned_item = self.api.read_item(test_item.upc)
        self.api.delete_item(test_item.upc)
        self.api.delete_item_category(test_item.category)

        assert returned_item.upc == test_item.upc

        with pytest.raises(ValueError):
            self.api.read_item(test_item.upc)

    def test_api_duplicate_item(self):
        test_item = Item(
            upc="55555555555",
            name="Test Item 5 -- Will be deleted",
            category="Test Category 5",
            unit="",  # Unit is not implemented yet
            size=55.55,
            description="This is a test item and will be deleted.",
        )

        self.api.create_item(test_item)
        with pytest.raises(ValueError):
            self.api.create_item(test_item)
        self.api.delete_item(test_item.upc)
        self.api.delete_item_category(test_item.category)

    def test_image_upload(self):
        test_item = Item(
            upc="44444444444",
            name="Test Item 4 -- Will be deleted",
            category="Test Category 4",
            unit="",  # Unit is not implemented yet
            size=44.44,
            description="This is a test item and will be deleted.",
        )

        self.api.create_item(test_item)
        image_path = os.path.join(os.path.dirname(__file__), "meat.jpg")
        self.api.add_item_image(test_item.upc, open(image_path, "rb").read())
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
