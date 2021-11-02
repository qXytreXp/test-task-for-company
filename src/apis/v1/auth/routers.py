from fastapi import APIRouter
from src.apis.v1.auth.endpoints.auth_ import auth_router_


auth_router = APIRouter()
auth_router.include_router(auth_router_)
