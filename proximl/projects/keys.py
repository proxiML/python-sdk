import json
import logging
from datetime import datetime
from dateutil import parser, tz


class ProjectKeys(object):
    def __init__(self, proximl, project_id):
        self.proximl = proximl
        self.project_id = project_id

    async def list(self, **kwargs):
        resp = await self.proximl._query(
            f"/project/{self.project_id}/keys", "GET", kwargs
        )
        keys = [ProjectKey(self.proximl, **service) for service in resp]
        return keys

    async def put(self, type, key_id, secret, tenant=None, **kwargs):
        data = dict(key_id=key_id, secret=secret, tenant=tenant)
        payload = {k: v for k, v in data.items() if v is not None}
        logging.info(f"Creating Project Key {type}")
        resp = await self.proximl._query(
            f"/project/{self.project_id}/key/{type}", "PUT", None, payload
        )
        key = ProjectKey(self.proximl, **resp)
        logging.info(f"Created Project Key {type} in project {self.project_id}")

        return key

    async def remove(self, type, **kwargs):
        await self.proximl._query(
            f"/project/{self.project_id}/key/{type}", "DELETE", kwargs
        )


class ProjectKey:
    def __init__(self, proximl, **kwargs):
        self.proximl = proximl
        self._entity = kwargs
        self._type = self._entity.get("type")
        self._project_uuid = self._entity.get("project_uuid")
        self._key_id = self._entity.get("key_id")
        self._updated_at = self._entity.get("updatedAt")

    @property
    def type(self) -> str:
        return self._type

    @property
    def project_uuid(self) -> str:
        return self._project_uuid

    @property
    def key_id(self) -> str:
        return self._key_id

    @property
    def updated_at(self) -> datetime:
        timestamp = parser.isoparse(self._updated_at)
        timezone = tz.tzlocal()
        return timestamp.astimezone(timezone)

    def __str__(self):
        return json.dumps({k: v for k, v in self._entity.items()})

    def __repr__(self):
        return f"ProjectKey( proximl , **{self._entity.__repr__()})"

    def __bool__(self):
        return bool(self._type)
