from get_edit_visit_html_page import get_edit_visit_page
from get_items import get_items
from main import CLIENT_DASHBOARD_REPO, VISIT_PAGE_REPO, get_session_id
from wrappers import VisitEditPage


def test_visit_id_extraction():
    dashboards = CLIENT_DASHBOARD_REPO.get_all()
    for dashboard in dashboards:
        visit_dates = dashboard.client_visit_dates
        print(visit_dates)
        visit_ids = dashboard.visit_ids
        assert len(visit_dates) == len(visit_ids), (
            "Visit dates and IDs do not match in length"
        )
        print(visit_ids)


def test_visit_edit_page():
    session_id = get_session_id()

    dashboard = CLIENT_DASHBOARD_REPO.get(100)
    visit_ids = dashboard.visit_ids

    for visit_id in visit_ids:
        print(visit_id)
        html_page = get_edit_visit_page(visit_id, session_id)
        page = VisitEditPage(html_page)

        assert page.visit_id == visit_id, "Visit ID is incorrect"


def test_visit_date_extraction():
    for visit_id in range(100):
        visit = VISIT_PAGE_REPO.get(visit_id)
        if visit:
            print(visit.visit_date_time)


def visit_item_extraction():
    visit_page = VISIT_PAGE_REPO.get(2267)
    for i in visit_page.visit_items:
        print(i)

    print(visit_page.get_visit())


def test_get_clients():
    session_id = get_session_id()
    items = get_items(session_id)
    print(items)


if __name__ == "__main__":
    test_get_clients()
