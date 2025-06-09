from fastapi import APIRouter
from models.container import ContainerTracking

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "running"}

@router.get("/track/{container_id}", response_model=ContainerTracking)
def get_container_status(container_id: str):
    return ContainerTracking(
        container_number=container_id,
        carrier="Maersk",
        status="In Transit",
        location="Port of Rotterdam",
        eta="2024-06-15T12:00:00Z"
    )
