from application import ps, database
from schemas.resource import (
    ResourceInDB
)
from typing import List


async def get_all_resources_in_db(
    offset: int = 0,
    limit: int = 10
) -> List[ResourceInDB]:
    query = ps.Resource.select().offset(offset).limit(limit)
    resources = await database.fetch_all(query)
    return resources


async def get_all_resources_count_in_db() -> int:
    query = ps.Resource.count()
    count = await database.execute(query)
    return count
