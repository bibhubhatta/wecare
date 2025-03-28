from functools import cache

import requests
import time
from bs4 import BeautifulSoup
from requests import JSONDecodeError

PANTRYSOFT_URL = "https://app.pantrysoft.com"


class PantrySoft:
    """PantrySoft API for retrieving item data."""

    def __init__(self, php_session_id):
        """Initialize a PantrySoft object.
        :param php_session_id:
        """

        self._cookies = {"PHPSESSID": php_session_id}
        self._headers = self._get_default_headers()

        self.last_item_changed = time.time()

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
            f"{PANTRYSOFT_URL}/{endpoint}/{indexdata}",
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
        self, item_number: str, name: str, item_type: str, size: float, description: str
    ) -> None:
        """Create an item in the PantrySoft inventory and link item number as its code."""
        self._create_item(item_number, name, item_type, size, description)
        self._link_code_to_item(
            item_number=item_number, name=name, code_number=item_number
        )

    def _create_item(
        self,
        item_number: str,
        name: str,
        item_type: str,
        weight: float,
        description: str,
    ) -> None:
        """Create an item in the PantrySoft inventory."""

        # Get the CSRF token
        response = requests.get(
            f"{PANTRYSOFT_URL}/inventoryitem/new",
            headers=self._headers,
            cookies=self._cookies,
        )
        soup = BeautifulSoup(response.text, "html.parser")
        form_token = soup.find(
            "input", {"id": "pantrybundle_inventoryitem__token"}
        ).get("value")

        # Check if item type exists
        try:
            item_type_id = self.get_item_type_id(item_type)
        except ValueError:
            self.create_item_type(item_type)
            item_type_id = self.get_item_type_id(item_type)

        # Send the create request
        data = {
            "pantrybundle_inventoryitem[name]": name,
            "pantrybundle_inventoryitem[itemNumber]": item_number,
            "pantrybundle_inventoryitem[inventoryItemType]": str(item_type_id),
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
            f"{PANTRYSOFT_URL}/inventoryitem/new",
            headers=self._headers,
            cookies=self._cookies,
            data=data,
        )

        self.last_item_changed = time.time()

    def get_item(self, item_number: str) -> dict:
        """Get the PantrySoft item with the given item number."""
        all_items = self.get_all_items_json()["data"]

        # Iterating in reverse because it is more likely that the item was added recently
        for pantry_soft_item in reversed(all_items):
            if pantry_soft_item["itemNumber"] == item_number:
                return pantry_soft_item

        raise ValueError(f"Item with item number {item_number} not found in PantrySoft")

    def get_item_description(self, item_number: str) -> str:
        """Get the PantrySoft item description with the given item number."""
        try:
            item_id = self.get_item_id(item_number)
        except ValueError as e:
            raise ValueError(
                f"Item with item number {item_number} not found in PantrySoft"
            ) from e

        # Get the edit page for the item
        response = requests.get(
            f"{PANTRYSOFT_URL}/inventoryitem/{item_id}/edit",
            headers=self._headers,
            cookies=self._cookies,
        )

        # Extract the description from the response
        soup = BeautifulSoup(response.text, "html.parser")
        description = soup.find(
            "textarea", {"id": "pantrybundle_inventoryitem_description"}
        )

        if description is None:
            raise ValueError(f"Failed to get description for item {item_number}")

        return description.text

    def get_item_id(self, item_number: str) -> int:
        """Get the PantrySoft item ID with the given item number."""
        return self.get_item(item_number)["id"]

    def update_item(
        self, item: dict, name: str, item_type: str, size: float, description: str
    ) -> None:
        """Update an item in the PantrySoft inventory."""
        # Check if item type exists
        try:
            item_type_id = self.get_item_type_id(item_type)
        except ValueError:
            self.create_item_type(item_type)
            item_type_id = self.get_item_type_id(item_type)

        # Get the CSRF token
        response = requests.get(
            f"{PANTRYSOFT_URL}/inventoryitem/{item['id']}/edit",
            headers=self._headers,
            cookies=self._cookies,
        )
        soup = BeautifulSoup(response.text, "html.parser")
        form_token = soup.find(
            "input", {"id": "pantrybundle_inventoryitem__token"}
        ).get("value")

        # Send the update request
        data = {
            "pantrybundle_inventoryitem[name]": name,
            "pantrybundle_inventoryitem[itemNumber]": item["itemNumber"],
            "pantrybundle_inventoryitem[inventoryItemType]": str(item_type_id),
            "pantrybundle_inventoryitem[unit]": "Ounces",
            "pantrybundle_inventoryitem[value]": "0.00",
            "pantrybundle_inventoryitem[weight]": str(size),
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
            f"{PANTRYSOFT_URL}/inventoryitem/{item['id']}/edit",
            headers=self._headers,
            cookies=self._cookies,
            data=data,
        )

        self.last_item_changed = time.time()

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
            f"{PANTRYSOFT_URL}/inventory_code/new",
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
            f"{PANTRYSOFT_URL}/inventory_code/new",
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
            f"{PANTRYSOFT_URL}/inventoryitem/",
            headers=self._headers,
            cookies=self._cookies,
        )
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("generic-delete-modal").get("csrf-token")

        # Send the delete request
        data = {"_method": "DELETE", "csrfToken": csrf_token}
        requests.post(
            f"{PANTRYSOFT_URL}/inventoryitem/delete/{item_id}",
            headers=self._headers,
            cookies=self._cookies,
            data=data,
        )

        self.last_item_changed = time.time()

    def _upload_image(self, image: bytes) -> int:
        """
        Upload an image to the PantrySoft item.

        Parameters:
        - image (bytes): The image file to upload. Must be a JPEG file.

        Returns:
        - int: The ID of the uploaded image.
        """

        files = {
            "context": (None, "inventoryItemImages"),
            "fileupload": (
                "image.jpg",
                image,
                "image/jpeg",
            ),
        }

        response = requests.post(
            f"{PANTRYSOFT_URL}/media/upload/image",
            cookies=self._cookies,
            headers=self._headers,
            files=files,
        )

        try:
            image_id = response.json()["media"]["id"]
            return image_id
        except (JSONDecodeError, KeyError):
            raise ValueError("Failed to upload image to PantrySoft")

    def add_item_image(self, item: dict, image: bytes) -> None:
        """
        Add an image to the PantrySoft item.

        Parameters:
        - item (dict): The PantrySoft item to add an image to.
        - image_path (str): The path to the image file to upload.
        """

        # Get the CSRF token
        response = requests.get(
            f"{PANTRYSOFT_URL}/inventoryitem/{item['id']}/edit",
            headers=self._headers,
            cookies=self._cookies,
        )

        soup = BeautifulSoup(response.text, "html.parser")
        form_token = soup.find(
            "input", {"id": "pantrybundle_inventoryitem__token"}
        ).get("value")

        # Send the update request
        headers = self._headers.copy()
        headers["content-type"] = "application/x-www-form-urlencoded"
        headers["origin"] = PANTRYSOFT_URL
        headers["referer"] = f"{PANTRYSOFT_URL}/inventoryitem/{item['id']}/edit"

        image_id = self._upload_image(image)

        data = {
            "pantrybundle_inventoryitem[name]": item["name"],
            "pantrybundle_inventoryitem[itemNumber]": item["itemNumber"],
            "pantrybundle_inventoryitem[inventoryItemType]": "1",
            "pantrybundle_inventoryitem[unit]": "Ounces",
            "pantrybundle_inventoryitem[value]": "0.00",
            "pantrybundle_inventoryitem[weight]": str(item["weight"]),
            "pantrybundle_inventoryitem[outOfStockThreshold]": "0.00",
            "pantrybundle_inventoryitem[isActive]": "1",
            "pantrybundle_inventoryitem[isVisit]": "1",
            "pantrybundle_inventoryitem[isKiosk]": "1",
            "pantrybundle_inventoryitem[isStore]": "1",
            "pantrybundle_inventoryitem[backgroundColor]": "",
            "pantrybundle_inventoryitem[symbolType]": "image",
            "fileupload": "",
            "pantrybundle_inventoryitem[description]": self.get_item_description(
                item_number=item["itemNumber"]
            ),
            "pantrybundle_inventoryitem[icon]": "",
            "pantrybundle_inventoryitem[imageUploadId]": str(image_id),
            "pantrybundle_inventoryitem[_token]": form_token,
        }

        requests.post(
            f"{PANTRYSOFT_URL}/inventoryitem/{item['id']}/edit",
            cookies=self._cookies,
            headers=headers,
            data=data,
        )

    def create_item_type(self, item_type: str) -> None:
        """Create an item type in the PantrySoft inventory."""

        # Get the CSRF token
        response = requests.get(
            f"{PANTRYSOFT_URL}/inventoryitemtype/new",
            headers=self._headers,
            cookies=self._cookies,
        )
        soup = BeautifulSoup(response.text, "html.parser")
        form_token = soup.find(
            "input", {"id": "pantrybundle_inventoryitemtype__token"}
        ).get("value")

        # Send the create request
        data = {
            "pantrybundle_inventoryitemtype[name]": item_type,
            "rules[1][limit]": "1",
            "rules[1][default]": "1",
            "rules[1][householdSizeId]": "1",
            "rules[1][id]": "",
            "pantrybundle_inventoryitemtype[backgroundColor]": "",
            "pantrybundle_inventoryitemtype[symbolType]": "",
            "fileupload": "",
            "pantrybundle_inventoryitemtype[icon]": "",
            "pantrybundle_inventoryitemtype[imageUploadId]": "",
            "pantrybundle_inventoryitemtype[_token]": form_token,
        }

        requests.post(
            f"{PANTRYSOFT_URL}/inventoryitemtype/new",
            headers=self._headers,
            cookies=self._cookies,
            data=data,
        )

    def get_item_type_id(self, item_type: str) -> int:
        """Get the PantrySoft item type ID with the given item type."""
        all_item_types = self.get_all_item_types_json()["data"]

        for item_type_data in all_item_types:
            if item_type_data["name"] == item_type:
                return item_type_data["id"]

        raise ValueError(f"Item type {item_type} not found in PantrySoft")

    def delete_item_type(self, item_type_id: int) -> None:
        """Delete an item type from the PantrySoft inventory."""

        # Get the CSRF token
        response = requests.get(
            f"{PANTRYSOFT_URL}/inventoryitemtype/{item_type_id}/edit",
            headers=self._headers,
            cookies=self._cookies,
        )
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("generic-delete-modal").get("csrf-token")

        # Send the delete request
        data = {"_method": "DELETE", "csrfToken": csrf_token}

        requests.post(
            f"{PANTRYSOFT_URL}/inventoryitemtype/delete/{item_type_id}",
            headers=self._headers,
            cookies=self._cookies,
            data=data,
        )
