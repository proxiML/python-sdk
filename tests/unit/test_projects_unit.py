import re
import json
import logging
from unittest.mock import AsyncMock, patch
from pytest import mark, fixture, raises
from aiohttp import WSMessage, WSMsgType

import proximl.projects as specimen
from proximl.exceptions import (
    ApiError,
    SpecificationError,
    ProxiMLException,
)

pytestmark = [mark.sdk, mark.unit, mark.projects]


@fixture
def projects(mock_proximl):
    yield specimen.Projects(mock_proximl)


@fixture
def project(mock_proximl):
    yield specimen.Project(
        mock_proximl,
        id="1",
        name="My Mock Project",
        owner=True,
        owner_name="Me",
        created_name="Me",
        job_all=True,
        dataset_all=True,
        model_all=True,
        createdAt="2020-12-31T23:59:59.000Z",
    )


@fixture
def project_datastore(mock_proximl):
    yield specimen.ProjectDatastore(
        mock_proximl,
        id="ds-id-1",
        name="datastore 1",
        project_uuid="proj-id-1",
        type="nfs",
        region_uuid="reg-id-1",
    )


@fixture
def project_data_connector(mock_proximl):
    yield specimen.ProjectDataConnector(
        mock_proximl,
        id="ds-id-1",
        name="connector 1",
        project_uuid="proj-id-1",
        type="custom",
        region_uuid="reg-id-1",
    )


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


class ProjectsTests:
    @mark.asyncio
    async def test_get_project(
        self,
        projects,
        mock_proximl,
    ):
        api_response = dict()
        mock_proximl._query = AsyncMock(return_value=api_response)
        await projects.get("1234")
        mock_proximl._query.assert_called_once_with("/project/1234", "GET", dict())

    @mark.asyncio
    async def test_list_projects(
        self,
        projects,
        mock_proximl,
    ):
        api_response = dict()
        mock_proximl._query = AsyncMock(return_value=api_response)
        await projects.list()
        mock_proximl._query.assert_called_once_with("/project", "GET", dict())

    @mark.asyncio
    async def test_remove_project(
        self,
        projects,
        mock_proximl,
    ):
        api_response = dict()
        mock_proximl._query = AsyncMock(return_value=api_response)
        await projects.remove("4567")
        mock_proximl._query.assert_called_once_with("/project/4567", "DELETE", dict())

    @mark.asyncio
    async def test_create_project_simple(self, projects, mock_proximl):
        requested_config = dict(
            name="new project",
        )
        expected_payload = dict(name="new project", copy_keys=False)
        api_response = {
            "id": "project-id-1",
            "name": "new project",
            "owner": True,
            "owner_name": "Me",
            "created_name": "Me",
            "job_all": True,
            "dataset_all": True,
            "model_all": True,
            "createdAt": "2020-12-31T23:59:59.000Z",
        }

        mock_proximl._query = AsyncMock(return_value=api_response)
        response = await projects.create(**requested_config)
        mock_proximl._query.assert_called_once_with(
            "/project", "POST", None, expected_payload
        )
        assert response.id == "project-id-1"


class ProjectDatastoreTests:
    def test_project_datastore_properties(self, project_datastore):
        assert isinstance(project_datastore.id, str)
        assert isinstance(project_datastore.name, str)
        assert isinstance(project_datastore.project_uuid, str)
        assert isinstance(project_datastore.type, str)
        assert isinstance(project_datastore.region_uuid, str)

    def test_project_datastore_str(self, project_datastore):
        string = str(project_datastore)
        regex = r"^{.*\"id\": \"" + project_datastore.id + r"\".*}$"
        assert isinstance(string, str)
        assert re.match(regex, string)

    def test_project_datastore_repr(self, project_datastore):
        string = repr(project_datastore)
        regex = (
            r"^ProjectDatastore\( proximl , \*\*{.*'id': '"
            + project_datastore.id
            + r"'.*}\)$"
        )
        assert isinstance(string, str)
        assert re.match(regex, string)

    def test_project_datastore_bool(self, project_datastore, mock_proximl):
        empty_project_datastore = specimen.ProjectDatastore(mock_proximl)
        assert bool(project_datastore)
        assert not bool(empty_project_datastore)


