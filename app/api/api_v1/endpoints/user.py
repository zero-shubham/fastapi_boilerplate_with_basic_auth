from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status
)
from typing import List
from schemas.user import (
    UserInResp,
    UserInDB,
    UserInDbUpdate,
    UsersInResp
)
from crud.user import (
    find_user_by_id,
    create_new_user,
    get_all_users,
    update_user_in_db,
    delete_user_in_db,
    get_all_users_count
)
from utils.dependencies import (
    get_current_user
)
from uuid import UUID
from application import ps
from permissions_system.constants import (
    InternalTables,
    PermissionTypesEnum
)
from schemas.common import (
    DeleteResp
)

router = APIRouter()


@router.get("/{user_id}", response_model=UserInResp)
async def get_user_by_id(
    user_id: UUID,
    current_user=Depends(get_current_user)
):
    """
    Get a specific user by id
    """

    user = await find_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.")
    return UserInResp(**user)


@router.get("/", response_model=UsersInResp)
async def get_users(
    offset: int = 0,
    limit: int = 10,
    current_user=Depends(get_current_user)
):
    """
    Get list of all users and
    total count of items for this resource in DB.
    """
    users = await get_all_users(offset, limit)
    count = await get_all_users_count()

    return UsersInResp(users=users, total_count=count)


@router.post("/", response_model=UserInResp)
async def create_user(user_in: UserInDB, current_user=Depends(get_current_user)):
    """
    Create new user.
    """
    user_id = await create_new_user(user_in)
    user = await find_user_by_id(user_id)
    return user


@router.put("/{user_id}", response_model=UserInResp)
async def update_user(
        user_id: UUID,
        user_in: UserInDbUpdate,
        current_user=Depends(get_current_user)):
    """
    Update specific user details.
    """
    user = await update_user_in_db(user_id, user_in)
    return user


@router.delete("/{user_id}", response_model=DeleteResp)
async def delete_user(
    user_id: UUID,
    current_user=Depends(get_current_user)
):
    """
    Delete specific user.
    """
    resp = {
        "deleted": None
    }
    if current_user["id"] != user_id and \
            current_user["group"] != "super_admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            "You are not authorised for this operation.")

    deleted = await delete_user_in_db(user_id)
    resp.update(deleted=deleted)
    return resp
