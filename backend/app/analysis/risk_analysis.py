from datetime import datetime
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.import_charge import ImportCharge

def assess_risk(days_left: int, total_fees: float) -> str:
    if days_left <= 1 or total_fees > 500:
        return "high"
    elif days_left <= 3 or total_fees > 200:
        return "medium"
    else:
        return "low"

def analyze_risk(db: Session) -> List[Dict]:
    today = datetime.utcnow().date()
    results = []

    charges = db.query(ImportCharge).all()
    grouped = {}

    for charge in charges:
        key = (charge.bill_of_lading, charge.charge_type)
        grouped.setdefault(key, []).append(charge)

    for (bol, charge_type), entries in grouped.items():
        latest = max(entries, key=lambda e: e.last_updated)
        end_date = latest.charges_end_date or today
        days_until_fees = (end_date - today).days
        total_fee = sum(e.amount for e in entries)

        results.append({
            "container_number": latest.container_number,
            "bill_of_lading": bol,
            "charge_type": charge_type,
            "risk_level": assess_risk(days_until_fees, total_fee),
            "days_until_fees": days_until_fees,
            "total_fees": float(total_fee)
        })

    return results
