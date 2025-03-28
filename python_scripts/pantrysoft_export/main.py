import csv
import os
from typing import Any

from dotenv import load_dotenv
from get_client_html_file import get_client_dashboard_html_page
from get_clients import get_clients
from joblib import Memory
from pantrysoft_authenticator import get_php_session_id


def main():
    session_id = get_session_id()

    clients = get_clients(session_id)
    save_to_csv(clients, "export/clients.csv")

    for client in clients:
        client_id = client["id"]
        print(f"Exporting client number {client_id}'s dashboard...")
        # Get the HTML for each client
        html = get_client_dashboard_html_page(client_id, session_id)
        save_html_file(html, f"export/html/client_dashboard_{client_id:03d}.html")


@Memory(".cache", verbose=0).cache
def save_html_file(html: str, file_path: str) -> None:
    """Saves HTML content to a file.

    Args:
        html (str): The HTML content to save.
        file_path (str): The path to the file to create/overwrite.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html)
        print(f"HTML content successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred while writing HTML to file: {e}")


@Memory(".cache", verbose=0).cache
def save_to_csv(data: list[dict[str, Any]], csv_file_path: str):
    """Saves a list of dictionaries to a CSV file.

    Args:
        data (list): A list of dictionaries to save.
        csv_file_path (str): The path to the CSV file to create/overwrite.
    """

    if not data:
        print("No data to write to CSV.")
        return

    flattened_data = [
        flatten_dict(item) for item in data
    ]  # Flatten each dictionary in the list

    # Get all unique headers from the flattened dictionaries.
    header = set()
    for row in flattened_data:
        header.update(row.keys())
    header = sorted(list(header))  # Sort for consistent column order

    try:
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            for row in flattened_data:
                writer.writerow(row)
        print(f"Data successfully written to {csv_file_path}")

    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")


def flatten_dict(
    data: dict[str, Any], parent_key: str = "", sep: str = "_"
) -> dict[str, Any]:
    """Flattens a nested dictionary into a single-level dictionary.

    Args:
        data (dict): The dictionary to flatten.
        parent_key (str): The prefix for keys in the flattened dictionary.
        sep (str): The separator to use when concatenating keys.

    Returns:
        dict: A flattened dictionary.
    """
    items = []
    for k, v in data.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):  # Handle lists (e.g., creditTransactions, documents)
            # For simplicity, just store the length of the list.
            items.append((new_key + "_length", len(v)))
        else:
            items.append((new_key, v))
    return dict(items)


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


def get_from_env(key: str) -> str:
    """Get an environment variable."""
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Environment variable {key} not found.")
    return value


if __name__ == "__main__":
    main()
