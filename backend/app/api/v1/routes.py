# backend/app/api/v1/routes.py

from fastapi import APIRouter, HTTPException, Query
import requests
from typing import Optional
from app.models.container import ContainerTracking
from app.services.maersk_client import MaerskAPIClient
from app.services.maersk_token import MaerskTokenManager
from app import config  # ✅ import config variables
from datetime import date

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
    chargesEndDate: Optional[str] = Query(None)
):
    if charge_type not in ["DMR", "DET"]:
        raise HTTPException(status_code=400, detail="Invalid charge_type. Use 'DMR' or 'DET'.")

    url = (
        f"https://api.maersk.com/shipping-charges/import/{charge_type}"
        f"?billOfLadingNumber={billOfLadingNumber}"
        f"&carrierCustomerCode={config.MAERSK_CUSTOMER_CODE}"
        f"&carrierCode={config.MAERSK_CARRIER_CODE}"
    )

    if chargesEndDate:
        url += f"&chargesEndDate={chargesEndDate}"

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
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Maersk API error: {str(e)}")
