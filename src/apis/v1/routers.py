from fastapi import APIRouter

from src.apis.v1.auth.routers import auth_router
from src.apis.v1.ipdata_.routers import ipdata_router


v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(auth_router)
v1_router.include_router(ipdata_router)
