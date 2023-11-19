from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def hello() -> str:
    return "Hello, World!"
