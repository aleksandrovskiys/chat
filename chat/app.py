from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from uvicorn import run

from chat.routers.api.websocket import router as websocket_router


def configure_app() -> FastAPI:
    app = FastAPI()

    app.include_router(websocket_router, tags=["websocket"])
    app.mount("/static", StaticFiles(directory="static"), name="static")

    return app


app = configure_app()


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    run(app, host="localhost", port=8081)
