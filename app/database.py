from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb+srv://shrivastavakhushi419_db_user:jDvt29ZU2A6CXsXN@cluster0.jlamjt7.mongodb.net/?appName=Cluster0"
    DB_NAME: str = "server_manager_db"
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def get_database():
    return db.client[settings.DB_NAME]

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    print("Connected to MongoDB")

async def close_mongo_connection(): 
    db.client.close()
    print("Closed MongoDB connection")
