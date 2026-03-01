from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

# Why this endpoint: frontend apps need a way to fetch the logged-in user's profile
# The token tells us WHO, this endpoint returns the full profile
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    # Why no DB call here: get_current_user already fetched the user from DB
    return current_user
