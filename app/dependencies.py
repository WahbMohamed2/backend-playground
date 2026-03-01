from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.auth import verify_clerk_token
from app.models.user import User

# Why HTTPBearer instead of OAuth2PasswordBearer:
# Clerk handles login externally — we only need to read the Bearer token
bearer_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = verify_clerk_token(token)

    # Clerk stores user ID in the "sub" field
    clerk_user_id = payload.get("sub")
    if not clerk_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    # Why store locally: we need owner_id for tasks in our own DB
    # First time we see this Clerk user, we create a local record
    user = db.query(User).filter(User.clerk_id == clerk_user_id).first()
    if not user:
        email = payload.get("email", "")
        username = payload.get("username") or email.split("@")[0]
        user = User(
            clerk_id=clerk_user_id,
            email=email,
            username=username,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user
