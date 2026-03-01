from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr      # Why EmailStr: validates format (has @, has domain)
    username: str        # before it even reaches your DB
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    created_at: datetime

    # Why here but not in UserCreate: UserCreate reads from a dict (JSON body)
    # UserResponse reads from a SQLAlchemy object — needs attribute access
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str