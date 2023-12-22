from fastapi import FastAPI
from uvicorn import run

app = FastAPI()


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    run(app, host="localhost", port=8081)
