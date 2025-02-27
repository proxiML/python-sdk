from pytest import fixture, mark


@fixture(scope="module")
@mark.xdist_group("project_resources")
async def project(proximl):
    project = await proximl.projects.create(
        name="New Project", copy_credentials=False, copy_secrets=False
    )
    yield project
    await project.remove()
