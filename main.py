from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="CalcuLog Backend")


class PEvalues(BaseModel):
    trueValue: str
    approxValue: float
    roundingchopping: str
    numDigits: float


class TMvalues(BaseModel):
    function: str
    point: float
    nthDegree: float


@app.get("/")
async def root(request: Request):
    return f"CalcuLog Backend | Go to this URL for docs: {request.url._url}docs"


@app.post("/propagationError")
async def propagation_error(PEvalues: PEvalues):
    return "Propagation Error"


@app.post("/taylorMaclaurin")
async def taylor_maclaurin(TMvalues: TMvalues):
    return "Taylor Maclaurin"

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0")
