from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status
)
from schemas.resource import (
    ResourceInDB,
    ResourcesInResp
)
from crud.resource import (
    get_all_resources_count_in_db,
    get_all_resources_in_db
)
from utils.dependencies import (
    get_if_super_admin
)
router = APIRouter()


@router.get("/", response_model=ResourcesInResp)
async def get_all_resources(
    offset: int = 0,
    limit: int = 10,
    admin_user=Depends(get_if_super_admin)
):
    """
    Returns the list of all resources in DB, and
    total count of resource in DB.
    Available only to super-admin.
    """
    resources = await get_all_resources_in_db(
        offset,
        limit
    )
    count = await get_all_resources_count_in_db()
    return ResourcesInResp(resources=resources, total_count=count)
