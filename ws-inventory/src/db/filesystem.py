import json
from pathlib import Path
from typing import List
import schemas
from db import manager


class RepoHost(manager.DBHost):
    def __init__(self, file: str):
        self.file = Path(file)
        if not self.file.exists():
            self.file.write_text(json.dumps([]))

    async def connect_to_database(self):
        pass

    async def close_database_connection(self):
        pass

    async def get_hosts(self) -> List[schemas.Host]:
        hosts = json.loads(self.file.read_text())
        return [schemas.Host(**host) for host in hosts]

    async def get_host_by_host_name(self, host_name: str) -> schemas.Host:
        hosts_json = json.loads(self.file.read_text())
        hosts = [schemas.Host(**host) for host in hosts_json]

        hosts = list(filter(lambda v: v.host_name == host_name, hosts))

        if not hosts:
            raise ValueError('host not found')

        return hosts[0]

    async def delete_host_by_host_name(self, host_name: str):
        hosts_json = json.loads(self.file.read_text())
        hosts = [schemas.Host(**host) for host in hosts_json]
        hosts_reduced = list(filter(lambda v: v.host_name != host_name, hosts))
        hosts_json_without_object_delete = json.dumps([host.json() for host in hosts_reduced])
        self.file.write_text(hosts_json_without_object_delete)

    async def upsert_host(self, host: schemas.Host):
        hosts_json = json.loads(self.file.read_text())
        hosts = [schemas.Host(**host) for host in hosts_json]
        hosts_reduced = list(filter(lambda v: v.host_name != host.host_name, hosts))
        hosts_reduced.append(host)
        hosts_json_with_new_object = json.dumps([host.dict() for host in hosts_reduced])
        self.file.write_text(hosts_json_with_new_object)
