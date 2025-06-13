# app/models/import_charges.py

from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ImportCharge(Base):
    __tablename__ = "import_charges"

    id = Column(Integer, primary_key=True, index=True)
    bill_of_lading = Column(String, index=True)
    container_number = Column(String)
    charge_type = Column(String)  # 'DMR' or 'DET'
    is_final_charge = Column(Boolean, default=False)

    estimated_last_free_date = Column(Date, nullable=True)
    actual_last_free_date = Column(Date, nullable=True)
    currency = Column(String, default="USD")
    location_name = Column(String, nullable=True)

    status = Column(String, default="Pending")  # Safe, ExpiringSoon, Expired, Unknown

    last_checked_at = Column(DateTime, default=datetime.utcnow)
