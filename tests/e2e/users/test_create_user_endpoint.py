import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from asgi_lifespan import LifespanManager

@pytest.mark.asyncio
async def test_create_user_successfully():
    transport = ASGITransport(app=app)

    async with LifespanManager(app):
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/api/v1/users", json={
                "username": "e2euser",
                "email": "e2e@example.com",
                "first_name": "Carlos",
                "last_name": "López",
                "raw_password": "Password1!"
            })
            print("\nURL:", response.url)
            print("Status Code:", response.status_code)
            try:
                print("Response JSON:", response.json())
            except Exception as e:
                print("Error al parsear JSON:", str(e))
                print("Raw Response Text:", response.text)

            # Asserts para validar comportamiento esperado
            assert response.status_code == 201, f"Expected 201, got {response.status_code} | {response.text}"
