from pantrysoft.credentials import (
    PANTRYSOFT_URL,
    PANTRYSOFT_USERNAME,
    PANTRYSOFT_PASSWORD,
)
from pantrysoft.pantrysoft import PantrySoft


def main():
    pantry_soft = PantrySoft(PANTRYSOFT_URL, PANTRYSOFT_USERNAME, PANTRYSOFT_PASSWORD)
    print(pantry_soft.get_all_items_json())
    print(pantry_soft.get_all_inventory_codes_json())
    print(pantry_soft.get_all_item_types_json())


if __name__ == "__main__":
    main()
