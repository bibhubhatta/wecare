import os

import sqlalchemy
from dotenv import load_dotenv
from get_client_html_file import get_client_dashboard_html_page
from get_clients import get_client_list
from get_edit_visit_html_page import get_edit_visit_page
from pantrysoft_authenticator import get_php_session_id
from utilities import get_from_env, save_to_csv
from wrappers import (
    ClientDashboard,
    ClientDashboardRepositorySql,
    ClientRepositorySql,
    VisitEditPage,
    VisitEditPageRepositorySql,
)

SQLITE_ENGINE = sqlalchemy.create_engine("sqlite:///export/pantrysoft.db")
CLIENT_REPO = ClientRepositorySql(SQLITE_ENGINE)
CLIENT_DASHBOARD_REPO = ClientDashboardRepositorySql(SQLITE_ENGINE)
VISIT_PAGE_REPO = VisitEditPageRepositorySql(SQLITE_ENGINE)


def main():
    """Main function to prepare the database and export data to CSV."""
    # save_clients()
    # export_to_csv()
    save_visits()


def save_visits():
    """Save visits to the database."""
    session_id = get_session_id()

    # Get clients from Pantrysoft
    clients = CLIENT_DASHBOARD_REPO.get_all()

    for client in clients:
        visit_ids = client.visit_ids
        for visit_id in visit_ids:
            if visit_id in VISIT_PAGE_REPO:
                print(f"Visit {visit_id} already exists in the database.")
            else:
                print(f"Visit {visit_id} does not exist in the database. Saving...")
                visit_html = get_edit_visit_page(visit_id, session_id)
                visit_page = VisitEditPage(visit_html)
                VISIT_PAGE_REPO.save(visit_page)
                print(f"Visit {visit_id} saved to the database.")

    print("Done.")


def export_to_csv():
    dashboards = CLIENT_DASHBOARD_REPO.get_all()
    client_vist_dates = []
    for dashboard in dashboards:
        visit_dates = dashboard.client_visit_dates
        for visit_date in visit_dates:
            client_vist_dates.append(
                {
                    "client_id": dashboard.client_id,
                    "visit_date": visit_date,
                }
            )

    save_to_csv(client_vist_dates, "export/client_vist_dates.csv")

    clients = CLIENT_REPO.get_all()
    client_data = [client.client_dict for client in clients]
    save_to_csv(client_data, "export/clients.csv")


def save_clients():
    session_id = get_session_id()

    # Get clients from Pantrysoft
    clients = get_client_list(session_id)

    for client in clients:
        if client in CLIENT_REPO and CLIENT_REPO.get(client.id) is not None:
            print(f"Client {client.id} already exists in the database.")
        else:
            print(f"Client {client.id} does not exist in the database. Saving...")
            CLIENT_REPO.save(client)

        if (
            client.id in CLIENT_DASHBOARD_REPO
            and CLIENT_DASHBOARD_REPO.get(client.id) is not None
        ):
            print(f"Client dashboard {client.id} already exists in the database.")
        else:
            print(
                f"Client {client.id} does not exist in the dashboard database. Saving..."
            )
            client_dashboard_html = get_client_dashboard_html_page(
                client.id, session_id
            )
            client_dashboard = ClientDashboard(client_dashboard_html)
            CLIENT_DASHBOARD_REPO.save(client_dashboard)

    print("All clients and dashboards have been saved to the database.")


def get_session_id() -> str:
    """Get the PHP session ID."""

    # Check if cached session ID is available
    SESSION_FILE = "session_id.txt"
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as file:
            return file.read().strip()

    load_dotenv()
    username = get_from_env("PANTRYSOFT_USERNAME")
    password = get_from_env("PANTRYSOFT_PASSWORD")

    session_id = get_php_session_id(username, password)
    # Save the session ID to a file
    with open(SESSION_FILE, "w") as file:
        file.write(session_id)

    return session_id


if __name__ == "__main__":
    main()
