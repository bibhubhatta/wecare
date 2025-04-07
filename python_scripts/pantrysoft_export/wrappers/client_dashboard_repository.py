from typing import List, Optional, Protocol

from wrappers import ClientDashboard


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
