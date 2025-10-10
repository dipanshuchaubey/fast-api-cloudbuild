import os
from fastapi import APIRouter
from logging import getLogger

logger = getLogger(__name__)
route = APIRouter()

@route.get("")
def get_health():
    hostname = os.uname().nodename
    logger.info(f"Health check from host: {hostname}")

    return {"status": "ok", "hostname": hostname}