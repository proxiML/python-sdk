import re
import json
import click
from unittest.mock import AsyncMock, patch, create_autospec
from pytest import mark, fixture, raises

pytestmark = [mark.cli, mark.unit, mark.projects]

from proximl.cli.project import credential as specimen
from proximl.projects import (
    Project,
)


def test_list_credentials(runner, mock_project_credentials):
    with patch("proximl.cli.ProxiML", new=AsyncMock) as mock_proximl:
        project = create_autospec(Project)
        mock_proximl.projects = AsyncMock()
        mock_proximl.projects.get = AsyncMock(return_value=project)
        mock_proximl.projects.get_current = AsyncMock(return_value=project)
        project.credentials = AsyncMock()
        project.credentials.list = AsyncMock(return_value=mock_project_credentials)
        result = runner.invoke(specimen, ["list"])
        print(result)
        assert result.exit_code == 0
        project.credentials.list.assert_called_once()
