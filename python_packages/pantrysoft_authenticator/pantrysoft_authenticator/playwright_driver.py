from time import sleep
from typing import Optional

from playwright.sync_api import Page, Playwright, sync_playwright

from .base_driver import BasePantrySoftDriver


class PlaywrightPantrySoftDriver(BasePantrySoftDriver):
    """Web driver for PantrySoft using Playwright."""

    def _setup_driver(self) -> None:
        """Set up the Playwright browser and page."""
        self.playwright: Playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page: Page = self.browser.new_page()
        self.page.goto(self._url)

        self.page.fill("#username", self._username)
        self.page.fill("#password", self._password)
        self.page.click("#index_login_btn")

        # Wait for the login to complete
        self.page.wait_for_selector("#index_login_btn", state="detached")

    def get_php_session(self) -> Optional[str]:
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

    def add_item(self, name: str, upc: str, size: float) -> None:
        """Add an item to the pantry."""
        self.page.goto("https://app.pantrysoft.com/inventoryitem/new")
        sleep(1)

        self._fill_input_field("pantrybundle_inventoryitem_name", name)
        self._fill_input_field("pantrybundle_inventoryitem_itemNumber", upc)
        self._fill_input_field("pantrybundle_inventoryitem_weight", str(size))

        self._submit("//button[@class='btn btn-default' and @type='submit']")

    def link_code_to_item(self, upc: str, name: str) -> None:
        """Links UPC code to an item."""
        self.page.goto("https://app.pantrysoft.com/inventory_code/")
        sleep(1)

        # Wait for and click the new code button
        self.page.wait_for_selector(".btn-default")
        self.page.click(".btn-default")
        sleep(0.6)

        self._fill_input_field("pantrybundle_inventoryitemcode_codeNumber", upc)

        # Search field handling
        search_field = self.page.locator(".vs__search")
        search_field.fill(name)
        sleep(1)
        search_field.press("Enter")

    def _fill_input_field(self, field_id: str, value: str) -> None:
        """Fill an input field."""
        self.page.fill(f"#{field_id}", value)
        sleep(0.5)

    def _submit(self, button_xpath: str) -> None:
        """Submit the form by clicking a button."""
        self.page.click(button_xpath)
        sleep(0.5)

    def close(self) -> None:
        """Close the browser and playwright."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
