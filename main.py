from contextlib import asynccontextmanager

from fastapi import FastAPI

from repository import models
from repository.db import engine
from routes.index import root_route


@asynccontextmanager
async def lifecycle(app: FastAPI):
    # Before start
    print("Starting app")
    yield
    # After shutdown
    print("Shutting down app")


app = FastAPI(lifespan=lifecycle)

# models.Base.metadata.create_all(bind=engine)

# @app.middleware("http")
# async def validate_auth_headers(request: Request, call_next):
#     if request.url.path == "/api/v1/auth/login":
#         return await call_next(request)
#
#     if "Authorization" not in request.headers:
#         return Response(status_code=401)
#
#     return await call_next(request)


app.include_router(root_route)
