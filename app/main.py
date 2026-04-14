import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logging import configure_logging, get_logger
from app.config import config_status
from app.routes import sync, plan, act, run

configure_logging()
log = get_logger()


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
        import structlog
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=req_id)
        response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    status = config_status()
    log.info("tardis_startup", config=status)
    missing = [k for k, v in status.items() if not v]
    if missing:
        log.warning("missing_config", keys=missing)
    yield
    log.info("tardis_shutdown")


app = FastAPI(title="TARDIS", version="0.1.0", lifespan=lifespan)
app.add_middleware(CorrelationIDMiddleware)

app.include_router(sync.router)
app.include_router(plan.router)
app.include_router(act.router)
app.include_router(run.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "tardis", "version": "0.1.0", "config": config_status()}
