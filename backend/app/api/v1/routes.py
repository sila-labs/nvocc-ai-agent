# app/api/v1/routes.py

from fastapi import APIRouter, HTTPException
import requests
from app.models.container import ContainerTracking
from app.services.maersk_client import MaerskAPIClient
from app.services.maersk_token import MaerskTokenManager
import os

router = APIRouter()
client = MaerskAPIClient()

# Ideally load these from environment variables or a config file
CLIENT_ID = os.getenv("MAERSK_CLIENT_ID", "your_consumer_key")
CLIENT_SECRET = os.getenv("MAERSK_CLIENT_SECRET", "your_secret_key")
CUSTOMER_CODE = os.getenv("MAERSK_CUSTOMER_CODE", "your_customer_code")

token_manager = MaerskTokenManager(CLIENT_ID, CLIENT_SECRET)

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

@router.get("/demurrage/{container_number}")
def get_demurrage(container_number: str):
    url = (
        f"https://api.maersk.com/demurrage-detention/v1/import"
        f"?customerCode={CUSTOMER_CODE}&containerNumber={container_number}"
    )
    try:
        response = requests.get(
            url,
            headers={
                **token_manager.get_auth_header(),
                "Content-Type": "application/json"
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Maersk API error: {str(e)}")
