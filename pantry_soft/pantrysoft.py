import time
from time import sleep

import requests
from bs4 import BeautifulSoup

from inventory.item import Item
from pantry_soft.driver import PantrySoftDriver


class PantrySoft:
    """PantrySoft API for retrieving item data."""

    def __init__(self, url: str, username: str, password: str):
        """Initialize a PantrySoft object."""
        self.driver = PantrySoftDriver(url, username, password)
        self.php_session = self.driver.get_php_session()

    def _get_request_params(self) -> dict:
        """Generate common request parameters."""
        return {
            "cookies": {"PHPSESSID": self.php_session},
            "headers": {
                "authority": "app.pantrysoft.com",
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-language": "en-US,en;q=0.9",
                "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        }

    def _make_get_request(self, endpoint: str, indexdata: str) -> dict:
        """Make a GET request to the PantrySoft API."""
        params = self._get_request_params()
        params["params"] = {"_": str(int(time.time() * 1000))}
        response = requests.get(
            f"https://app.pantrysoft.com/{endpoint}/{indexdata}", **params
        )
        return response.json()

    def get_all_items_json(self) -> dict:
        """Return the JSON response for all items."""
        return self._make_get_request("inventoryitem", "indexdata")

    def get_all_inventory_codes_json(self) -> dict:
        """Return the JSON response for all inventory codes."""
        return self._make_get_request("inventory_code", "indexData")

    def get_all_item_types_json(self) -> dict:
        """Return the JSON response for all item types."""
        return self._make_get_request("inventoryitemtype", "indexdata")

    def get_all_item_tags_json(self) -> dict:
        """Return the JSON response for all item tags."""
        return self._make_get_request("inventoryitemtag", "indexdata")

    def add_item(self, item: Item) -> None:
        """Add an item to the PantrySoft inventory."""
        self.driver.add_item(item)
        sleep(1)
        self.driver.link_code_to_item(item)

    def delete_item(self, item_id: int) -> None:
        """Delete an item from the PantrySoft inventory."""
        params = self._get_request_params()
        response = requests.get("https://app.pantrysoft.com/inventoryitem/", **params)
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("generic-delete-modal").get("csrf-token")
        data = {"_method": "DELETE", "csrfToken": csrf_token}
        requests.post(
            f"https://app.pantrysoft.com/inventoryitem/delete/{item_id}",
            **params,
            data=data,
        )
