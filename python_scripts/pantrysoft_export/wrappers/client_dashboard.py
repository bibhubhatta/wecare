import json
from dataclasses import dataclass
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
