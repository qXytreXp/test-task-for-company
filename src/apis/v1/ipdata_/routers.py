from fastapi import APIRouter
from src.apis.v1.ipdata_.endpoints.ipaddrsdata import ipaddrsdata_router


ipdata_router = APIRouter()
ipdata_router.include_router(ipaddrsdata_router)
