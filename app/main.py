import json
import logging
import traceback
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import time

import uvicorn

from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_versioning import VersionedFastAPI
from redis.asyncio import Redis
from sqladmin import Admin
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.responses import JSONResponse

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_booking
from app.config import settings
from app.database import engine

from app.hotels.images.router import router as router_images
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.users.router import router as router_users
from app.importer.router import router as router_importer
from app.prometheus.router import router as router_prometheus
from app.logger import log


# @asynccontextmanager
# async def lifespan(_: FastAPI) -> AsyncIterator[None]:
#     redis = Redis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#     yield



app = FastAPI(
    # lifespan=lifespan,
    title="Бронирование Отелей",
    version="0.1.0",
    root_path="/api",
)


app.include_router(router_users)
app.include_router(router_booking)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_images)
app.include_router(router_importer)
app.include_router(router_prometheus)

app = VersionedFastAPI(app,
                       version_format='{major}',
                       prefix_format='/v{major}',
                       description='Greet users with a nice message',

                       )



redis = Redis.from_url(settings.UPSTASH_REDIS_URL)
FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")



instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    log.info("Request execute time:%s", extra={"process_time": round(process_time, 3)})
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080)
