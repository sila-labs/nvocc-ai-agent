# backend/app/api/v1/routes.py

from fastapi import APIRouter, HTTPException, Query
import requests
from typing import Optional
from app.models.container import ContainerTracking
from app.services.maersk_client import MaerskAPIClient
from app.services.maersk_token import MaerskTokenManager
from app import config
from datetime import date
from app.services.import_charge_service import upsert_import_charge_from_api
from app.dependencies.db import get_db 
from fastapi import Depends
from sqlalchemy.orm import Session

from app.models.import_charges import ImportCharge
from app.models.schemas import ImportChargeOut
from datetime import datetime

from app.services.risk_analysis import calculate_demurrage_risk
from app.services.risk_analysis import generate_risk_summary

router = APIRouter()
client = MaerskAPIClient()
token_manager = MaerskTokenManager()

@router.get("/health")
def health():
    return {"status": "running"}

@router.get("/track/{container_id}", response_model=ContainerTracking)
def get_container_status(container_id: str):
    try:
        data = client.track_container(container_id)
        return ContainerTracking(
            container_number=data["containerNumber"],
            carrier="Maersk",
            status=data["status"],
            location=data["location"],
            eta=data["eta"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/demurrage-detention/{charge_type}")
def get_demurrage_detention(
    charge_type: str,
    billOfLadingNumber: str = Query(..., min_length=9, max_length=9),
    chargesEndDate: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    ...
    try:
        response = requests.get(
            url,
            headers={
                **token_manager.get_auth_header(),
                "Consumer-Key": config.MAERSK_CLIENT_ID,
                "Content-Type": "application/json"
            }
        )
        response.raise_for_status()
        data = response.json()

        # Save to DB
        for container in data.get("equipmentCharges", []):
            upsert_import_charge_from_api(
                db=db,
                bill_of_lading=billOfLadingNumber,
                charge_type=charge_type,
                container_data=container,
                location_name=data.get("location", {}).get("locationName"),
                currency=data.get("currencyCode", "USD")
            )

        return data

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Maersk API error: {str(e)}")

@router.get("/import-charges", response_model=list[ImportChargeOut])
def list_import_charges(
    status: Optional[str] = Query(None, description="Filter by status (e.g., Safe, Expired, ExpiringSoon)"),
    db: Session = Depends(get_db)
):
    query = db.query(ImportCharge)

    if status:
        query = query.filter(ImportCharge.status == status)

    charges = query.order_by(ImportCharge.last_checked_at.desc()).all()
    return charges

@router.get("/demurrage-risk-report")
def get_risk_report(db: Session = Depends(get_db)):
    charges = db.query(ImportCharge).all()
    scored = [
        {
            "bill_of_lading": c.bill_of_lading,
            "charge_type": c.charge_type,
            "eta": c.eta.isoformat() if c.eta else None,
            "free_time_end": c.free_time_end.isoformat() if c.free_time_end else None,
            "risk_score": calculate_demurrage_risk(c)
        }
        for c in charges
    ]
    return {
        "report_date": datetime.utcnow().date().isoformat(),
        "report": scored
    }


@router.get("/demurrage-risk-summary")
def demurrage_risk_summary(db=Depends(get_db)):
    summary = generate_risk_summary(db)
    return {"summary": summary}