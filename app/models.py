from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

from typing import Any
from pydantic_core import core_schema

class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ]),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, value) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return ObjectId(value)

class MongoBaseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# User Models
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserInDB(MongoBaseModel):
    username: str
    email: EmailStr
    hashed_password: str

class UserResponse(MongoBaseModel):
    username: str
    email: EmailStr

# Profile Models
class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: EmailStr
    phone_no: str
    profile_photo_url: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None
    phone_no: Optional[str] = None
    profile_photo_url: Optional[str] = None

class ProfileResponse(ProfileBase, MongoBaseModel):
    pass

# Server Models
class ServerBase(BaseModel):
    name: str
    ip_address: str
    username: str
    port: int = 22

class ServerCreate(ServerBase):
    password: Optional[str] = None
    private_key: Optional[str] = None # Store path or content securely (simplified for now)

class ServerUpdate(BaseModel):
    name: Optional[str] = None
    ip_address: Optional[str] = None
    username: Optional[str] = None
    port: Optional[int] = None
    password: Optional[str] = None
    private_key: Optional[str] = None

class ServerResponse(ServerBase, MongoBaseModel):
    pass

class ServerInDB(ServerBase, MongoBaseModel):
    password: Optional[str] = None
    private_key: Optional[str] = None

# Command Execution Models
class CommandExecute(BaseModel):
    command: str

class CommandLog(MongoBaseModel):
    server_id: str
    command: str
    output: str
    error: str
    exit_status: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Token Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
