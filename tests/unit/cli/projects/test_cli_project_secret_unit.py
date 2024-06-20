import re
import json
import click
from unittest.mock import AsyncMock, patch, create_autospec
from pytest import mark, fixture, raises

pytestmark = [mark.cli, mark.unit, mark.projects]

from proximl.cli.project import secret as specimen
from proximl.projects import (
    Project,
)


def test_list_secrets(runner, mock_project_secrets):
    with patch("proximl.cli.ProxiML", new=AsyncMock) as mock_proximl:
        project = create_autospec(Project)
        mock_proximl.projects = AsyncMock()
        mock_proximl.projects.get = AsyncMock(return_value=project)
        mock_proximl.projects.get_current = AsyncMock(return_value=project)
        project.secrets = AsyncMock()
        project.secrets.list = AsyncMock(return_value=mock_project_secrets)
        result = runner.invoke(specimen, ["list"])
        print(result)
        assert result.exit_code == 0
        project.secrets.list.assert_called_once()
