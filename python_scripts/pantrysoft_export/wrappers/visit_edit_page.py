import html
import json
import re
from dataclasses import dataclass
from datetime import datetime

from bs4 import BeautifulSoup


@dataclass
class VisitItem:
    id: int
    item_id: int
    item_quantity: int
    comment: str


@dataclass
class VisitEditPage:
    html: str

    def __post_init__(self):
        assert self.visit_id is not None, "VisitEditPage must have a valid id"

    @property
    def visit_id(self) -> int:
        # Directly use regex to find the visit ID in the action attribute
        pattern = r'action="/visit/edit_visit_dialog/(\d+)"'
        match = re.search(pattern, self.html)
        if match:
            visit_id = match.group(1)
            return int(visit_id)

        # If regex fails, use BeautifulSoup as a fallback
        soup = BeautifulSoup(self.html, "html.parser")
        form = soup.find("form", {"name": "pantrybundle_visit"})
        if form and "action" in form.attrs:
            action = form["action"]
            visit_id = action.split("/")[-1]
            return int(visit_id)

        raise ValueError("Visit ID not found in the HTML")

    @property
    def visit_date_time(self) -> datetime:
        soup = BeautifulSoup(self.html, "html.parser")
        date_time_input = soup.find("input", {"id": "pantrybundle_visit_visitDatetime"})
        if date_time_input and "value" in date_time_input.attrs:
            date_time_str = date_time_input["value"]
            return datetime.strptime(date_time_str, "%m/%d/%Y %I:%M %p")

        raise ValueError("Visit date time not found in the HTML")

    @property
    def visit_items(self) -> list[VisitItem]:
        """
        Extract inventory items data from the inventory-item-distributor element.
        """
        soup = BeautifulSoup(self.html, "html.parser")
        inventory_item_distributor = soup.find("inventory-item-distributor")

        if not inventory_item_distributor:
            return []

        # Find the init-inventory-item-instances attribute
        visit_list = []
        for attr in inventory_item_distributor.attrs:
            if attr.lower().endswith("init-inventory-item-instances"):
                # Extract the JSON string from the attribute
                json_str = inventory_item_distributor[attr]

                # Decode HTML entities
                decoded_str = html.unescape(json_str)

                # Remove any surrounding brackets if they exist
                if decoded_str.startswith("[") and decoded_str.endswith("]"):
                    decoded_str = decoded_str
                else:
                    # Try to find the JSON array using regex
                    match = re.search(r"\[\{.*\}\]", decoded_str)
                    if match:
                        decoded_str = match.group(0)

                try:
                    # Parse the JSON string into a Python list of dictionaries
                    visit_list = json.loads(decoded_str)
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {e}")

        visit_items = []
        for item_dict in visit_list:
            visit_item = VisitItem(
                id=item_dict.get("id"),
                item_id=item_dict.get("inventoryItem").get("id"),
                item_quantity=item_dict.get("quantity"),
                comment=item_dict.get("comment"),
            )

            visit_items.append(visit_item)

        return visit_items
