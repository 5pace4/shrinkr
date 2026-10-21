from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from shrinkr.services.auth_service import create_access_token, get_current_user_id


def _credentials(token: str) -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


def test_create_and_decode_access_token_roundtrip():
    user_id = uuid4()
    token = create_access_token(user_id)
    assert get_current_user_id(_credentials(token)) == user_id


def test_invalid_token_raises_401():
    with pytest.raises(HTTPException) as exc_info:
        get_current_user_id(_credentials("not-a-real-token"))
    assert exc_info.value.status_code == 401
