from pydantic import BaseModel

class ContainerTracking(BaseModel):
    container_number: str
    carrier: str
    status: str
    location: str
    eta: str