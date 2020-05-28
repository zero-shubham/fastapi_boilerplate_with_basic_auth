from application import database, ps
from schemas.group import GroupBase
from typing import List
from uuid import uuid4, UUID


async def add_new_group(new_group: str) -> GroupBase:
    query = ps.UserGroup.insert()
    values = {
        "id": uuid4(),
        "group": new_group
    }
    await database.execute(query=query, values=values)
    return values


async def get_all_groups(offset: int = 0, limit: int = 10) -> List[GroupBase]:
    query = ps.UserGroup.select().offset(offset).limit(limit)
    groups = []
    groups = await database.fetch_all(query)
    return groups


async def get_all_groups_count() -> int:
    query = ps.UserGroup.count()
    count = await database.execute(query)
    return count


async def get_user_group_by_name(group: str) -> GroupBase:
    query = ps.UserGroup.select().where(ps.UserGroup.columns.group == group)
    group = await database.fetch_one(query)
    return group


async def get_user_group_by_id(group_id: UUID) -> GroupBase:
    query = ps.UserGroup.select().where(ps.UserGroup.columns.id == group_id)
    group = await database.fetch_one(query)
    return group


async def delete_group_in_db(group_id: UUID) -> bool:
    query = ps.UserGroup.delete().where(ps.UserGroup.columns.id == group_id)
    await database.execute(query)
    exists = await get_user_group_by_id(group_id)
    return True if not exists else False
