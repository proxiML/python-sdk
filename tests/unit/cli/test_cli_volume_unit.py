import re
import json
import click
from unittest.mock import AsyncMock, patch
from pytest import mark, fixture, raises

pytestmark = [mark.cli, mark.unit, mark.volumes]

from proximl.cli import volume as specimen
from proximl.volumes import Volume


def test_list(runner, mock_my_volumes):
    with patch("proximl.cli.ProxiML", new=AsyncMock) as mock_proximl:
        mock_proximl.volumes = AsyncMock()
        mock_proximl.volumes.list = AsyncMock(return_value=mock_my_volumes)
        result = runner.invoke(specimen, ["list"])
        print(result)
        assert result.exit_code == 0
        mock_proximl.volumes.list.assert_called_once()
