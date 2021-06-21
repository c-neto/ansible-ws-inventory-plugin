import logging
from typing import List
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase
)
import schemas
from db import manager


class RepoHost(manager.DBHost):
    def __init__(self, url: str):
        self.url = url
        self._client: AsyncIOMotorClient = None
        self._db: AsyncIOMotorDatabase = None

    async def connect_to_database(self):
        logging.debug("Connecting to MongoDB")
        self._client = AsyncIOMotorClient(
            self.url,
            maxPoolSize=10,
            minPoolSize=10
        )
        self._db = self._client.main_db
        logging.debug("Connected to MongoDB")

    async def close_database_connection(self):
        logging.info("Closing connection with MongoDB")
        self._client.close()
        logging.info("Closed connection with MongoDB")

    async def get_hosts(self) -> List[schemas.Host]:
        return [schemas.Host(**host) async for host in self._db.hosts.find()]

    async def get_host_by_group(self, group: str) -> List[schemas.Host]:
        hosts = self._db.hosts.find({'group': group})
        return [schemas.Host(**host) async for host in hosts]

    async def get_host_by_host_name(self, host_name: str) -> schemas.Host:
        host_q = await self._db.hosts.find_one({'host_name': host_name})
        if host_q:
            return schemas.Host(**host_q)
        else:
            raise ValueError('host not found')

    async def delete_host_by_host_name(self, host_name: str):
        await self._db.hosts.delete_one(
            {'host_name': host_name},
        )

    async def upsert_host(self, host: schemas.Host):
        await self._db.hosts.replace_one(
            {'host_name': host.host_name},
            host.dict(),
            upsert=True
        )
