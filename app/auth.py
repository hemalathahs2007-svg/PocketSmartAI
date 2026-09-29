from datetime import datetime, timedelta, timezone
from hashlib import sha256
import hmac
import secrets
import jwt
from fastapi import Request
from .config import SECRET_KEY

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = sha256((salt + password).encode()).hexdigest()
    return f"sha256${salt}${digest}"

def verify_password(password: str, stored: str) -> bool:
    try:
        algorithm, salt, expected = stored.split("$", 2)
        if algorithm != "sha256":
            return False
        actual = sha256((salt + password).encode()).hexdigest()
        return hmac.compare_digest(actual, expected)
    except ValueError:
        return False

def create_access_token(user_id: int) -> str:
    payload = {"sub": str(user_id),
               "exp": datetime.now(timezone.utc) + timedelta(hours=12)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def get_user_id_from_request(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return int(data["sub"])
    except (jwt.PyJWTError, TypeError, ValueError):
        return None
