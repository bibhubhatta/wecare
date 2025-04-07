import json
from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Protocol

from bs4 import BeautifulSoup


@dataclass
class ClientDashboard:
    html: str

    def __post_init__(self):
        assert self.client_id is not None, "ClientDashboard must have a valid id"

    @property
    def client_id(self) -> int:
        soup = BeautifulSoup(self.html, "html.parser")
        location_map = soup.select_one("location-map-view")
        json_str = location_map[":json-client"]
        client_id = json.loads(json_str)["id"]
        return int(client_id)

    @property
    def client_visit_dates(self) -> List[date]:
        soup = BeautifulSoup(self.html, "html.parser")
        visit_modal = soup.select_one("visit-frequency-rule-modal")

        if visit_modal and ":visit-stats" in visit_modal.attrs:
            visit_stats_json = visit_modal[":visit-stats"]
            visit_stats = json.loads(visit_stats_json)

            if visit_stats and len(visit_stats) > 0 and "events" in visit_stats[0]:
                events = visit_stats[0]["events"]
                # Convert string dates to date objects
                return [date.fromisoformat(event_date) for event_date in events]

        return []

    @property
    def visit_ids(self) -> List[int]:
        soup = BeautifulSoup(self.html, "html.parser")
        visit_labels = soup.find_all(
            "div", id=lambda x: x and x.startswith("visit_label_")
        )
        visit_ids = []
        for label in visit_labels:
            # Extract the visit ID from the div's id attribute
            visit_id = label["id"].split("_")[-1]
            visit_ids.append(int(visit_id))
        return visit_ids


class ClientDashboardRepository(Protocol):
    def save(self, dashboard: ClientDashboard) -> None: ...

    def get(self, client_id: int) -> Optional[ClientDashboard]: ...

    def get_all(self) -> List[ClientDashboard]: ...


class ClientDashboardRepositoryInMemory(ClientDashboardRepository):
    def __init__(self):
        self.dashboards = {}

    def save(self, dashboard: ClientDashboard) -> None:
        self.dashboards[dashboard.client_id] = dashboard

    def get(self, client_id: int) -> Optional[ClientDashboard]:
        return self.dashboards.get(client_id)

    def get_all(self) -> List[ClientDashboard]:
        return list(self.dashboards.values())
