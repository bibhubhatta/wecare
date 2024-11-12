import os
from dotenv import load_dotenv

load_dotenv()

PANTRYSOFT_URL = os.environ.get("PANTRYSOFT_URL")
PANTRYSOFT_USERNAME = os.environ.get("PANTRYSOFT_USERNAME")
PANTRYSOFT_PASSWORD = os.environ.get("PANTRYSOFT_PASSWORD")

if not PANTRYSOFT_URL:
    raise ValueError("PANTRYSOFT_URL environment variable not set")
if not PANTRYSOFT_USERNAME:
    raise ValueError("PANTRYSOFT_USERNAME environment variable not set")
if not PANTRYSOFT_PASSWORD:
    raise ValueError("PANTRYSOFT_PASSWORD environment variable not set")