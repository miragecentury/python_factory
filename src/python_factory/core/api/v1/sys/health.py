"""
API v1 sys health module.

Provide the Get health endpoint
"""

from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse

api_v1_sys_health = APIRouter(prefix="/health")


@api_v1_sys_health.get(path="", tags=["sys"])
def get_api_v1_sys_health() -> JSONResponse:
    """
    Get the health of the system.
    Args:
        request (Request): The request object.
    Returns:
        Response: The response object.
    """
    return JSONResponse(status_code=HTTPStatus.OK.value, content={"status": "OK"})
