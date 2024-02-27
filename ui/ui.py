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
        name = input(f"Enter name for {upc}: ")
        category = ""  # Skipping category because it is not implemented yet
        unit = ""  # Skipping unit because it is not implemented yet
        size = float(input(f"Enter size for {upc}: "))
        description = ""  # Skipping description because it is not implemented yet
        return Item(upc, name, category, unit, size, description)

    def run(self):
        while True:
            upc = input("Enter UPC: ")

            if upc.lower().strip() == "no more meat":
                break

            if self.item_in_pantry(upc):
                item = self.pantry_soft.read_item(upc)
                print(f"{item.name} found in PantrySoft. Skipping...")
                continue
            else:
                print("Item not in PantrySoft. Adding...")

            try:
                item = self.shoprite.get(upc)
                print(f"Item: {item.name} found in Shoprite")
            except Exception as e:
                print(f"Item not found in Shoprite. Please add details for {upc}")
                item = self.get_item_from_input(upc)

            print(f"Creating {item.name} in PantrySoft")
            self.pantry_soft.create_item(item)

            print(f"Item {item.name} added to PantrySoft\n\n")


def main():
    cli = CommandLineInterface()
    cli.run()


if __name__ == "__main__":
    main()
