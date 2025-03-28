from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_driver import BasePantrySoftDriver


class SeleniumPantrySoftDriver(BasePantrySoftDriver):
    """Web driver for PantrySoft using Selenium."""

    def _setup_driver(self) -> None:
        """Set up the Selenium WebDriver and log in to PantrySoft."""
        # Start the web driver headless
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self._url)

        self.driver.find_element(By.ID, "username").send_keys(self._username)
        self.driver.find_element(By.ID, "password").send_keys(self._password)
        self.driver.find_element(By.ID, "index_login_btn").click()

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[@href='/inventoryitem/']")
                )
            )
        except TimeoutException:
            print("Timed out waiting for page to load.")
            self.driver.quit()
            raise

    def get_php_session(self) -> str:
        """Return the PHP session ID."""
        return self.driver.get_cookie("PHPSESSID")["value"]

    def get_php_session_expiry(self) -> int:
        """Return the PHP session expiry time in unix timestamp."""
        expiry = self.driver.get_cookie("PHPSESSID")["expiry"]
        return expiry

    def add_item(self, name: str, upc: str, size: float) -> None:
        """Add an item to the pantry."""
        self.driver.get("https://app.pantrysoft.com/inventoryitem/new")
        sleep(1)

        self._fill_input_field("pantrybundle_inventoryitem_name", name)
        self._fill_input_field("pantrybundle_inventoryitem_itemNumber", upc)
        self._fill_input_field("pantrybundle_inventoryitem_weight", str(size))

        self._submit("//button[@class='btn btn-default' and @type='submit']")

    def link_code_to_item(self, upc: str, name: str) -> None:
        """Links UPC code to an item."""
        self.driver.get("https://app.pantrysoft.com/inventory_code/")
        sleep(1)

        new_code_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-default"))
        )
        new_code_button.send_keys(Keys.ENTER)
        sleep(0.6)

        self._fill_input_field("pantrybundle_inventoryitemcode_codeNumber", upc)

        search_field = self.driver.find_element(By.CLASS_NAME, "vs__search")
        search_field.send_keys(name)
        sleep(1)
        search_field.send_keys(Keys.ENTER)

    def _fill_input_field(self, field_id: str, value: str) -> None:
        """Fill an input field."""
        field = self.driver.find_element(By.ID, field_id)
        field.clear()
        field.send_keys(value)
        sleep(0.5)

    def _submit(self, button_xpath: str) -> None:
        """Submit the form by clicking a button."""
        submit_button = self.driver.find_element(By.XPATH, button_xpath)
        submit_button.send_keys(Keys.ENTER)
        sleep(0.5)

    def close(self) -> None:
        """Close the web driver."""
        self.driver.quit()
