import time

import requests

from pantry_soft.driver import PantrySoftDriver


class PantrySoft:
    """PantrySoft API for retrieving item data."""

    def __init__(self, url: str, username: str, password: str):
        """Initialize a PantrySoft object."""

        self.driver = PantrySoftDriver(url, username, password)
        self.php_session = self.driver.get_php_session()

    def get_json(self, endpoint: str, indexdata: str):
        """Return the JSON response from the PantrySoft API."""
        cookies = {
            "PHPSESSID": self.php_session,
        }

        headers = {
            "authority": "app.pantrysoft.com",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9",
            "referer": f"https://app.pantrysoft.com/{endpoint}/",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

        params = {
            "_": str(int(time.time() * 1000)),
        }

        response = requests.get(
            f"https://app.pantrysoft.com/{endpoint}/{indexdata}",
            params=params,
            cookies=cookies,
            headers=headers,
        )

        return response.json()

    def get_all_items_json(self) -> dict:
        """Return the JSON response from the PantrySoft API."""
        return self.get_json("inventoryitem", "indexdata")

    def get_all_inventory_codes_json(self) -> dict:
        """Return the JSON response from the PantrySoft API."""
        return self.get_json("inventory_code", "indexData")

    def get_all_item_types_json(self) -> dict:
        """Return the JSON response from the PantrySoft API."""
        return self.get_json("inventoryitemtype", "indexdata")

    def get_all_item_tags_json(self) -> dict:
        """Return the JSON response from the PantrySoft API."""
        return self.get_json("inventoryitemtag", "indexdata")
