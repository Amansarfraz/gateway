from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 🔐 Authentication
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


# 🔥 Role-Based Authorization
def role_required(roles: list):
    def checker(user=Depends(get_current_user)):

        if user.get("role") not in roles:
            raise HTTPException(
                status_code=403,
                detail="Access Denied"
            )

        return user
    return checker