# app/services/import_charge_service.py

from sqlalchemy.orm import Session
from app.models.import_charges import ImportCharge
from datetime import datetime

def upsert_import_charge_from_api(
    db: Session,
    bill_of_lading: str,
    charge_type: str,
    container_data: dict,
    location_name: str = None,
    currency: str = "USD",
):
    container_number = container_data.get("equipmentReference")
    is_final = container_data.get("isFinalCharge", False)
    free_period = container_data.get("freePeriod", {})
    actual_last_free = free_period.get("actualLastFreeDate")
    estimated_last_free = free_period.get("estimatedLastFreeDate")

    # Check if entry exists
    existing = db.query(ImportCharge).filter_by(
        bill_of_lading=bill_of_lading,
        container_number=container_number,
        charge_type=charge_type
    ).first()

    if existing:
        # Update existing
        existing.is_final_charge = is_final
        existing.actual_last_free_date = actual_last_free
        existing.estimated_last_free_date = estimated_last_free
        existing.last_checked_at = datetime.utcnow()
        existing.status = determine_status(actual_last_free or estimated_last_free)
    else:
        # Create new entry
        new_entry = ImportCharge(
            bill_of_lading=bill_of_lading,
            container_number=container_number,
            charge_type=charge_type,
            is_final_charge=is_final,
            actual_last_free_date=actual_last_free,
            estimated_last_free_date=estimated_last_free,
            location_name=location_name,
            currency=currency,
            status=determine_status(actual_last_free or estimated_last_free),
            last_checked_at=datetime.utcnow()
        )
        db.add(new_entry)

    db.commit()

def determine_status(last_free_date):
    if not last_free_date:
        return "Unknown"
    today = datetime.utcnow().date()
    delta = (last_free_date - today).days
    if delta < 0:
        return "Expired"
    elif delta == 0:
        return "ExpiringToday"
    elif delta <= 2:
        return "ExpiringSoon"
    return "Safe"
