import logging
from typing import List
from datetime import datetime

import uvicorn
import converter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi import (
    FastAPI,
    status,
    Response,
    Depends,
    File,
    UploadFile
)

from conf import settings
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

    @app.get('/read/hosts/group/{group}', response_model=List[schemas.Host])
    async def get_host(group: str, db_host: manager.DBHost = Depends(db.get_connection)):
        return await db_host.get_host_by_group(group)

    @app.get('/read/host/{host_name}', response_model=schemas.Host)
    async def get_host(host_name: str, db_host: manager.DBHost = Depends(db.get_connection)):
        return await db_host.get_host_by_host_name(host_name)

    @app.post('/upsert/host', response_model=str, status_code=status.HTTP_200_OK)
    async def upsert_host(host: schemas.Host, db_host: manager.DBHost = Depends(db.get_connection)):
        await db_host.upsert_host(host)
        logging.debug(f'host created | {host}')
        return PlainTextResponse(f"host {host.host_name} update/created with successful")

    @app.post('/delete/host/host_name/{host_name}', response_model=str, status_code=status.HTTP_200_OK)
    async def delete_host(host_name: str, db_host: manager.DBHost = Depends(db.get_connection)):
        await db_host.delete_host_by_host_name(host_name)
        logging.debug(f'host deleted | {host_name}')
        return PlainTextResponse(f"host {host_name} deleted with successful")

    @app.post('/import/hosts', response_model=schemas.Host)
    async def import_hosts(db_host: manager.DBHost = Depends(db.get_connection), file: UploadFile = File(...)):
        file_bytes = await file.read()
        csv_content = file_bytes.decode('utf-8')
        hosts = converter.read_csv(csv_content)
        for host in hosts:
            await db_host.upsert_host(host)
            logging.debug(f'host created | {host}')

    @app.get('/export/hosts', response_model=schemas.Host)
    async def export_hosts(db_host: manager.DBHost = Depends(db.get_connection)):
        hosts = await db_host.get_hosts()
        csv_memory_file = converter.generate_csv(hosts)

        response = Response(content=csv_memory_file.getvalue(), media_type="text/csv")
        dt_now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        response.headers["Content-Disposition"] = f"attachment; filename=list-equips-{dt_now}.csv"

        return response


def run():
    app = FastAPI(root_path=settings['URI_ROOT_PATH'])
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
        host=settings['BIND_ADDRESS'],
        port=settings['BIND_PORT'],
        log_config=None
    )
