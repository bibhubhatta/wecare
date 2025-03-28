import os

from dotenv import load_dotenv
from get_clients import get_clients
from pantrysoft_authenticator import get_php_session_id


def main():
    session_id = get_session_id()

    clients = get_clients(session_id)
    print(clients)
    

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
