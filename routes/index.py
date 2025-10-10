from fastapi import APIRouter
from .requisitions import route as requisitions_route
from .orders import route as orders_route
from .users import route as users_route
from .auth import route as auth_route
from .health import route as health_route

root_route = APIRouter(prefix="/api/v1", tags=["root"])

root_route.include_router(health_route, prefix="/health")
root_route.include_router(auth_route, prefix="/auth")
root_route.include_router(users_route, prefix="/users")
root_route.include_router(requisitions_route, prefix="/requisitions")
root_route.include_router(orders_route, prefix="/orders")
