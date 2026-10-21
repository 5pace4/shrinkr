import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from shrinkr.config import settings
from shrinkr.rate_limit import limiter
from shrinkr.routes import users, health, urls

app_settings = settings()

app = FastAPI(
    title="Shrinkr API",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in app_settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    health.router,
    prefix="/api"
)

app.include_router(
    users.router,
    prefix="/api"
)

app.include_router(
    urls.router,
    prefix="/api"
)

def dev() -> None:
    app_settings = settings()

    uvicorn.run(
        "shrinkr.main:app",
        host=app_settings.app_host,
        port=app_settings.app_port,
        reload=True,
    )