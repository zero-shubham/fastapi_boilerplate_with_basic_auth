from fastapi import APIRouter
from api.api_v1.endpoints import user
from api.api_v1.endpoints import login


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
