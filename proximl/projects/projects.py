import json
import logging
from .datastores import ProjectDatastores
from .data_connectors import ProjectDataConnectors
from .services import ProjectServices
from .credentials import ProjectCredentials
from .secrets import ProjectSecrets
from .members import ProjectMembers


class Projects(object):
    def __init__(self, proximl):
        self.proximl = proximl

    async def get(self, id, **kwargs):
        resp = await self.proximl._query(f"/project/{id}", "GET", kwargs)
        return Project(self.proximl, **resp)

    async def get_current(self, **kwargs):
        resp = await self.proximl._query(
            f"/project/{self.proximl.project}", "GET", kwargs
        )
        return Project(self.proximl, **resp)

    async def list(self, **kwargs):
        resp = await self.proximl._query(f"/project", "GET", kwargs)
        projects = [Project(self.proximl, **project) for project in resp]
        return projects

    async def create(self, name, **kwargs):
        data = dict(
            name=name,
            **kwargs
        )
        payload = {k: v for k, v in data.items() if v is not None}
        logging.info(f"Creating Project {name}")
        resp = await self.proximl._query("/project", "POST", None, payload)
        project = Project(self.proximl, **resp)
        logging.info(f"Created Project {name} with id {project.id}")

        return project

    async def remove(self, id, **kwargs):
        await self.proximl._query(f"/project/{id}", "DELETE", kwargs)


class Project:
    def __init__(self, proximl, **kwargs):
        self.proximl = proximl
        self._entity = kwargs
        self._id = self._entity.get("id")
        self._name = self._entity.get("name")
        self._is_owner = self._entity.get("owner")
        self._owner_name = self._entity.get("owner_name")
        self.datastores = ProjectDatastores(self.proximl, self._id)
        self.data_connectors = ProjectDataConnectors(self.proximl, self._id)
        self.services = ProjectServices(self.proximl, self._id)
        self.credentials = ProjectCredentials(self.proximl, self._id)
        self.secrets = ProjectSecrets(self.proximl, self._id)
        self.members = ProjectMembers(self.proximl, self._id)

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_owner(self) -> bool:
        return self._is_owner

    @property
    def owner_name(self) -> str:
        return self._owner_name

    def __str__(self):
        return json.dumps({k: v for k, v in self._entity.items()})

    def __repr__(self):
        return f"Project( proximl , **{self._entity.__repr__()})"

    def __bool__(self):
        return bool(self._id)

    async def remove(self):
        await self.proximl._query(f"/project/{self._id}", "DELETE")
