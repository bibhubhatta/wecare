from inventory.item import Item
from inventory.shoprite_api import ShopriteItemApi
from pantry_soft.api import PantrySoftApi


class CommandLineInterface:
    def __init__(self):
        self.shoprite = ShopriteItemApi()
        print("Logging into PantrySoft...")
        self.pantry_soft = PantrySoftApi()

    def item_in_pantry(self, upc: str) -> bool:
        try:
            self.pantry_soft.read_item(upc)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_item_from_input(upc: str) -> Item:
        print("\n")
        name = input(f"Enter name for {upc}: ")
        # Skipping size because it is not necessary for now and slows down the process
        size = 0
        # Skipping category, unit, and description because they are not implemented yet
        category = ""
        unit = ""
        description = ""
        print("\n")

        return Item(upc, name, category, unit, size, description)

    @staticmethod
    def print_item(item: Item):
        print(f"Item: {item.name}\n")

    def run(self):
        while True:
            upc = input("Enter UPC: ")

            if upc.lower().strip() == "no more meat":
                break

            if self.item_in_pantry(upc):
                item = self.pantry_soft.read_item(upc)
                self.print_item(item)
                print("Item found in PantrySoft. Skipping...\n\n")
                continue
            else:
                print("Item not in PantrySoft. Adding...")

            try:
                item = self.shoprite.get(upc)
                self.print_item(item)
                print("Item found in Shoprite.")
            except Exception as e:
                print(f"Item not found in Shoprite. Please add details for {upc}")
                item = self.get_item_from_input(upc)

            print("Creating item in PantrySoft...")
            self.pantry_soft.create_item(item)

            print("Item added to PantrySoft\n\n")


def main():
    cli = CommandLineInterface()
    cli.run()


if __name__ == "__main__":
    main()
