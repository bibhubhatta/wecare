import re
from dataclasses import dataclass
from datetime import datetime

from bs4 import BeautifulSoup


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
