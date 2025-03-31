from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class Client:
    client_dict: dict[str, Any]

    def __post_init__(self):
        if "id" not in self.client_dict:
            raise ValueError("Client dictionary must contain 'id' key.")

    @property
    def id(self) -> int:
        return int(self.client_dict["id"])


class ClientRepository(Protocol):
    def save(self, client: Client) -> None: ...
    def get(self, client_id: int) -> Client: ...
    def get_all(self) -> list[Client]: ...


class ClientRepositoryInMemory(ClientRepository):
    def __init__(self):
        self.clients = {}

    def save(self, client: Client) -> None:
        self.clients[client.id] = client

    def get(self, client_id: int) -> Client:
        return self.clients.get(client_id)

    def get_all(self) -> list[Client]:
        return list(self.clients.values())
