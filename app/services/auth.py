import httpx
import jwt
from jwt.algorithms import RSAAlgorithm
from fastapi import HTTPException, status
from app.config import settings

def get_clerk_public_keys():
    # Why fetch from URL: Clerk rotates keys periodically
    # We always get the current valid keys
    response = httpx.get(settings.CLERK_JWKS_URL)
    jwks = response.json()
    
    public_keys = {}
    for key_data in jwks["keys"]:
        kid = key_data["kid"]  # key ID — matches the JWT header
        public_key = RSAAlgorithm.from_jwk(key_data)
        public_keys[kid] = public_key
    
    return public_keys

def verify_clerk_token(token: str) -> dict:
    try:
        # Why decode header first: we need the kid to pick the right public key
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")

        public_keys = get_clerk_public_keys()

        if kid not in public_keys:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token key"
            )

        # Why RS256: Clerk signs with RSA private key, we verify with public key
        payload = jwt.decode(
            token,
            public_keys[kid],
            algorithms=["RS256"],
            options={"verify_aud": False}
        )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
