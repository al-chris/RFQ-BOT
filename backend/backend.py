
from fastapi import FastAPI
from email_monitor import check_email
from rfq_generator import generate_rfq_table
from models import SessionLocal, Email
import asyncio

app = FastAPI()

ongoing_tasks = []
completed_tasks = []

@app.get("/")
async def index():
    return {"tasks": ongoing_tasks}

@app.get("/process_emails")
async def process_emails():
    global ongoing_tasks, completed_tasks
    emails = check_email()
    for email in emails[-2:]:
        rfq = generate_rfq_table(email)
        await asyncio.sleep(2)
        task = {
            'subject': email['subject'],
            'rfq': rfq,
            'status': 'Completed'
        }
        ongoing_tasks.append(task)
        completed_tasks.append(task)

    ongoing_tasks.clear()
    return {"message": "Emails processed!"}

@app.get("/completed_tasks")
async def completed_tasks_view():
    return {"tasks": completed_tasks}

@app.get("/emails/")
async def get_emails():
    session = SessionLocal()
    emails = session.query(Email).all()
    session.close()

    return [{
        "email_id": email.id,
        "subject": email.subject, 
        "body": email.body, 
        "template_table": email.template_table,
        "template_json": email.template_json
    } for email in emails]

@app.get("/emails/{email_id}")
async def get_email(email_id: str):
    session = SessionLocal()
    email = session.query(Email).filter_by(id=email_id).first()
    session.close()

    return {
        "subject": email.subject, 
        "body": email.body, 
        "template_table": email.template_table,
        "template_json": email.template_json
    }

@app.get("/all-ids")
async def get_all_ids():
    session = SessionLocal()
    emails = session.query(Email).all()
    session.close()

    return [email.id for email in emails]

@app.get("/check-emails")
async def check_emails():
    emails = check_email()
    return emails