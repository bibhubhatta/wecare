import json
import time
from functools import cache

import requests
from bs4 import BeautifulSoup
from requests import JSONDecodeError

from pantry_soft.driver import PantrySoftDriver


class PantrySoft:
    """PantrySoft API for retrieving item data."""

    def __init__(self, url: str, username: str, password: str):
        """Initialize a PantrySoft object."""
        self.url = url

        self._cookies = self._get_cookies(username, password)
        self._headers = self._get_default_headers()

        self.last_item_changed = time.time()

    def _get_cookies(self, username: str, password: str) -> dict:
        """
        Returns the cookies for the PantrySoft API.

        Cookies are retrieved by logging into the PantrySoft website and extracting the PHP session ID.
        """

        # Check if the cookie is cached
        try:
            with open("cookies.json", "r") as f:
                cookies_dict = json.loads(f.read())

            # Check if the cookies are still valid
            if cookies_dict["expiry"] > time.time():
                return {"PHPSESSID": cookies_dict["PHPSESSID"]}
        except FileNotFoundError:
            pass

        # Get the cookies by logging in
        driver = PantrySoftDriver(self.url, username, password)
        php_session = driver.get_php_session()
        php_session_expiry = driver.get_php_session_expiry()
        driver.driver.quit()

        # Cache the cookie for future use
        cookies_dict = {
            "user": username,
            "PHPSESSID": php_session,
            "expiry": php_session_expiry,
        }

        with open("cookies.json", "w") as f:
            f.write(json.dumps(cookies_dict))

        return {"PHPSESSID": php_session}

    @staticmethod
    def _get_default_headers() -> dict:
        """Generate common request parameters."""
        return {
            "authority": "app.pantrysoft.com",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

    def _get_json(self, endpoint: str, indexdata: str = "indexdata") -> dict:
        """Make a GET request to the PantrySoft API."""
        params = {"_": str(int(time.time() * 1000))}
        response = requests.get(
            f"{self.url}/{endpoint}/{indexdata}",
            headers=self._headers,
            cookies=self._cookies,
            params=params,
        )
        return response.json()

    @cache
    def _get_all_items_json_cached(self, last_item_changed: float) -> dict:
        """Return the JSON response for all items."""
        return self._get_json("inventoryitem")

    def get_all_items_json(self) -> dict:
        """Return the JSON response for all items."""
        return self._get_all_items_json_cached(self.last_item_changed)

    def get_all_inventory_codes_json(self) -> dict:
        """Return the JSON response for all inventory codes."""
        return self._get_json("inventory_code", "indexData")

    def get_all_item_types_json(self) -> dict:
        """Return the JSON response for all item types."""
        return self._get_json("inventoryitemtype")

    def get_all_item_tags_json(self) -> dict:
        """Return the JSON response for all item tags."""
        return self._get_json("inventoryitemtag")

    def add_item(
        self, item_number: str, name: str, size: float, description: str
    ) -> None:
        """Create an item in the PantrySoft inventory and link item number as its code."""
        self._create_item(item_number, name, size, description)
        self._link_code_to_item(
            item_number=item_number, name=name, code_number=item_number
        )

    def _create_item(
        self, item_number: str, name: str, weight: float, description: str
    ) -> None:
        """Create an item in the PantrySoft inventory."""

        # Get the CSRF token
        response = requests.get(
            f"{self.url}/inventoryitem/new",
            headers=self._headers,
            cookies=self._cookies,
        )
        soup = BeautifulSoup(response.text, "html.parser")
        form_token = soup.find(
            "input", {"id": "pantrybundle_inventoryitem__token"}
        ).get("value")

        # Send the create request
        data = {
            "pantrybundle_inventoryitem[name]": name,
            "pantrybundle_inventoryitem[itemNumber]": item_number,
            "pantrybundle_inventoryitem[inventoryItemType]": "1",
            "pantrybundle_inventoryitem[unit]": "Ounces",
            "pantrybundle_inventoryitem[value]": "0.00",
            "pantrybundle_inventoryitem[weight]": str(weight),
            "pantrybundle_inventoryitem[outOfStockThreshold]": "0.00",
            "pantrybundle_inventoryitem[isActive]": "1",
            "pantrybundle_inventoryitem[isVisit]": "1",
            "pantrybundle_inventoryitem[isKiosk]": "1",
            "pantrybundle_inventoryitem[isStore]": "1",
            "pantrybundle_inventoryitem[backgroundColor]": "",
            "pantrybundle_inventoryitem[symbolType]": "",
            "fileupload": "",
            "pantrybundle_inventoryitem[description]": description,
            "pantrybundle_inventoryitem[icon]": "",
            "pantrybundle_inventoryitem[imageUploadId]": "",
            "pantrybundle_inventoryitem[_token]": form_token,
        }
        requests.post(
            f"{self.url}/inventoryitem/new",
            headers=self._headers,
            cookies=self._cookies,
            data=data,
        )

        self.last_item_changed = time.time()

    def get_item(self, item_number: str) -> dict:
        """Get the PantrySoft item with the given item number."""
        all_items = self.get_all_items_json()["data"]

        item_id = None
        # Iterating in reverse because it is more likely that the item was added recently
        for pantry_soft_item in reversed(all_items):
            if pantry_soft_item["itemNumber"] == item_number:
                return pantry_soft_item

        if not item_id:
            raise ValueError(
                f"Item with item number {item_number} not found in PantrySoft"
            )

    def get_item_id(self, item_number: str) -> int:
        """Get the PantrySoft item ID with the given item number."""
        return self.get_item(item_number)["id"]

    def _link_code_to_item(self, item_number: str, name: str, code_number: str) -> None:
        """Links item code to item in the PantrySoft inventory."""

        # Check if the item exists in PantrySoft
        try:
            item_id = self.get_item_id(item_number)
        except ValueError:
            raise ValueError(
                f"Item with item number {item_number} not found in PantrySoft"
            )

        # Get the CSRF token
        response = requests.get(
            f"{self.url}/inventory_code/new",
            headers=self._headers,
            cookies=self._cookies,
        )
        soup = BeautifulSoup(response.text, "html.parser")
        form_token = soup.find(
            "input", {"id": "pantrybundle_inventoryitemcode__token"}
        ).get("value")

        # Send the link request
        files = {
            "inventoryItem": (None, str(item_id)),
            "pantrybundle_inventoryitemcode[codeNumber]": (None, code_number),
            "pantrybundle_inventoryitemcode[_token]": (None, form_token),
        }
        response = requests.post(
            f"{self.url}/inventory_code/new",
            headers=self._headers,
            cookies=self._cookies,
            files=files,
        )

        # Check if the link was successful
        expected_message = f"Item Code {item_number} for {name} Added"
        try:
            response_json = response.json()
            if response_json["message"] != expected_message:
                raise ValueError(
                    f"Failed to link item code {item_number} to item {name} in PantrySoft. {response_json['message']}"
                )
        except JSONDecodeError:
            raise ValueError(
                f"Failed to link item code {item_number} to item {name} in PantrySoft. {response.text}"
            )

    def delete_item(self, item_id: int) -> None:
        """Delete an item from the PantrySoft inventory."""

        # Get the CSRF token
        response = requests.get(
            f"{self.url}/inventoryitem/",
            headers=self._headers,
            cookies=self._cookies,
        )
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("generic-delete-modal").get("csrf-token")

        # Send the delete request
        data = {"_method": "DELETE", "csrfToken": csrf_token}
        requests.post(
            f"{self.url}/inventoryitem/delete/{item_id}",
            headers=self._headers,
            cookies=self._cookies,
            data=data,
        )

        self.last_item_changed = time.time()
