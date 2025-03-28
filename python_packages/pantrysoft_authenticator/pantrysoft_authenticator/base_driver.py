from abc import ABC, abstractmethod


class BasePantrySoftDriver(ABC):
    """Abstract base class for PantrySoft web drivers."""

    def __init__(self, url: str, username: str, password: str):
        """Initialize a PantrySoft driver."""
        self._url = url
        self._username = username
        self._password = password
        self._setup_driver()

    @abstractmethod
    def _setup_driver(self) -> None:
        """Set up the driver and log in to PantrySoft."""
        pass

    @abstractmethod
    def get_php_session(self) -> str:
        """Return the PHP session ID."""
        pass

    @abstractmethod
    def get_php_session_expiry(self) -> int:
        """Return the PHP session expiry time in unix timestamp."""
        pass

    @abstractmethod
    def add_item(self, name: str, upc: str, size: float) -> None:
        """Add an item to the pantry."""
        pass

    @abstractmethod
    def link_code_to_item(self, upc: str, name: str) -> None:
        """Links UPC code to an item."""
        pass

    @abstractmethod
    def _fill_input_field(self, field_id: str, value: str) -> None:
        """Fill an input field."""
        pass

    @abstractmethod
    def _submit(self, button_selector: str) -> None:
        """Submit the form by clicking a button."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the driver."""
        pass
