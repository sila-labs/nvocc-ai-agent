# app/tasks/refresh_import_charges.py

from app.db.session import SessionLocal
from app.models.import_charges import ImportCharge
from app.services.maersk_token import MaerskTokenManager
from app.services.import_charge_service import upsert_import_charge_from_api
from app import config
import requests

def refresh_all_tracked_bls():
    db = SessionLocal()
    token_manager = MaerskTokenManager()
    updated_count = 0

    print("[INFO] Starting daily demurrage refresh...")

    try:
        records = db.query(ImportCharge).all()
        seen = set()

        for record in records:
            key = (record.bill_of_lading, record.charge_type)
            if key in seen:
                continue
            seen.add(key)

            url = (
                f"https://api.maersk.com/shipping-charges/import/{record.charge_type}"
                f"?billOfLadingNumber={record.bill_of_lading}"
                f"&carrierCustomerCode={config.MAERSK_CUSTOMER_CODE}"
                f"&carrierCode={config.MAERSK_CARRIER_CODE}"
            )

            print(f"[INFO] Refreshing {key}...")

            response = requests.get(
                url,
                headers={
                    **token_manager.get_auth_header(),
                    "Consumer-Key": config.MAERSK_CLIENT_ID,
                    "Content-Type": "application/json"
                }
            )

            if response.status_code != 200:
                print(f"[WARN] Failed to refresh B/L {record.bill_of_lading} — {response.status_code}")
                continue

            data = response.json()
            for container in data.get("equipmentCharges", []):
                upsert_import_charge_from_api(
                    db=db,
                    bill_of_lading=record.bill_of_lading,
                    charge_type=record.charge_type,
                    container_data=container,
                    location_name=data.get("location", {}).get("locationName"),
                    currency=data.get("currencyCode", "USD")
                )
                updated_count += 1

    finally:
        db.close()

    print(f"[SUCCESS] Refreshed {updated_count} containers.")

if __name__ == "__main__":
    refresh_all_tracked_bls()
