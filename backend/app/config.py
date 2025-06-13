# backend/app/config.py

from dotenv import load_dotenv
import os

load_dotenv()  # Load .env early and once

MAERSK_CLIENT_ID = os.getenv("MAERSK_CLIENT_ID")
MAERSK_CLIENT_SECRET = os.getenv("MAERSK_CLIENT_SECRET")
MAERSK_CUSTOMER_CODE = os.getenv("MAERSK_CUSTOMER_CODE")
MAERSK_CARRIER_CODE = os.getenv("MAERSK_CARRIER_CODE", "MAEU")

# Optional safety check
if not MAERSK_CLIENT_ID or not MAERSK_CUSTOMER_CODE:
    raise ValueError("Missing required Maersk credentials in .env")
