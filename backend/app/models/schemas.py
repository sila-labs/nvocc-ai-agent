# app/models/schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ImportChargeOut(BaseModel):
    id: int
    bill_of_lading: str
    container_number: str
    charge_type: str
    is_final_charge: bool
    estimated_last_free_date: Optional[date]
    actual_last_free_date: Optional[date]
    location_name: Optional[str]
    currency: str
    status: str
    last_checked_at: datetime

    class Config:
        orm_mode = True
