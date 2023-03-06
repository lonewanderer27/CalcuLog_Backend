from typing import Union
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return "Hello World"

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0")