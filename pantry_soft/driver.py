from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from inventory.item import Item


class PantrySoftDriver:
    """Web driver for PantrySoft."""

    _instance = None

    def __init__(self, url: str, username: str, password: str):
        """Initialize a PantrySoftDriver object."""
        self.driver = self.__get_driver(url, username, password)

    def get_php_session(self) -> str:
        """Return the PHP session ID."""
        return self.driver.get_cookie("PHPSESSID")["value"]

    def get_php_session_expiry(self) -> int:
        """Return the PHP session expiry time in unix timestamp."""
        expiry = self.driver.get_cookie("PHPSESSID")["expiry"]
        return expiry

    @classmethod
    def __get_driver(cls, url: str, username: str, password: str) -> webdriver.Chrome:
        """Return a Selenium WebDriver."""
        if cls._instance is None:
            options = webdriver.ChromeOptions()
            # options.add_argument("--headless")

            driver = webdriver.Chrome(options=options)
            driver.get(url)

            driver.find_element(By.ID, "username").send_keys(username)
            driver.find_element(By.ID, "password").send_keys(password)
            driver.find_element(By.ID, "index_login_btn").click()

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//a[@href='/inventoryitem/']")
                    )
                )
            except TimeoutException:
                print("Timed out waiting for page to load.")
                driver.quit()
                raise

            cls._instance = driver

        return cls._instance

    def add_item(self, item: Item):
        """Add an item to the pantry."""
        self.driver.get("https://app.pantrysoft.com/inventoryitem/new")
        sleep(1)

        self.__fill_input_field("pantrybundle_inventoryitem_name", item.name)
        self.__fill_input_field("pantrybundle_inventoryitem_itemNumber", item.upc)
        self.__fill_input_field("pantrybundle_inventoryitem_weight", str(item.size))

        self.__submit("//button[@class='btn btn-default' and @type='submit']")

    def link_code_to_item(self, item: Item):
        """Links UPC code to an item."""
        self.driver.get("https://app.pantrysoft.com/inventory_code/")
        sleep(1)

        new_code_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-default"))
        )
        new_code_button.send_keys(Keys.ENTER)
        sleep(0.6)

        self.__fill_input_field("pantrybundle_inventoryitemcode_codeNumber", item.upc)

        search_field = self.driver.find_element(By.CLASS_NAME, "vs__search")
        search_field.send_keys(item.name)
        sleep(1)
        search_field.send_keys(Keys.ENTER)

    def __fill_input_field(self, field_id: str, value: str):
        """Fill an input field."""
        field = self.driver.find_element(By.ID, field_id)
        field.clear()
        field.send_keys(value)
        sleep(0.5)

    def __submit(self, button_xpath: str):
        """Submit the form by clicking a button."""
        submit_button = self.driver.find_element(By.XPATH, button_xpath)
        submit_button.send_keys(Keys.ENTER)
        sleep(0.5)

    def close(self):
        """Close the web driver."""
        self.driver.quit()
        PantrySoftDriver._instance = None
