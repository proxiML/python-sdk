import json
import logging
import asyncio
import math
from enum import Enum

from proximl.exceptions import (
    ApiError,
    SpecificationError,
    ProxiMLException,
)

class SERVICE_CERT_ALGORITHMS(str, Enum):
    RSA_2048 = 'rsa2048'
    RSA_4096 = 'rsa4096'
    ED25519 = 'ed25519'
    P256 = 'p256'
    P384 ='p384'
    P521='p521'


class Services(object):
    def __init__(self, proximl):
        self.proximl = proximl

    async def get(self, provider_uuid, region_uuid, id, **kwargs):
        resp = await self.proximl._query(
            f"/provider/{provider_uuid}/region/{region_uuid}/service/{id}",
            "GET",
            kwargs,
        )
        return Service(self.proximl, **resp)

    async def list(self, provider_uuid, region_uuid, **kwargs):
        resp = await self.proximl._query(
            f"/provider/{provider_uuid}/region/{region_uuid}/service",
            "GET",
            kwargs,
        )
        services = [Service(self.proximl, **service) for service in resp]
        return services

    async def create(
        self,
        provider_uuid,
        region_uuid,
        name,
        type,
        public,
        **kwargs,
    ):
        logging.info(f"Creating Service {name}")
        data = dict(
            name=name,
            type=type,
            public=public,
            **kwargs,
        )
        payload = {k: v for k, v in data.items() if v is not None}
        resp = await self.proximl._query(
            f"/provider/{provider_uuid}/region/{region_uuid}/service",
            "POST",
            None,
            payload,
        )
        service = Service(self.proximl, **resp)
        logging.info(f"Created Service {name} with id {service.id}")
        return service

    async def remove(self, provider_uuid, region_uuid, id, **kwargs):
        await self.proximl._query(
            f"/provider/{provider_uuid}/region/{region_uuid}/service/{id}",
            "DELETE",
            kwargs,
        )


class Service:
    def __init__(self, proximl,  **kwargs):
        self.proximl = proximl
        self._service = kwargs
        self._id = self._service.get("service_id")
        self._provider_uuid = self._service.get("provider_uuid")
        self._region_uuid = self._service.get("region_uuid")
        self._public = self._service.get("public")
        self._name = self._service.get("name")
        self._type = self._service.get("type")
        self._hostname = self._service.get("custom_hostname") or self._service.get(
            "hostname"
        )
        self._status = self._service.get("status")
        self._port = self._service.get("port")

    @property
    def id(self) -> str:
        return self._id

    @property
    def provider_uuid(self) -> str:
        return self._provider_uuid

    @property
    def region_uuid(self) -> str:
        return self._region_uuid

    @property
    def public(self) -> bool:
        return self._public

    @property
    def name(self) -> str:
        return self._name

    @property
    def hostname(self) -> str:
        return self._hostname

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    @property
    def port(self) -> str:
        return self._port

    def __str__(self):
        return json.dumps({k: v for k, v in self._service.items()})

    def __repr__(self):
        return f"Service( proximl , **{self._service.__repr__()})"

    def __bool__(self):
        return bool(self._id)

    async def remove(self):
        await self.proximl._query(
            f"/provider/{self._provider_uuid}/region/{self._region_uuid}/service/{self._id}",
            "DELETE",
        )

    async def refresh(self):
        resp = await self.proximl._query(
            f"/provider/{self._provider_uuid}/region/{self._region_uuid}/service/{self._id}",
            "GET",
        )
        self.__init__(self.proximl, **resp)
        return self

    async def wait_for(self, status, timeout=300):
        if self.status == status:
            return
        valid_statuses = ["active", "archived"]
        if not status in valid_statuses:
            raise SpecificationError(
                "status",
                f"Invalid wait_for status {status}.  Valid statuses are: {valid_statuses}",
            )
        MAX_TIMEOUT = 24 * 60 * 60
        if timeout > MAX_TIMEOUT:
            raise SpecificationError(
                "timeout",
                f"timeout must be less than {MAX_TIMEOUT} seconds.",
            )

        POLL_INTERVAL_MIN = 5
        POLL_INTERVAL_MAX = 60
        POLL_INTERVAL = max(min(timeout / 60, POLL_INTERVAL_MAX), POLL_INTERVAL_MIN)
        retry_count = math.ceil(timeout / POLL_INTERVAL)
        count = 0
        while count < retry_count:
            await asyncio.sleep(POLL_INTERVAL)
            try:
                await self.refresh()
            except ApiError as e:
                if status == "archived" and e.status == 404:
                    return
                raise e
            if self.status == status:
                return self
            else:
                count += 1
                logging.debug(f"self: {self}, retry count {count}")

        raise ProxiMLException(f"Timeout waiting for {status}")
    
    async def generate_certificate(self, algorithm=SERVICE_CERT_ALGORITHMS.ED25519.value, **kwargs):
        resp = await self.proximl._query(
            f"/provider/{self._provider_uuid}/region/{self._region_uuid}/service/{self._id}/certificate",
            "POST",
            kwargs,
            dict(algorithm=algorithm)
        )
        self.__init__(self.proximl, **resp)
        return self
    
    async def sign_client_certificate(self, csr, **kwargs):
        certificate = await self.proximl._query(
            f"/provider/{self._provider_uuid}/region/{self._region_uuid}/service/{self._id}/certificate/sign",
            "POST",
            kwargs,
            dict(csr=csr)
        )
        return certificate
