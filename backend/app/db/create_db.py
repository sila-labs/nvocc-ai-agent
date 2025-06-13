# app/db/create_db.py

from app.db.session import engine
from app.models.import_charges import ImportCharge, Base

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
