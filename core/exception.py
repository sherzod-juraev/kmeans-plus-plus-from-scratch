from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import TimeoutError
from .logging import get_logger


async def get_ip(request: Request, /) -> str:
    client_ip = request.headers.get('X-Forwarded-For')
    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    else:
        client_ip = request.client.host
    return client_ip


async def get_route_path(request: Request, /) -> str:
    route_path = request.scope.get('route')
    if route_path:
        route_path = getattr(route_path, 'path', request.url.path)
    else:
        route_path = request.url.path
    return route_path


def register_exception_handler(app: FastAPI, /):

    logger = get_logger('exception_handler')
    @app.exception_handler(TimeoutError)
    async def timeout_exception_handler(
            request: Request,
            exc: TimeoutError
    ):
        client_ip = await get_ip(request)
        route_path = await get_route_path(request)
        logger.warning(f"{client_ip} {request.method} {route_path} 503 TimeoutError")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                'detail': 'There are not enough  server resources. Please try again later'
            }
        )


    @app.exception_handler(ResponseValidationError)
    async def response_validation_exception_handler(
            request: Request,
            exc: ResponseValidationError
    ):
        client_ip = await get_ip(request)
        route_path = await get_route_path(request)
        logger.warning(f"{client_ip} {request.method} {route_path} 503 ResponseValidationError")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                'detail': 'Server response error'
            }
        )


    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
            request: Request,
            exc: RequestValidationError
    ):
        client_ip = await get_ip(request)
        route_path = await get_route_path(request)
        logger.warning(f"{client_ip} {request.method} {route_path} 400 RequestValidationError")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'detail': 'Error in request',
                'body': exc.errors()
            }
        )


    @app.exception_handler(ValueError)
    async def value_error_exception_handler(
            request: Request,
            exc: ValueError
    ):
        client_ip = await get_ip(request)
        route_path = await get_route_path(request)
        logger.warning(f"{client_ip} {request.method} {route_path} 503 ValueError")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'detail': str(exc)
            }
        )


    @app.exception_handler(Exception)
    async def global_exception_handler(
            request: Request,
            exc: Exception
    ):
        client_ip = await get_ip(request)
        route_path = await get_route_path(request)
        logger.error(f"{client_ip} {request.method} {route_path} 500 {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'detail': 'Internal server error'
            }
        )