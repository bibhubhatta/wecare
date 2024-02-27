from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class PantrySoftDriver:
    """Web driver for PantrySoft.
    Stores the Selenium WebDriver and provides methods to interact with the PantrySoft website.
    """

    def __init__(self, url: str, username: str, password: str):
        """Initialize a PantrySoftDriver object.
        Args:
            url (str): The URL of the PantrySoft website.
            username (str): The username to log in with.
            password (str): The password to log in with.
        """
        self.driver = self.__get_driver(url, username, password)

    def get_php_session(self) -> str:
        """Return the PHP session ID."""
        return self.driver.get_cookie("PHPSESSID")["value"]

    @staticmethod
    def __get_driver(url: str, username: str, password: str) -> webdriver.Chrome:
        """Return a Selenium WebDriver."""
        driver = webdriver.Chrome()
        driver.get(url)

        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "index_login_btn").click()

        # Wait for the page to load
        max_wait: int = 10
        try:
            # find <a href="/inventoryitem/">Items</a>
            WebDriverWait(driver, max_wait).until(
                lambda d: d.find_element(By.XPATH, "//a[@href='/inventoryitem/']")
            )
        except TimeoutException:
            print(f"Timed out waiting for page to load after {max_wait} seconds.")
            driver.quit()
            raise

        return driver
