import asyncio
from app.db.session import SessionLocal
from app.services.risk_analysis import generate_and_email_risk_summary

if __name__ == "__main__":
    db = SessionLocal()
    asyncio.run(generate_and_email_risk_summary(db))
