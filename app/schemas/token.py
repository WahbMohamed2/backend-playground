from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str  # always "bearer"

class TokenData(BaseModel):
    # What we extract FROM the token after decoding it
    user_id: int | None = None
