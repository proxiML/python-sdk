import re
import sys
import asyncio
from pytest import mark, fixture

pytestmark = [mark.sdk, mark.integration, mark.cloudbender, mark.regions]


@mark.create
@mark.asyncio
@mark.xdist_group("cloudbender_resources")
class GetRegionTests:
    async def test_get_regions(self, proximl, provider, region):
        regions = await proximl.cloudbender.regions.list(provider_uuid=provider.id)
        assert len(regions) > 0

    async def test_get_region(self, proximl, provider, region):
        response = await proximl.cloudbender.regions.get(provider.id, region.id)
        assert response.id == region.id

    async def test_region_properties(self, provider, region):
        assert isinstance(region.id, str)
        assert isinstance(region.provider_uuid, str)
        assert isinstance(region.type, str)
        assert region.type == "test"
        assert region.provider_uuid == provider.id

    async def test_region_str(self, region):
        string = str(region)
        regex = r"^{.*\"region_uuid\": \"" + region.id + r"\".*}$"
        assert isinstance(string, str)
        assert re.match(regex, string)

    async def test_region_repr(self, region):
        string = repr(region)
        regex = (
            r"^Region\( proximl , \*\*{.*'region_uuid': '"
            + region.id
            + r"'.*}\)$"
        )
        assert isinstance(string, str)
        assert re.match(regex, string)
