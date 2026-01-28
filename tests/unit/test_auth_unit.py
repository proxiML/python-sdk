import re
import logging
import json
import os
from unittest.mock import AsyncMock, patch, mock_open, MagicMock
from pytest import mark, fixture, raises
from aiohttp import WSMessage, WSMsgType

import proximl.utils.auth as specimen

pytestmark = [mark.sdk, mark.unit]


@patch.dict(
    os.environ,
    {
        "PROXIML_USER": "user-id",
        "PROXIML_KEY": "key",
        "PROXIML_REGION": "ap-east-1",
        "PROXIML_CLIENT_ID": "client_id",
        "PROXIML_POOL_ID": "pool_id",
    },
)
@patch("proximl.utils.auth.boto3.client")
@patch("proximl.utils.auth.requests.get")
@patch("builtins.open", side_effect=FileNotFoundError)
def test_auth_from_envs(mock_open, mock_requests_get, mock_boto3_client):
    # Mock the auth config request
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "region": "us-east-1",
        "userPoolSDKClientId": "default_client_id",
        "userPoolId": "default_pool_id",
    }
    mock_requests_get.return_value = mock_response

    # Mock boto3 client
    mock_boto3_client.return_value = MagicMock()

    auth = specimen.Auth(config_dir=os.path.expanduser("~/.proximl"))
    assert auth.__dict__.get("username") == "user-id"
    assert auth.__dict__.get("password") == "key"
    assert auth.__dict__.get("region") == "ap-east-1"
    assert auth.__dict__.get("client_id") == "client_id"
    assert auth.__dict__.get("pool_id") == "pool_id"
