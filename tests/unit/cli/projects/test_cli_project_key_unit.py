import re
import json
import click
from unittest.mock import AsyncMock, patch, create_autospec
from pytest import mark, fixture, raises

pytestmark = [mark.cli, mark.unit, mark.projects]

from proximl.cli.project import key as specimen
from proximl.projects import (
    Project,
)


def test_list_keys(runner, mock_project_keys):
    with patch("proximl.cli.ProxiML", new=AsyncMock) as mock_proximl:
        project = create_autospec(Project)
        mock_proximl.projects = AsyncMock()
        mock_proximl.projects.get = AsyncMock(return_value=project)
        mock_proximl.projects.get_current = AsyncMock(return_value=project)
        project.keys = AsyncMock()
        project.keys.list = AsyncMock(return_value=mock_project_keys)
        result = runner.invoke(specimen, ["list"])
        print(result)
        assert result.exit_code == 0
        project.keys.list.assert_called_once()
