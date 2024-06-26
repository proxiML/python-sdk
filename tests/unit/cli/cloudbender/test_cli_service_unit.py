import re
import json
import click
from unittest.mock import AsyncMock, patch
from pytest import mark, fixture, raises

pytestmark = [mark.cli, mark.unit, mark.cloudbender, mark.services]

from proximl.cli.cloudbender import service as specimen
from proximl.cloudbender.services import Service


def test_list(runner, mock_services):
    with patch("proximl.cli.ProxiML", new=AsyncMock) as mock_proximl:
        mock_proximl.cloudbender = AsyncMock()
        mock_proximl.cloudbender.services = AsyncMock()
        mock_proximl.cloudbender.services.list = AsyncMock(return_value=mock_services)
        result = runner.invoke(
            specimen,
            args=["list", "--provider=prov-id-1", "--region=reg-id-1"],
        )
        assert result.exit_code == 0
        mock_proximl.cloudbender.services.list.assert_called_once_with(
            provider_uuid="prov-id-1", region_uuid="reg-id-1"
        )


def test_list_no_provider(runner, mock_services):
    with patch("proximl.cli.ProxiML", new=AsyncMock) as mock_proximl:
        mock_proximl.cloudbender = AsyncMock()
        mock_proximl.cloudbender.services = AsyncMock()
        mock_proximl.cloudbender.services.list = AsyncMock(return_value=mock_services)
        result = runner.invoke(specimen, ["list"])
        assert result.exit_code != 0
