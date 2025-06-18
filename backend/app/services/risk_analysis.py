from datetime import datetime
from datetime import date
import openai
from app.models.import_charges import ImportCharge
import os
from app.utils.emailer import send_risk_email
import asyncio

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_and_email_risk_summary(db):
    today = date.today()
    charges = db.query(ImportCharge).filter(ImportCharge.risk_level != "Low").all()

    if not charges:
        summary = "No urgent demurrage risks today."
    else:
        prompt = "Summarize these demurrage risks:\n"
        for c in charges:
            prompt += f"- BOL: {c.bill_of_lading}, Type: {c.charge_type}, Days Left: {c.days_remaining}, Risk: {c.risk_level}\n"
        prompt += "\nBrief summary for logistics team."

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            summary = response.choices[0].message.content.strip()
        except Exception as e:
            summary = f"LLM summarization failed: {e}"

    subject = f"🚨 Daily Demurrage Risk Summary – {today.strftime('%B %d, %Y')}"
    await send_risk_email(subject, summary)
    return summary

def calculate_demurrage_risk(charge_entry):
    today = datetime.utcnow().date()
    eta = charge_entry.eta.date() if charge_entry.eta else None
    free_end = charge_entry.free_time_end.date() if charge_entry.free_time_end else None

    risk_score = 0

    if eta and eta <= today:
        risk_score += 1

    if free_end:
        days_left = (free_end - today).days
        if days_left < 3:
            risk_score += 1
        if days_left < 0:
            risk_score += 2

    return risk_score

def generate_risk_summary(db):
    today = date.today()
    charges = db.query(ImportCharge).filter(ImportCharge.risk_level != "Low").all()

    if not charges:
        return "No urgent demurrage risks today."

    # Build summary input
    prompt = "Summarize the following container demurrage risks into a concise operations alert:\n"
    for c in charges:
        prompt += f"- BOL: {c.bill_of_lading}, Type: {c.charge_type}, Days Left: {c.days_remaining}, Risk: {c.risk_level}\n"

    prompt += "\nGenerate a 2-3 sentence summary suitable for a logistics team."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or gpt-3.5-turbo
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM summarization failed: {e}"


