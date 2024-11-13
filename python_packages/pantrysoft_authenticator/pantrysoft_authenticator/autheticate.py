from pantrysoft_authenticator import driver

PANTRYSOFT_URL = "https://app.pantrysoft.com"

def get_php_session_id(username: str, password: str) -> str:
    """Authenticate with PantrySoft."""
    pantrysoft_driver = driver.PantrySoftDriver(PANTRYSOFT_URL, username, password)
    try:
        return pantrysoft_driver.get_php_session()
    except Exception as e:
        pantrysoft_driver.driver.quit()
        raise e
