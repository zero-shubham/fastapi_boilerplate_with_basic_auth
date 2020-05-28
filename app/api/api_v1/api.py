from fastapi import APIRouter
from api.api_v1.endpoints import user
from api.api_v1.endpoints import login
from api.api_v1.endpoints import group
from api.api_v1.endpoints import permission
from api.api_v1.endpoints import customer


api_router = APIRouter()

api_router.include_router(
    user.router,
    prefix="/users",
    tags=["users"]
)
api_router.include_router(
    login.router,
    tags=["authentication"]
)
api_router.include_router(
    group.router,
    prefix="/groups",
    tags=["groups"]
)
api_router.include_router(
    permission.router,
    prefix="/permissions",
    tags=["permissions"]
)
api_router.include_router(
    customer.router,
    prefix="/customers",
    tags=["customers"]
)