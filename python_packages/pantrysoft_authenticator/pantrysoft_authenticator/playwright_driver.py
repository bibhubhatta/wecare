from time import sleep

from playwright.sync_api import sync_playwright


class PantrySoftDriver:
    """Web driver for PantrySoft."""

    def __init__(self, url: str, username: str, password: str):
        """Initialize a PantrySoftDriver object."""
        self.playwright = sync_playwright().start()
        self.browser = None
        self.page = None
        self.__setup_driver(url, username, password)

    def __setup_driver(self, url: str, username: str, password: str):
        """Set up the Playwright browser and page."""
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()
        self.page.goto(url)

        self.page.fill("#username", username)
        self.page.fill("#password", password)
        self.page.click("#index_login_btn")

        # Wait for the login to complete
        self.page.wait_for_selector("#index_login_btn", state="detached")

    def get_php_session(self) -> str:
        """Return the PHP session ID."""
        cookies = self.page.context.cookies()
        for cookie in cookies:
            if cookie["name"] == "PHPSESSID":
                return cookie["value"]
        return None

    def get_php_session_expiry(self) -> int:
        """Return the PHP session expiry time in unix timestamp."""
        cookies = self.page.context.cookies()
        for cookie in cookies:
            if cookie["name"] == "PHPSESSID":
                return cookie.get("expires", 0)
        return 0

    def add_item(self, name: str, upc: str, size: float):
        """Add an item to the pantry."""
        self.page.goto("https://app.pantrysoft.com/inventoryitem/new")
        sleep(1)

        self.__fill_input_field("pantrybundle_inventoryitem_name", name)
        self.__fill_input_field("pantrybundle_inventoryitem_itemNumber", upc)
        self.__fill_input_field("pantrybundle_inventoryitem_weight", str(size))

        self.__submit("//button[@class='btn btn-default' and @type='submit']")

    def link_code_to_item(self, upc: str, name: str):
        """Links UPC code to an item."""
        self.page.goto("https://app.pantrysoft.com/inventory_code/")
        sleep(1)

        # Wait for and click the new code button
        self.page.wait_for_selector(".btn-default")
        self.page.click(".btn-default")
        sleep(0.6)

        self.__fill_input_field("pantrybundle_inventoryitemcode_codeNumber", upc)

        # Search field handling
        search_field = self.page.locator(".vs__search")
        search_field.fill(name)
        sleep(1)
        search_field.press("Enter")

    def __fill_input_field(self, field_id: str, value: str):
        """Fill an input field."""
        self.page.fill(f"#{field_id}", value)
        sleep(0.5)

    def __submit(self, button_xpath: str):
        """Submit the form by clicking a button."""
        self.page.click(button_xpath)
        sleep(0.5)

    def close(self):
        """Close the browser and playwright."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
