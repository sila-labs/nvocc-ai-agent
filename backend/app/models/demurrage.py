from pydantic import BaseModel

class DemurrageStatus(BaseModel):
    container_number: str
    free_days_remaining: int
    last_free_day: str
    detention_start_date: str
    demurrage_charges: float
    detention_charges: float
    currency: str
