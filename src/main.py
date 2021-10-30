import time
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from pydantic import BaseModel, validator
from ipaddress import ip_address

from celery.result import AsyncResult

from src.tasks import get_ip_data_task
from src.db import mysql_db
from src.models import (
    Task, 
    IpAddressDataAsn, 
    IpAddressDataLanguages, 
    IpAddressDataCurrency, 
    IpAddressDataTimeZone, 
    IpAddressDataThreat
)
from src.celery_ import celery_app


class IpAddressSchema(BaseModel):
    ip: str = "69.78.70.14"

    @validator("ip")
    def check_ip_validity(cls, value: str) -> str:
        return str(ip_address(value))


app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next) -> Any:
    start_time = time.time()

    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


@app.post("/task")
async def create_task_for_getting_ip_data(data: IpAddressSchema) -> JSONResponse:
    ip = data.ip
    celery_task_id = get_ip_data_task.delay(ip).id
    task_model = Task.create(celery_task_id=str(celery_task_id))

    return JSONResponse({"task_id": task_model.id}, status_code=200)


@app.get("/status/{task_id}")
async def result_task(task_id: int) -> JSONResponse:
    task = Task.get(id=task_id)
    task_result = AsyncResult(task.celery_task_id, app=celery_app)

    return JSONResponse(task_result.get(), status_code=200)


@app.on_event("startup")
async def startup() -> None:
    mysql_db.connect(reuse_if_open=True)
    mysql_db.create_tables((
        Task, 
        IpAddressDataAsn, 
        IpAddressDataLanguages, 
        IpAddressDataCurrency, 
        IpAddressDataTimeZone, 
        IpAddressDataThreat,
    ))


@app.on_event("shutdown")
async def shutdown() -> None:
    mysql_db.close()
