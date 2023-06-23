import json
import logging
from datetime import datetime


class Providers(object):
    def __init__(self, proximl):
        self.proximl = proximl

    async def get(self, id):
        resp = await self.proximl._query(f"/provider/{id}", "GET")
        return Provider(self.proximl, **resp)

    async def list(self):
        resp = await self.proximl._query(f"/provider", "GET")
        providers = [Provider(self.proximl, **provider) for provider in resp]
        return providers

    async def enable(self, type, **kwargs):
        data = dict(type=type, **kwargs)
        payload = {k: v for k, v in data.items() if v is not None}
        logging.info(f"Enabling Provider {type}")
        resp = await self.proximl._query("/provider", "POST", None, payload)
        provider = Provider(self.proximl, **resp)
        logging.info(f"Enabled Provider {type} with id {provider.id}")

        return provider

    async def remove(self, id):
        await self.proximl._query(f"/provider/{id}", "DELETE")


class Provider:
    def __init__(self, proximl, **kwargs):
        self.proximl = proximl
        self._provider = kwargs
        self._id = self._provider.get("provider_uuid")
        self._type = self._provider.get("type")
        self._credits = self._provider.get("credits")

    @property
    def id(self) -> str:
        return self._id

    @property
    def type(self) -> str:
        return self._type

    @property
    def credits(self) -> float:
        return self._credits

    def __str__(self):
        return json.dumps({k: v for k, v in self._provider.items()})

    def __repr__(self):
        return f"Provider( proximl , **{self._provider.__repr__()})"

    def __bool__(self):
        return bool(self._id)

    async def remove(self):
        await self.proximl._query(f"/provider/{self._id}", "DELETE")

    async def refresh(self):
        resp = await self.proximl._query(
            f"/provider/{self._id}",
            "GET",
        )
        self.__init__(self.proximl, **resp)
        return self
