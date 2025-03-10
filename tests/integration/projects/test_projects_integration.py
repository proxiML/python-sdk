import re
import sys
import asyncio
from pytest import mark, fixture

pytestmark = [mark.sdk, mark.integration, mark.projects]


@mark.create
@mark.asyncio
@mark.xdist_group("project_resources")
class GetProjectsTests:
    async def test_get_projects(self, proximl):
        projects = await proximl.projects.list()
        assert len(projects) > 0

    async def test_get_project(self, proximl, project):
        response = await proximl.projects.get(project.id)
        assert response.id == project.id

    async def test_project_properties(self, project):
        assert isinstance(project.id, str)
        assert isinstance(project.name, str)
        assert isinstance(project.owner_name, str)
        assert isinstance(project.is_owner, bool)
        assert project.name == "New Project"
        assert project.is_owner

    async def test_project_str(self, project):
        string = str(project)
        regex = r"^{.*\"id\": \"" + project.id + r"\".*}$"
        assert isinstance(string, str)
        assert re.match(regex, string)

    async def test_project_repr(self, project):
        string = repr(project)
        regex = r"^Project\( proximl , \*\*{.*'id': '" + project.id + r"'.*}\)$"
        assert isinstance(string, str)
        assert re.match(regex, string)
