import pytest
from httpx import ASGITransport, AsyncClient

from CI.main import app


@pytest.mark.asyncio
async def test_post_recipes():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/recipes",
            json={
                "title": "string1",
                "time_cooking": 2,
                "ingredients": [{"name": "string", "weight": 0.2}],
                "description": "string2",
            },
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_recipes():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/recipes/")
        assert response.status_code == 200
