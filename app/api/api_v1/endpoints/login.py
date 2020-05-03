from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from crud.user import find_user_by_email
from core.jwt import create_access_token
from schemas.token import (
    LoginResponse,
    TokenPayload,
    LogoutResponse,
    Logout,
    ValidateResponse,
    LoginForm
)
from crud.token import (
    add_token_in_db,
    remove_token_in_db
)
from utils.dependencies import (
    get_current_user
)

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    resp = {
        "access_token": "",
        "token_type": ""
    }
    user = await find_user_by_email(form_data.username)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    encoded_jwt, expire = create_access_token(data=TokenPayload(
        user_id=str(user.get("id")), user_group=user.get("group")).dict())
    added_token_in_db = await add_token_in_db(
        user_id=user.get("id"),
        token=encoded_jwt.decode("utf-8")
    )
    if encoded_jwt and expire and added_token_in_db:
        resp.update(
            access_token=encoded_jwt.decode("utf-8"),
            token_type="bearer"
        )
    return resp


@router.post("/logout", response_model=LogoutResponse)
async def logout_user(
    current_user=Depends(get_current_user)
):
    resp = {
        "logged_out": False
    }
    logged_out = await remove_token_in_db(current_user[0])
    if logged_out >= 0:
        resp.update(logged_out=True)
    return resp


@router.get("/validate", response_model=ValidateResponse)
async def validate(
    current_user=Depends(get_current_user)
):
    resp = {
        "valid": True
    }
    if not current_user[0]:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED
        )
        resp.update(valid=False)
    return resp
