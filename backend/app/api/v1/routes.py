# app/api/v1/routes.py

from fastapi import APIRouter, HTTPException
from app.models.container import ContainerTracking
from app.services.maersk_client import MaerskAPIClient

router = APIRouter()
client = MaerskAPIClient()

@router.get("/health")
def health():
    return {"status": "running"}

@router.get("/track/{container_id}", response_model=ContainerTracking)
def get_container_status(container_id: str):
    try:
        data = client.track_container(container_id)

        # Adapt this mapping depending on Maersk’s actual response schema
        return ContainerTracking(
            container_number=data["containerNumber"],
            carrier="Maersk",
            status=data["status"],
            location=data["location"],
            eta=data["eta"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
