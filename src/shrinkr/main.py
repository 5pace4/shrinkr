import uvicorn

from fastapi import FastAPI
from shrinkr.config import settings
from shrinkr.routes import users, health, urls

app = FastAPI(
    title="Shrinkr API",
    version="1.0.0"
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