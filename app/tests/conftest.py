import asyncio

import pytest
import json

from sqlalchemy import insert
from datetime import datetime

from app.config import settings
from app.database import Base,async_session_maker,engine
from app.bookings.models import Bookings
from app.main import app as fastapi_app
from app.users.models import Users
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


from fastapi.testclient import TestClient
from httpx import AsyncClient,ASGITransport


@pytest.fixture(scope="session",autouse=True)
async def repare_database():
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


    def open_mock_json(model:str):
        with open (f"app/tests/mock_{model}.json",encoding="utf-8") as f:
            return json.load(f)

    hotels = open_mock_json('hotels')
    rooms = open_mock_json('rooms')
    users = open_mock_json('users')
    bookings = open_mock_json('bookings')

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        for Model, values in [
            (Hotels, hotels),
            (Rooms, rooms),
            (Users, users),
            (Bookings, bookings),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()

# Взято из документации к pytest-asyncio
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def ac() :
    async with AsyncClient(transport=ASGITransport(app=fastapi_app),base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session")
async def authenticated_ac() :
    async with AsyncClient(transport=ASGITransport(app=fastapi_app),base_url="http://test") as ac:
        response = await ac.post("/auth/login", json={
            "email":"test@test.com",
            "password":"test",
        })
        token = response.cookies.get("token")
        assert token
        ac.cookies.set("token",token)
        yield ac

@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session