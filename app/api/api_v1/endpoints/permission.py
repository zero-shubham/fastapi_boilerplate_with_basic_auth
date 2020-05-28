from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status
)
from typing import List
from utils.dependencies import (
    get_if_super_admin,
    get_current_user,
    UserHasResourcePermission
)
from uuid import UUID
from schemas.permission import (
    PermissionInResp,
    PermissionBase,
    PermissionsInResp,
    PermissionUpdate
)
from crud.permission import (
    get_all_permissions_in_db,
    get_all_permissions_count_in_db,
    get_permission_by_resource_and_group,
    add_new_permission,
    get_permission_by_id,
    update_permissions_by_id,
    delete_permissions_by_id
)
from permissions_system.constants import (
    InternalTables,
    PermissionTypesEnum
)
from schemas.common import (
    DeleteResp
)

router = APIRouter()


@router.get("/", response_model=PermissionsInResp)
async def get_all_permissions(
    offset: int = 0,
    limit: int = 10,
    admin_user=Depends(get_if_super_admin)
):
    """
    Returns the list of all permissions for each
    combination of user-group and resource, and
    total count of items for this resource in DB.
    Available only to super-admin.
    """
    permissions = await get_all_permissions_in_db(
        offset,
        limit
    )
    count = await get_all_permissions_count_in_db()
    return PermissionsInResp(permissions=permissions, total_count=count)


@router.post("/", response_model=PermissionInResp)
async def create_permission(
    new_permission: PermissionBase,
    admin_user=Depends(get_if_super_admin)
):
    """
    Add CRUD permissions for a combination of
    user-group and resource.
    No check on legitimacy of group, it's assumed.
    Available only to super-admin.
    """
    permission_exists = await get_permission_by_resource_and_group(
        resource=new_permission.resource,
        group=new_permission.group
    )

    if permission_exists:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="Permission for specified group and resouce already exists."
        )
    permission = await add_new_permission(new_permission)
    return permission


@router.put("/{permission_id}", response_model=PermissionInResp)
async def update_permission(
    permission_id: UUID,
    update_permission_data: PermissionUpdate,
    admin_user=Depends(get_if_super_admin)
):
    """
    Update available permissions for a combination of resource and
    user-group.
    """
    permission_exists = await get_permission_by_id(
        _id=permission_id
    )

    if not permission_exists:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Permission record for specified group and resouce does not exists."
        )
    update_data = update_permission_data.dict()
    update_data = {k: v for k, v in update_data.items()
                   if v is not None and k != "id"}
    updated_permission = await update_permissions_by_id(permission_id, update_data)
    return updated_permission


@router.delete("/{permission_id}", response_model=DeleteResp)
async def delete_permission(
    permission_id: UUID,
    admin_user=Depends(get_if_super_admin)
):
    """
    Delete a permissions record for user-group and
    resouce combination. Permission ID is needed.
    """
    resp = {
        "deleted": None
    }
    permission_exists = await get_permission_by_id(
        _id=permission_id
    )

    if not permission_exists:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Permission record for specified group and resouce does not exists."
        )

    deleted = await delete_permissions_by_id(permission_id)
    resp.update(deleted=deleted)
    return resp
