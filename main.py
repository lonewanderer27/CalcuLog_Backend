from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from solvers import wolfram, compute_absolute_error, parse_roundingchopping

import uvicorn

app = FastAPI(title="CalcuLog Backend")


class PEvalues(BaseModel):
    trueValue: str
    approxValue: float
    roundingchopping: str
    numDigits: float


class PEresult(BaseModel):
    absolute_error: float
    absolute_percentage_error: float
    relative_error: float
    relative_percentage_error: float


class TMvalues(BaseModel):
    function: str
    point: float
    nthDegree: float


@app.get("/")
async def root(request: Request):
    return f"CalcuLog Backend | Go to this URL for docs: {request.url._url}docs"


@app.get("/pe")
async def propagation_error(
    trueValue: str,
    approxValue: str,
    roundingchopping: str,
    numDigits: int
):
    try:
        # if only number is given, then we assign it directly as the true value
        true_value_result = float(trueValue)
    except ValueError:
        # otherwise, if it's an equation we compute the true value
        true_value_result = wolfram(trueValue)
        print("true_value result:", true_value_result)

    try:
        # if only number is given, then we assign it directly as the approx value
        approx_value_result = float(approxValue)
    except ValueError:
        # otherwise, if it's an equation we compute the approx value
        approx_value_result = wolfram(approxValue)
        print("approx_value result:", approx_value_result)

    # compute absolute_error
    [ab_error, ab_error_percentage] = compute_absolute_error(
        true_value_result, approx_value_result)
    print("ab_error:", ab_error)
    print("ab_error_percentage:", ab_error_percentage)

    ab_error = parse_roundingchopping(ab_error, roundingchopping, numDigits)
    ab_error_percentage = parse_roundingchopping(
        ab_error_percentage, roundingchopping, numDigits)

    # return the result as json object
    return {
        "absolute_error": ab_error,
        "absolute_error_percentage": ab_error_percentage,
    }


@app.post("/tm")
async def taylor_maclaurin(TMvalues: TMvalues):
    return "Taylor Maclaurin"

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0")
