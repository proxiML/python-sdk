import re
import json
import click
from unittest.mock import AsyncMock, patch, create_autospec
from pytest import mark, fixture, raises

pytestmark = [mark.cli, mark.unit, mark.projects]

from proximl.cli import project as specimen
from proximl.projects import Project


def test_list(runner, mock_projects):
    with patch("proximl.cli.ProxiML", new=AsyncMock) as mock_proximl:
        mock_proximl.projects = AsyncMock()
        mock_proximl.projects.list = AsyncMock(return_value=mock_projects)
        result = runner.invoke(specimen, ["list"])
        print(result)
        assert result.exit_code == 0
        mock_proximl.projects.list.assert_called_once()


def test_list_datastores(runner, mock_project_datastores):
    with patch("proximl.cli.ProxiML", new=AsyncMock) as mock_proximl:
        mock_project = create_autospec(Project)
        mock_project.list_datastores = AsyncMock(return_value=mock_project_datastores)
        mock_proximl.projects.get = AsyncMock(return_value=mock_project)
        result = runner.invoke(specimen, ["list-datastores"])
        print(result)
        assert result.exit_code == 0
        mock_project.list_datastores.assert_called_once()


def test_list_services(runner, mock_project_services):
    with patch("proximl.cli.ProxiML", new=AsyncMock) as mock_proximl:
        mock_project = create_autospec(Project)
        mock_project.list_services = AsyncMock(return_value=mock_project_services)
        mock_proximl.projects.get = AsyncMock(return_value=mock_project)
        result = runner.invoke(specimen, ["list-services"])
        print(result)
        assert result.exit_code == 0
        mock_project.list_services.assert_called_once()
