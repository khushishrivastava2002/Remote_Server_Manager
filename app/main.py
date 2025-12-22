
from fastapi import FastAPI
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import auth, users, servers, email

app = FastAPI(title="Remote Server Manager API")

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, tags=["Users"])
app.include_router(servers.router, tags=["Servers"])
app.include_router(email.router, prefix="/email", tags=["Email"])

@app.get("/")
async def root():
    return {"message": "Welcome to Remote Server Manager API"}