class ProjectDataConnectorTests:
    def test_project_data_connector_properties(self, project_data_connector):
        assert isinstance(project_data_connector.id, str)
        assert isinstance(project_data_connector.name, str)
        assert isinstance(project_data_connector.project_uuid, str)
        assert isinstance(project_data_connector.type, str)
        assert isinstance(project_data_connector.region_uuid, str)

    def test_project_data_connector_str(self, project_data_connector):
        string = str(project_data_connector)
        regex = r"^{.*\"id\": \"" + project_data_connector.id + r"\".*}$"
        assert isinstance(string, str)
        assert re.match(regex, string)

    def test_project_data_connector_repr(self, project_data_connector):
        string = repr(project_data_connector)
        regex = (
            r"^ProjectDataConnector\( proximl , \*\*{.*'id': '"
            + project_data_connector.id
            + r"'.*}\)$"
        )
        assert isinstance(string, str)
        assert re.match(regex, string)

    def test_project_data_connector_bool(self, project_data_connector, mock_proximl):
        empty_project_data_connector = specimen.ProjectDataConnector(mock_proximl)
        assert bool(project_data_connector)
        assert not bool(empty_project_data_connector)


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


class ProjectTests:
    def test_project_properties(self, project):
        assert isinstance(project.id, str)
        assert isinstance(project.name, str)
        assert isinstance(project.owner_name, str)
        assert isinstance(project.is_owner, bool)

    def test_project_str(self, project):
        string = str(project)
        regex = r"^{.*\"id\": \"" + project.id + r"\".*}$"
        assert isinstance(string, str)
        assert re.match(regex, string)

    def test_project_repr(self, project):
        string = repr(project)
        regex = r"^Project\( proximl , \*\*{.*'id': '" + project.id + r"'.*}\)$"
        assert isinstance(string, str)
        assert re.match(regex, string)

    def test_project_bool(self, project, mock_proximl):
        empty_project = specimen.Project(mock_proximl)
        assert bool(project)
        assert not bool(empty_project)

    @mark.asyncio
    async def test_project_remove(self, project, mock_proximl):
        api_response = dict()
        mock_proximl._query = AsyncMock(return_value=api_response)
        await project.remove()
        mock_proximl._query.assert_called_once_with("/project/1", "DELETE")

    @mark.asyncio
    async def test_project_refresh_datastores(self, project, mock_proximl):
        api_response = dict()
        mock_proximl._query = AsyncMock(return_value=api_response)
        await project.refresh_datastores()
        mock_proximl._query.assert_called_once_with("/project/1/datastores", "PATCH")

    @mark.asyncio
    async def test_project_refresh_services(self, project, mock_proximl):
        api_response = dict()
        mock_proximl._query = AsyncMock(return_value=api_response)
        await project.refresh_services()
        mock_proximl._query.assert_called_once_with("/project/1/services", "PATCH")

    @mark.asyncio
    async def test_project_list_datastores(self, project, mock_proximl):
        api_response = [
            {
                "project_uuid": "proj-id-1",
                "region_uuid": "reg-id-1",
                "id": "store-id-1",
                "type": "nfs",
                "name": "On-prem NFS",
            },
            {
                "project_uuid": "proj-id-1",
                "region_uuid": "reg-id-2",
                "id": "store-id-2",
                "type": "smb",
                "name": "GCP Samba",
            },
        ]
        mock_proximl._query = AsyncMock(return_value=api_response)
        resp = await project.list_datastores()
        mock_proximl._query.assert_called_once_with("/project/1/datastores", "GET")
        assert len(resp) == 2

    @mark.asyncio
    async def test_project_list_services(self, project, mock_proximl):
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
        resp = await project.list_services()
        mock_proximl._query.assert_called_once_with("/project/1/services", "GET")
        assert len(resp) == 2
