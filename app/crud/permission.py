from typing import List
from uuid import uuid4, UUID
from application import database, ps
from schemas.permission import (
    PermissionInResp,
    PermissionBase
)


async def add_new_permission(
        add_new_permission: PermissionBase) -> PermissionInResp:
    query = ps.Permission.insert()
    values = {
        "id": uuid4(),
        **add_new_permission.dict()
    }
    await database.execute(query=query, values=values)
    return values


async def get_all_permissions_in_db(
    offset: int = 0,
    limit: int = 10
) -> List[PermissionInResp]:
    query = ps.Permission.select().offset(offset).limit(limit)
    permissions = await database.fetch_all(query)
    return permissions


async def get_all_permissions_count_in_db() -> int:
    query = ps.Permission.count()
    count = await database.execute(query)
    return count


async def get_permission_by_resource_and_group(
    resource: str,
    group: str
) -> PermissionInResp:
    query = ps.Permission.select().where(
        ps.Permission.columns.group == group
    ).where(
        ps.Permission.columns.resource == resource
    )
    permission = await database.fetch_one(query)
    return permission


async def get_permission_by_id(_id: UUID) -> PermissionInResp:
    query = ps.Permission.select().where(
        ps.Permission.columns.id == _id
    )
    permission = await database.fetch_one(query)
    return permission


async def update_permissions_by_id(_id: UUID, values: dict) -> PermissionInResp:
    query = ps.Permission.update().where(
        ps.Permission.columns.id == _id
    )
    await database.execute(query, values)
    permission = await get_permission_by_id(_id)
    return permission


async def delete_permissions_by_id(_id: UUID) -> bool:
    query = ps.Permission.delete().where(
        ps.Permission.columns.id == _id
    )
    await database.execute(query)
    exists = await get_permission_by_id(_id)
    return True if not exists else False
