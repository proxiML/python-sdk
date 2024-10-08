import re
import json
import logging
from unittest.mock import AsyncMock, patch
from pytest import mark, fixture, raises
from aiohttp import WSMessage, WSMsgType

import proximl.projects.credentials as specimen
from proximl.exceptions import (
    ApiError,
    SpecificationError,
    ProxiMLException,
)

pytestmark = [mark.sdk, mark.unit, mark.projects]


@fixture
def project_credentials(mock_proximl):
    yield specimen.ProjectCredentials(mock_proximl, project_id="1")


@fixture
def project_credential(mock_proximl):
    yield specimen.ProjectCredential(
        mock_proximl, project_uuid="proj-id-1", type="aws", key_id="AIYHGFSDLK"
    )


class ProjectCredentialsTests:
    @mark.asyncio
    async def test_project_credentials_list(self, project_credentials, mock_proximl):
        api_response = [
            {"project_uuid": "proj-id-1", "type": "aws", "key_id": "AIYHGFSDLK"},
            {"project_uuid": "proj-id-1", "type": "gcp", "key_id": "credentials.json"},
        ]
        mock_proximl._query = AsyncMock(return_value=api_response)
        resp = await project_credentials.list()
        mock_proximl._query.assert_called_once_with(
            "/project/1/credentials", "GET", dict()
        )
        assert len(resp) == 2

    @mark.asyncio
    async def test_remove_project_credential(
        self,
        project_credentials,
        mock_proximl,
    ):
        api_response = dict()
        mock_proximl._query = AsyncMock(return_value=api_response)
        await project_credentials.remove("aws")
        mock_proximl._query.assert_called_once_with(
            "/project/1/credential/aws", "DELETE", dict()
        )

    @mark.asyncio
    async def test_put_project_credential(self, project_credentials, mock_proximl):
        requested_config = dict(type="aws", key_id="AIUDHADA", secret="ASKHJSLKF")
        expected_payload = dict(key_id="AIUDHADA", secret="ASKHJSLKF")
        api_response = {
            "project_uuid": "project-id-1",
            "type": "aws",
            "key_id": "AIUDHADA",
        }

        mock_proximl._query = AsyncMock(return_value=api_response)
        response = await project_credentials.put(**requested_config)
        mock_proximl._query.assert_called_once_with(
            "/project/1/credential/aws", "PUT", None, expected_payload
        )
        assert response.type == "aws"


class ProjectCredentialTests:
    def test_project_credential_properties(self, project_credential):
        assert isinstance(project_credential.type, str)
        assert isinstance(project_credential.key_id, str)
        assert isinstance(project_credential.project_uuid, str)

    def test_project_credential_str(self, project_credential):
        string = str(project_credential)
        regex = r"^{.*\"type\": \"" + project_credential.type + r"\".*}$"
        assert isinstance(string, str)
        assert re.match(regex, string)

    def test_project_credential_repr(self, project_credential):
        string = repr(project_credential)
        regex = (
            r"^ProjectCredential\( proximl , \*\*{.*'type': '"
            + project_credential.type
            + r"'.*}\)$"
        )
        assert isinstance(string, str)
        assert re.match(regex, string)

    def test_project_credential_bool(self, project_credential, mock_proximl):
        empty_project_credential = specimen.ProjectCredential(mock_proximl)
        assert bool(project_credential)
        assert not bool(empty_project_credential)
