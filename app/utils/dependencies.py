from fastapi import (
    HTTPException,
    Security,
    status
)
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from schemas.token import TokenPayload
from core.config import SECRET_KEY
from core.jwt import ALGORITHM
from crud.user import find_user_by_id
from crud.token import check_token_in_db
from enum import Enum
from application import ps
from permissions_system.constants import PermissionTypesEnum


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    token_is_valid = await check_token_in_db(token_data.user_id, token)
    if not token_is_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    user = await find_user_by_id(user_id=token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


async def get_if_super_admin(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    token_is_valid = await check_token_in_db(token_data.user_id, token)
    if not token_is_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    if not token_data.group == "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorised for this operation."
        )
    user = await find_user_by_id(user_id=token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


class UserHasResourcePermission:
    def __init__(
        self,
        resource: str,
        permission_type: PermissionTypesEnum
    ):
        self.resource = resource
        self.permission_type = permission_type

    async def __call__(self, token: str = Security(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            token_data = TokenPayload(**payload)
        except PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials"
            )
        token_is_valid = await check_token_in_db(token_data.user_id, token)
        if not token_is_valid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials"
            )
        result = await ps.user_has_permissions(
            token_data.user_id, self.resource, self.permission_type)
        return result
