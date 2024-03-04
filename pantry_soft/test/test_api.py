from inventory.item import Item
from pantry_soft.api import PantrySoftApi


class TestPantrySoftApi:
    api = PantrySoftApi()

    def test_api_gets_item(self):
        test_item = Item(
            upc="044000882105",
            name="RITZ Peanut Butter Sandwich Crackers, 8 - 1.38 oz Snack Packs",
            category="",  # Category is not implemented yet
            unit="",  # Unit is not implemented yet
            size=11.04,
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
            upc="070275000012",
            name="Whink Rust Stain Remover, 16 fl oz",
            category="",  # Category is not implemented yet
            unit="",  # Unit is not implemented yet
            size=16.0,
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

        try:
            self.api.read_item(test_item.upc)
            assert False
        except ValueError:
            assert True
