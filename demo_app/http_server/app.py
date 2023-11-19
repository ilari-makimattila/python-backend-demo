from fastapi import FastAPI
from .routes import measurements


app = FastAPI()
app.include_router(measurements.router)


@app.get("/")
async def hello() -> str:
    return "Hello, World!"
