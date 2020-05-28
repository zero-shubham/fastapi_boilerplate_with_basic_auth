from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status
)
from typing import List
from utils.dependencies import (
    get_if_super_admin,
    get_current_user
)
from schemas.group import (
    GroupBase,
    GroupsInResp
)
from schemas.common import (
    DeleteResp
)
from crud.group import (
    get_all_groups,
    add_new_group,
    get_user_group_by_name,
    get_user_group_by_id,
    delete_group_in_db,
    get_all_groups_count
)
from uuid import UUID

router = APIRouter()


@router.get("/", response_model=GroupsInResp)
async def get_groups(
    offset: int = 0,
    limit: int = 10,
    current_user=Depends(get_current_user)
):
    """
    Returns the list of user groups available in DB and
    total count of items for this resource in DB.
    """
    groups = await get_all_groups(offset, limit)
    count = await get_all_groups_count()
    return GroupsInResp(groups=groups, total_count=count)


@router.post("/", response_model=GroupBase)
async def add_group(new_group: str, current_user=Depends(get_if_super_admin)):
    """
    Add new group to permissions system.
    """
    group_exists = await get_user_group_by_name(new_group)
    if group_exists:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="Group already exists.")
    group = await add_new_group(new_group)
    return group


@router.delete("/{group_id}", response_model=DeleteResp)
async def delete_group(
    group_id: UUID,
    current_user=Depends(get_if_super_admin)
):
    """
    Delete a specific group by id. Only for super_admin.
    """
    resp = {
        "deleted": None
    }
    group_exists = await get_user_group_by_id(group_id)
    if not group_exists:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="No such group exists."
        )
    deleted = await delete_group_in_db(group_id)
    resp.update(deleted=deleted)
    return resp
