import time

from typing import Any

from fastapi import FastAPI, Request

from src.db import mysql_db
from src.apps.auth.models import User
from src.apps.ipdata_.models import (
    Task, 
    IpAddressData,
    Asn, 
    Languages, 
    Currency, 
    TimeZone, 
    Threat 
)

from src.apis.v1.routers import v1_router


app = FastAPI()
app.include_router(v1_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next) -> Any:
    start_time = time.time()

    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


@app.on_event("startup")
async def startup() -> None:
    mysql_db.connect(reuse_if_open=True)

    mysql_db.create_tables([
        User,
        Task,
        IpAddressData,
        Asn, 
        Languages,
        Languages, 
        Currency, 
        TimeZone, 
        Threat,
    ])


@app.on_event("shutdown")
async def shutdown() -> None:
    mysql_db.close()
