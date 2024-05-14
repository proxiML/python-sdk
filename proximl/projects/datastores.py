import json
import logging


class ProjectDatastores(object):
    def __init__(self, proximl, project_id):
        self.proximl = proximl
        self.project_id = project_id

    async def list(self, **kwargs):
        resp = await self.proximl._query(
            f"/project/{self.project_id}/datastores", "GET", kwargs
        )
        datastores = [ProjectDatastore(self.proximl, **datastore) for datastore in resp]
        return datastores

    async def refresh(self):
        await self.proximl._query(f"/project/{self.project_id}/datastores", "PATCH")


class ProjectDatastore:
    def __init__(self, proximl, **kwargs):
        self.proximl = proximl
        self._entity = kwargs
        self._id = self._entity.get("id")
        self._project_uuid = self._entity.get("project_uuid")
        self._name = self._entity.get("name")
        self._type = self._entity.get("type")
        self._region_uuid = self._entity.get("region_uuid")

    @property
    def id(self) -> str:
        return self._id

    @property
    def project_uuid(self) -> str:
        return self._project_uuid

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def region_uuid(self) -> str:
        return self._region_uuid

    def __str__(self):
        return json.dumps({k: v for k, v in self._entity.items()})

    def __repr__(self):
        return f"ProjectDatastore( proximl , **{self._entity.__repr__()})"

    def __bool__(self):
        return bool(self._id)
