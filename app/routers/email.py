from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import BaseModel, EmailStr
from typing import List
from app.database import settings

# fastapi-mail library to send emails.

router = APIRouter()

# Email Configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)

class EmailSchema(BaseModel):
    email: List[EmailStr]
    subject: str
    body: str

@router.post("/send")
async def send_email(email: EmailSchema, background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject=email.subject,
        recipients=email.email,
        body=email.body,
        subtype=MessageType.html
    )
    
    fm = FastMail(conf)
    
    try:
        background_tasks.add_task(fm.send_message, message)
        return {"message": "Email has been scheduled to be sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
