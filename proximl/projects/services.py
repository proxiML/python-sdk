import json
import logging


class ProjectServices(object):
    def __init__(self, proximl, project_id):
        self.proximl = proximl
        self.project_id = project_id

    async def get(self, id, **kwargs):
        resp = await self.proximl._query(
            f"/project/{self.project_id}/services/{id}", "GET", kwargs
        )
        return ProjectService(self.proximl, **resp)

    async def list(self, **kwargs):
        resp = await self.proximl._query(
            f"/project/{self.project_id}/services", "GET", kwargs
        )
        services = [ProjectService(self.proximl, **service) for service in resp]
        return services

    async def refresh(self):
        await self.proximl._query(f"/project/{self.project_id}/services", "PATCH")


class ProjectService:
    def __init__(self, proximl, **kwargs):
        self.proximl = proximl
        self._entity = kwargs
        self._id = self._entity.get("id")
        self._project_uuid = self._entity.get("project_uuid")
        self._name = self._entity.get("name")
        self._hostname = self._entity.get("hostname")
        self._public = self._entity.get("public")
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
    def hostname(self) -> str:
        return self._hostname

    @property
    def public(self) -> bool:
        return self._public

    @property
    def region_uuid(self) -> str:
        return self._region_uuid

    def __str__(self):
        return json.dumps({k: v for k, v in self._entity.items()})

    def __repr__(self):
        return f"ProjectService( proximl , **{self._entity.__repr__()})"

    def __bool__(self):
        return bool(self._id)

    async def enable(self):
        await self.proximl._query(
            f"/project/{self._project_uuid}/services/{self._id}/enable", "PATCH"
        )

    async def disable(self):
        await self.proximl._query(
            f"/project/{self._project_uuid}/services/{self._id}/disable", "PATCH"
        )

    async def get_service_ca_certificate(self, **kwargs):
        certificate = await self.proximl._query(
            f"/project/{self._project_uuid}/services/{self._id}/certificate/ca",
            "GET",
            kwargs,
        )
        return certificate
    
    async def sign_client_certificate(self, csr, **kwargs):
        certificate = await self.proximl._query(
            f"/project/{self._project_uuid}/services/{self._id}/certificate/sign",
            "POST",
            kwargs,
            dict(csr=csr)
        )
        return certificate
