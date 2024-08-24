from selenium.webdriver.common.by import By

from pantry_soft.credentials import (
    PANTRYSOFT_URL,
    PANTRYSOFT_USERNAME,
    PANTRYSOFT_PASSWORD,
)
from pantry_soft.driver import PantrySoftDriver
from pantry_soft.pantrysoft import PantrySoft
from scripts.helpers import is_valid_upc


def main():
    deactivator = Deactivator(PANTRYSOFT_URL, PANTRYSOFT_USERNAME, PANTRYSOFT_PASSWORD)
    pantry_soft = PantrySoft(PANTRYSOFT_URL, PANTRYSOFT_USERNAME, PANTRYSOFT_PASSWORD)

    all_items = pantry_soft.get_all_items_json()["data"]

    for item in all_items:
        if not item["isActive"]:
            continue

        if is_valid_upc(item["itemNumber"]):
            continue

        deactivator.deactivate_item(item)
        print(f"Deactivated item {item['itemNumber']}: {item['name']}")


class Deactivator:
    def __init__(self, url: str, username: str, password: str):
        self.driver = PantrySoftDriver(url, username, password)

    def deactivate_item(self, item):
        item_id = item["id"]
        self.driver.driver.get(f"https://app.pantrysoft.com/inventoryitem/{item_id}/edit")

        is_active_checkbox = self.driver.driver.find_element(By.ID, "pantrybundle_inventoryitem_isActive")

        if not is_active_checkbox.is_selected():
            return

        is_active_checkbox.click()

        # Find the submit button and click on it
        self.driver.driver.find_element(
            By.XPATH,
            "//button[@class='btn btn-default' and @type='submit']"
        ).click()

        # Wait for the page to load
        self.driver.driver.implicitly_wait(10)


if __name__ == "__main__":
    main()
