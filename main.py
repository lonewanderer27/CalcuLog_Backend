from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from internet import internet
from solvers import wolfram, compute_error, parse_roundingchopping, approx_ln, approx_taylormaclaurin

import uvicorn

app = FastAPI(title="CalcuLog Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

v1 = FastAPI(title="CalcuLog API v1")
v2 = FastAPI(title="CalcuLog API v2")


@app.get("/")
async def root(request: Request):
    return HTMLResponse(
        f'CalcuLog Backend<br><br>'
        f'API v1 Docs : <a href="{request.url._url}api/v1/docs">{request.url._url}api/v1/docs</a> <br/>'
        f'API v1 Route : <a href="{request.url._url}api/v1/">{request.url._url}api/v1/</a> <br/><br/>'
        f'API v2 Docs : <a href="{request.url._url}api/v2/docs">{request.url._url}api/v2/docs</a> <br/>'
        f'API v2 Route : <a href="{request.url._url}api/v2/">{request.url._url}api/v2/</a> <br/>'
    )


@v1.get("/pe/", name="Propagation Error v1")
async def propagation_error(
    trueValue: str,
    approxValue: str,
    roundingchopping: str,
    numDigits: int
):
    true_value_result = 0
    try:
        # if only number is given, then we assign it directly as the true value
        true_value_result = eval(trueValue)
        print("equation has no special symbols, solvable!")
    except:
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

    # we chop or round the approximated value
    approx_value_result = parse_roundingchopping(
        approx_value_result, roundingchopping, numDigits)

    # compute absolute_error
    [ab_error, percentage_relative_error] = compute_error(
        true_value_result, approx_value_result)
    print("absolute_error:", ab_error)
    print("percentage_relative_error:", percentage_relative_error)

    ab_error = parse_roundingchopping(ab_error, roundingchopping, numDigits)
    percentage_relative_error = parse_roundingchopping(
        percentage_relative_error, roundingchopping, numDigits)

    # return the result as json object
    return {
        "absolute_error": ab_error,
        "percentage_relative_error": percentage_relative_error,
        "steps": [
            ""
        ]
    }


@v2.get("/pe/", name="Propagation Error v2")
async def propagation_error2(
    trueValue: str,
    roundingchopping: str,
    numDigits: int,
):
    try:
        # if only number is given, then we assign it directly as the true value
        true_value_result = eval(trueValue)
        print("equation has no special symbols, solvable!")
    except:
        # otherwise, if it's an equation we compute the true value
        true_value_result = wolfram(trueValue)
        print("true_value result:", true_value_result)

    approx_value = parse_roundingchopping(
        true_value_result, roundingchopping, numDigits)

    [ab_error, percentage_relative_error] = compute_error(
        true_value_result, approx_value
    )
    print("approx_value:", approx_value)
    print("absolute_error:", ab_error)
    print("percentage_relative_error:", percentage_relative_error)

    return {
        "approx_value": approx_value,
        "absolute_error": ab_error,
        "percentage_relative_error": percentage_relative_error
    }


@v1.get("/tm")
async def taylor_maclaurin(
    point: int,
    nthDegree: int,
    roundingchopping: str,
    numDigits: int,
):
    x = 1e-10   # default value
    true_value_result = approx_ln(x)
    approx_value_result = approx_taylormaclaurin(x, point, nthDegree)
    print("true_value: ", true_value_result)
    print("approx_value: ", approx_value_result)

    approx_value = parse_roundingchopping(
        approx_value_result, roundingchopping, numDigits
    )
    print("approx_value: ", approx_value)

    [ab_error, percentage_relative_error] = compute_error(
        true_value_result, approx_value
    )

    print("appox_value:", approx_value)
    print("absolute_error:", ab_error)
    print("percentage_relative_error:", percentage_relative_error)

    return {
        "approx_value": approx_value,
        "absolute_error": ab_error,
        "percentage_relative_error": percentage_relative_error
    }

app.mount("/api/v1", v1)
app.mount("/api/v2", v2)

if __name__ == "__main__":
    print("Starting CalcuLog Backend API")
    print("checking if there's internet")
    if internet():
        print("there is! proceeding")
        uvicorn.run("main:app", host="0.0.0.0")
    else:
        print("you need active internet connection to run the backend! Please check then try again.")
