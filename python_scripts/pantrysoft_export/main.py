import os

from dotenv import load_dotenv

from pantrysoft_authenticator import get_php_session_id


def main():
    load_dotenv()
    username = get_from_env("PANTRYSOFT_USERNAME")
    password = get_from_env("PANTRYSOFT_PASSWORD")

    session_id = get_php_session_id(username, password)
    print("session_id:", session_id)


def get_from_env(key: str) -> str:
    """Get an environment variable."""
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Environment variable {key} not found.")
    return value


if __name__ == "__main__":
    main()
