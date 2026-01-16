from fastapi import Request
from time import perf_counter
from .logging import get_logger


logger = get_logger('middleware')


async def log_request_middleware(request: Request, call_next):

    start = perf_counter()
    response = await call_next(request)
    duration_time = (perf_counter() - start) * 1000
    client_ip = request.headers.get('X-Forwarded-For')
    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    else:
        client_ip = request.client.host
    route_path = request.scope.get('route')
    if route_path:
        route_path = getattr(route_path, 'path', request.url.path)
    else:
        route_path = request.url.path
    logger.info(f"{client_ip} {request.method} {route_path} {response.status_code} {duration_time:.6f}ms")
    return response