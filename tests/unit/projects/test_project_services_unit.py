import re
import json
import logging
from unittest.mock import AsyncMock, patch
from pytest import mark, fixture, raises
from aiohttp import WSMessage, WSMsgType

import proximl.projects.services as specimen
from proximl.exceptions import (
    ApiError,
    SpecificationError,
    ProxiMLException,
)

pytestmark = [mark.sdk, mark.unit, mark.projects]


@fixture
def project_services(mock_proximl):
    yield specimen.ProjectServices(mock_proximl, project_id="1")


@fixture
def project_service(mock_proximl):
    yield specimen.ProjectService(
        mock_proximl,
        id="res-id-1",
        name="service 1",
        project_uuid="proj-id-1",
        region_uuid="reg-id-1",
        public=False,
        hostname="asdf.proximl.cloud",
    )


class ProjectServicesTests:
    @mark.asyncio
    async def test_project_services_get(self, project_services, mock_proximl):
        """Test get method (lines 11-14)."""
        api_response = {
            "project_uuid": "proj-id-1",
            "region_uuid": "reg-id-1",
            "id": "res-id-1",
            "type": "port",
            "name": "On-Prem Service A",
            "hostname": "service-a.local",
        }
        mock_proximl._query = AsyncMock(return_value=api_response)
        result = await project_services.get("res-id-1", param1="value1")
        mock_proximl._query.assert_called_once_with(
            "/project/1/services/res-id-1", "GET", dict(param1="value1")
        )
        assert result.id == "res-id-1"

    @mark.asyncio
    async def test_project_services_refresh(self, project_services, mock_proximl):
        api_response = dict()
        mock_proximl._query = AsyncMock(return_value=api_response)
        await project_services.refresh()
        mock_proximl._query.assert_called_once_with("/project/1/services", "PATCH")

    @mark.asyncio
    async def test_project_services_list(self, project_services, mock_proximl):
        api_response = [
            {
                "project_uuid": "proj-id-1",
                "region_uuid": "reg-id-1",
                "id": "res-id-1",
                "type": "port",
                "name": "On-Prem Service A",
                "resource": "8001",
                "hostname": "service-a.local",
            },
            {
                "project_uuid": "proj-id-1",
                "region_uuid": "reg-id-2",
                "id": "res-id-2",
                "type": "port",
                "name": "Cloud Service B",
                "resource": "8001",
                "hostname": "service-b.local",
            },
        ]
        mock_proximl._query = AsyncMock(return_value=api_response)
        resp = await project_services.list()
        mock_proximl._query.assert_called_once_with(
            "/project/1/services", "GET", dict()
        )
        assert len(resp) == 2


class ProjectServiceTests:
    def test_project_service_properties(self, project_service):
        assert isinstance(project_service.id, str)
        assert isinstance(project_service.name, str)
        assert isinstance(project_service.project_uuid, str)
        assert isinstance(project_service.hostname, str)
        assert isinstance(project_service.public, bool)
        assert isinstance(project_service.region_uuid, str)

    def test_project_service_str(self, project_service):
        string = str(project_service)
        regex = r"^{.*\"id\": \"" + project_service.id + r"\".*}$"
        assert isinstance(string, str)
        assert re.match(regex, string)

    def test_project_service_repr(self, project_service):
        string = repr(project_service)
        regex = (
            r"^ProjectService\( proximl , \*\*{.*'id': '"
            + project_service.id
            + r"'.*}\)$"
        )
        assert isinstance(string, str)
        assert re.match(regex, string)

    def test_project_service_bool(self, project_service, mock_proximl):
        empty_project_service = specimen.ProjectService(mock_proximl)
        assert bool(project_service)
        assert not bool(empty_project_service)

    @mark.asyncio
    async def test_project_service_enable(self, project_service, mock_proximl):
        """Test enable method (line 72)."""
        api_response = dict()
        mock_proximl._query = AsyncMock(return_value=api_response)
        await project_service.enable()
        mock_proximl._query.assert_called_once_with(
            "/project/proj-id-1/services/res-id-1/enable", "PATCH"
        )

    @mark.asyncio
    async def test_project_service_disable(self, project_service, mock_proximl):
        """Test disable method (line 77)."""
        api_response = dict()
        mock_proximl._query = AsyncMock(return_value=api_response)
        await project_service.disable()
        mock_proximl._query.assert_called_once_with(
            "/project/proj-id-1/services/res-id-1/disable", "PATCH"
        )

    @mark.asyncio
    async def test_project_service_get_service_ca_certificate(self, project_service, mock_proximl):
        """Test get_service_ca_certificate method (lines 82-87)."""
        api_response = {"certificate": "ca-cert-data"}
        mock_proximl._query = AsyncMock(return_value=api_response)
        result = await project_service.get_service_ca_certificate(param1="value1")
        mock_proximl._query.assert_called_once_with(
            "/project/proj-id-1/services/res-id-1/certificate/ca",
            "GET",
            dict(param1="value1"),
        )
        assert result == api_response

    @mark.asyncio
    async def test_project_service_sign_client_certificate(self, project_service, mock_proximl):
        """Test sign_client_certificate method (lines 90-96)."""
        api_response = {"certificate": "signed-cert-data"}
        mock_proximl._query = AsyncMock(return_value=api_response)
        result = await project_service.sign_client_certificate("csr-data", param1="value1")
        mock_proximl._query.assert_called_once_with(
            "/project/proj-id-1/services/res-id-1/certificate/sign",
            "POST",
            dict(param1="value1"),
            dict(csr="csr-data"),
        )
        assert result == api_response
