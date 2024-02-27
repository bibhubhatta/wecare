from time import sleep

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from inventory.item import Item


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
        # Start driver headless
        # options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # driver = webdriver.Chrome(options=options)
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

    def add_item(self, item: Item):
        # TODO: driver should not have dependencies on the Item class
        """Add an item to the pantry."""
        self.driver.get("https://app.pantrysoft.com/inventoryitem/new")
        sleep(1)

        name_field = self.driver.find_element(By.ID, "pantrybundle_inventoryitem_name")
        sleep(0.1)
        item_number_field = self.driver.find_element(
            By.ID, "pantrybundle_inventoryitem_itemNumber"
        )
        sleep(0.1)
        weight_field = self.driver.find_element(
            By.ID, "pantrybundle_inventoryitem_weight"
        )
        sleep(0.1)

        name_field.clear()
        name_field.send_keys(item.name)
        sleep(0.15)

        item_number_field.clear()
        item_number_field.send_keys(item.upc)
        sleep(0.15)

        weight_field.clear()
        weight_field.send_keys(item.size)
        sleep(0.15)

        # Unit and category are difficult to deal with because they are many to many relationships, so we'll skip them
        # for now.
        # Description also seems like a foreign key relationship, so we'll skip that for now.

        submit_button = self.driver.find_element(
            By.XPATH, '//*[@id="blueBar"]/div/div[3]/button'
        )
        submit_button.send_keys(Keys.ENTER)
        sleep(0.5)

    def link_code_to_item(self, item: Item):
        """Links UPC code to an item."""
        self.driver.get("https://app.pantrysoft.com/inventory_code/")
        sleep(1)

        # click on the <button type="button" class="btn btn-default" onclick="newItemCode()">
        #         New Item Code
        #     </button>

        # wait until the button is clickable
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(By.CLASS_NAME, "btn-default")
        )
        self.driver.find_element(By.CLASS_NAME, "btn-default").send_keys(Keys.ENTER)
        sleep(0.6)

        # find text field with id pantrybundle_inventoryitemcode_codeNumber
        code_number_field = self.driver.find_element(
            By.ID, "pantrybundle_inventoryitemcode_codeNumber"
        )
        code_number_field.send_keys(item.upc)
        sleep(0.15)

        # <input aria-autocomplete="list" aria-labelledby="vs4__combobox" aria-controls="vs4__listbox" type="search" autocomplete="off" class="vs__search">
        search_field = self.driver.find_element(By.CLASS_NAME, "vs__search")
        search_field.send_keys(item.name)

        # Pause for one second and press enter on the search field
        sleep(1)
        search_field.send_keys(Keys.ENTER)
