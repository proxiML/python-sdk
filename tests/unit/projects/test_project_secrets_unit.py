import re
import json
import logging
from unittest.mock import AsyncMock, patch
from pytest import mark, fixture, raises
from aiohttp import WSMessage, WSMsgType

import proximl.projects.secrets as specimen
from proximl.exceptions import (
    ApiError,
    SpecificationError,
    ProxiMLException,
)

pytestmark = [mark.sdk, mark.unit, mark.projects]


@fixture
def project_secrets(mock_proximl):
    yield specimen.ProjectSecrets(mock_proximl, project_id="1")


@fixture
def project_service(mock_proximl):
    yield specimen.ProjectSecret(
        mock_proximl,
        project_uuid="proj-id-1",
        name="secret_value",
    )


class ProjectSecretsTests:
    @mark.asyncio
    async def test_project_secrets_list(self, project_secrets, mock_proximl):
        api_response = [
            {
                "project_uuid": "proj-id-1",
                "name": "secret_value",
            },
            {
                "project_uuid": "proj-id-1",
                "name": "secret_value_2",
            },
        ]
        mock_proximl._query = AsyncMock(return_value=api_response)
        resp = await project_secrets.list()
        mock_proximl._query.assert_called_once_with("/project/1/secrets", "GET", dict())
        assert len(resp) == 2

    @mark.asyncio
    async def test_remove_project_secret(
        self,
        project_secrets,
        mock_proximl,
    ):
        api_response = dict()
        mock_proximl._query = AsyncMock(return_value=api_response)
        await project_secrets.remove("secret_value")
        mock_proximl._query.assert_called_once_with(
            "/project/1/secret/secret_value", "DELETE", dict()
        )

    @mark.asyncio
    async def test_put_project_secret(self, project_secrets, mock_proximl):
        requested_config = dict(name="secret_value", value="ASKHJSLKF")
        expected_payload = dict(value="ASKHJSLKF")
        api_response = {"project_uuid": "project-id-1", "name": "secret_value"}

        mock_proximl._query = AsyncMock(return_value=api_response)
        response = await project_secrets.put(**requested_config)
        mock_proximl._query.assert_called_once_with(
            "/project/1/secret/secret_value", "PUT", None, expected_payload
        )
        assert response.name == "secret_value"


class ProjectSecretTests:
    def test_project_service_properties(self, project_service):
        assert isinstance(project_service.name, str)
        assert isinstance(project_service.project_uuid, str)

    def test_project_service_str(self, project_service):
        string = str(project_service)
        regex = r"^{.*\"name\": \"" + project_service.name + r"\".*}$"
        assert isinstance(string, str)
        assert re.match(regex, string)

    def test_project_service_repr(self, project_service):
        string = repr(project_service)
        regex = (
            r"^ProjectSecret\( proximl , \*\*{.*'name': '"
            + project_service.name
            + r"'.*}\)$"
        )
        assert isinstance(string, str)
        assert re.match(regex, string)

    def test_project_service_bool(self, project_service, mock_proximl):
        empty_project_service = specimen.ProjectSecret(mock_proximl)
        assert bool(project_service)
        assert not bool(empty_project_service)
