import uvicorn

from fastapi import FastAPI
from shrinkr.routes import users

app = FastAPI(
    title="Shrinkr API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "status": "ok"
    }

app.include_router(
    users.router,
    prefix="/api"
)


def dev() -> None:
    uvicorn.run("shrinkr.main:app", host="127.0.0.1", port=8000, reload=True)