from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse

from src.apps.ipdata_.schemas import IpAddressSchema, IpAddressDataSchema

from src.apps.ipdata_.services.schemas import \
    peewee_ipdata_model_to_pydantic_schema
from src.apps.ipdata_.services.ipdata import (
    create_task_for_getting_data_about_ip,
    ipaddrs_exists_in_db,
    get_task_model_by_ipdata_ip,
    get_task_model_by_id
)
from src.apps.auth.services.auth import check_user_auth
from src.apis.v1.auth.endpoints.auth_ import security



ipaddrsdata_router = APIRouter(
    tags=["IPData"],
    dependencies=[Depends(check_user_auth)]
)


@ipaddrsdata_router.post("/task")
async def create_task_for_getting_ip_data(
    data: IpAddressSchema,
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> JSONResponse:

    ip = data.ip
    
    if not ipaddrs_exists_in_db(ip=ip):
        task_model = create_task_for_getting_data_about_ip(ip)
    else:
        task_model = get_task_model_by_ipdata_ip(ip)
    
    return JSONResponse({"task_id": task_model.id}, status_code=200)


@ipaddrsdata_router.get(
    "/status/{task_id}", 
    response_model=IpAddressDataSchema,
)
async def result_task(
    task_id: int, 
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> JSONResponse:
    task_model = get_task_model_by_id(task_id)
    ipdata_model = task_model.ipdata
    ipdata_schema = peewee_ipdata_model_to_pydantic_schema(ipdata_model)

    return JSONResponse({
        "id": task_id, 
        "task_result": ipdata_schema.dict()
    }, status_code=200)
