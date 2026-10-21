from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from shrinkr.config import settings

_bearer_scheme = HTTPBearer()


def create_access_token(user_id: UUID) -> str:
    """Issue a signed JWT identifying user_id."""
    app_settings = settings()
    expire = datetime.now(timezone.utc) + timedelta(minutes=app_settings.jwt_expire_minutes)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, app_settings.jwt_secret_key, algorithm=app_settings.jwt_algorithm)


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
) -> UUID:
    """Resolve the authenticated user id from the bearer token, or raise 401."""
    app_settings = settings()
    try:
        payload = jwt.decode(
            credentials.credentials,
            app_settings.jwt_secret_key,
            algorithms=[app_settings.jwt_algorithm],
        )
        return UUID(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error
