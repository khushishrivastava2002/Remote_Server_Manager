from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import BaseModel, EmailStr
from typing import List
from app.database import settings

# fastapi-mail library to send emails.

router = APIRouter()

# Email Configuration
conf = ConnectionConfig(
    MAIL_USERNAME="shrivastavakhushi419@gmail.com",
    MAIL_PASSWORD="your-password",
    MAIL_FROM="shrivastavakhushi419@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
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
