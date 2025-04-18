
from pytest import fixture, mark


pytestmark = [mark.integration,mark.cloudbender]

@fixture(scope="session")
@mark.create
@mark.asyncio
@mark.xdist_group("cloudbender_resources")
async def provider( proximl):
    provider = await proximl.cloudbender.providers.enable(type="test")
    await provider.wait_for("ready")
    yield provider
    await provider.remove()

@fixture(scope="session")
@mark.create
@mark.asyncio
@mark.xdist_group("cloudbender_resources")
async def region(proximl, provider):
    region = await proximl.cloudbender.regions.create(provider_uuid=provider.id,name="test-region",
        public=False,
        storage=dict(mode="local"),)
    await region.wait_for("healthy")
    yield region
    await region.remove()
    await region.wait_for("archived")