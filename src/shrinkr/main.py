import uvicorn

from fastapi import FastAPI
from shrinkr.routes import users, health

app = FastAPI(
    title="Shrinkr API",
    version="1.0.0"
)

app.include_router(
    health.router
)

app.include_router(
    users.router,
    prefix="/api"
)


def dev() -> None:
    uvicorn.run("shrinkr.main:app", host="127.0.0.1", port=8000, reload=True)