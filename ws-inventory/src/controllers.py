from typing import List

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi import (
    FastAPI,
    status,
    Depends
)

import os
import schemas
import db
from db import manager


def exception_handlers(app: FastAPI):
    async def validation_request(_, exc):
        return PlainTextResponse(str(exc), status_code=status.HTTP_400_BAD_REQUEST)

    @app.exception_handler(Exception)
    async def internal_server_error(_, exc):
        return PlainTextResponse(str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def db_connection(app: FastAPI):
    @app.on_event("startup")
    async def startup():
        await db.connection.connect_to_database()

    @app.on_event("shutdown")
    async def shutdown():
        await db.connection.close_database_connection()


def routes_host(app: FastAPI):
    @app.get('/read/hosts', response_model=List[schemas.Host])
    async def get_hosts(db_host: manager.DBHost = Depends(db.get_connection)):
        return await db_host.get_hosts()

    @app.get('/read/host/{hostname}', response_model=schemas.Host)
    async def get_host(hostname: str, db_host: manager.DBHost = Depends(db.get_connection)):
        return await db_host.get_host_by_host_name(hostname)

    @app.post('/upsert/host', response_model=schemas.Host, status_code=status.HTTP_200_OK)
    async def upsert_host(host: schemas.Host, db_host: manager.DBHost = Depends(db.get_connection)):
        await db_host.upsert_host(host)

    @app.post('/delete/host/host_name/{host_name}', response_model=schemas.Host, status_code=status.HTTP_200_OK)
    async def delete_host(host_name: str, db_host: manager.DBHost = Depends(db.get_connection)):
        await db_host.delete_host_by_host_name(host_name)


def run():
    app = FastAPI(root_path=os.getenv('ROOT_PATH', "/"))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    exception_handlers(app)

    db_connection(app)
    routes_host(app)

    uvicorn.run(
        app,
        host=os.getenv('BIND_ADDRESS', '0.0.0.0'),
        port=os.getenv('BIND_PORT', 5000),
        log_config=None
    )
