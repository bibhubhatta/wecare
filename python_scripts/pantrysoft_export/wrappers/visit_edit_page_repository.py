from typing import List, Optional, Protocol

from wrappers import VisitEditPage


class VisitEditPageRepository(Protocol):
    def save(self, visit_page: VisitEditPage) -> None: ...

    def get(self, visit_id: int) -> Optional[VisitEditPage]: ...

    def get_all(self) -> List[VisitEditPage]: ...


class VisitEditPageRepositoryInMemory(VisitEditPageRepository):
    def __init__(self):
        self.visit_pages = {}

    def save(self, visit_page: VisitEditPage) -> None:
        self.visit_pages[visit_page.visit_id] = visit_page

    def get(self, visit_id: int) -> Optional[VisitEditPage]:
        return self.visit_pages.get(visit_id)

    def get_all(self) -> List[VisitEditPage]:
        return list(self.visit_pages.values())
