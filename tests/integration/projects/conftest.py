from pytest import fixture


@fixture(scope="module")
async def project(proximl):
    project = await proximl.projects.create(name="New Project", copy_keys=False)
    yield project
    await project.remove()
