import csv
import os
from typing import Any


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


def get_from_env(key: str) -> str:
    """Get an environment variable."""
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Environment variable {key} not found.")
    return value


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
