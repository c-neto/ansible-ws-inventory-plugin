import schemas
import typing
import abc


class DBConnection:
    @abc.abstractmethod
    async def connect_to_database(self):
        pass

    @abc.abstractmethod
    async def close_database_connection(self):
        pass


class DBHost(DBConnection):
    @abc.abstractmethod
    async def get_hosts(self) -> typing.List[schemas.Host]:
        pass

    @abc.abstractmethod
    async def delete_host_by_host_name(self, host_name: str):
        pass

    @abc.abstractmethod
    async def get_host_by_host_name(self, host_name) -> schemas.Host:
        pass

    @abc.abstractmethod
    async def upsert_host(self, host: schemas.Host):
        pass
