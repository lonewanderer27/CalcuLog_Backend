import requests
import math
from constants import WOLFRAM_APPID


def truncate(number, digits) -> float:
    # Improve accuracy with floating point operations, to avoid truncate(16.4, 2) = 16.39 or truncate(-1.13, 2) = -1.12
    nbDecimals = len(str(number).split('.')[1])
    if nbDecimals <= digits:
        return number
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


def wolfram(equation: str) -> float:
    print("equation:", equation)

    # replace all four operations with a literal word
    equation_convd = equation.replace(
        "+", " add ").replace("-", " minus ").replace("*", " times ").replace("/", " divide ")

    print("input_converted:", equation_convd)

    response = requests.get("https://api.wolframalpha.com/v2/query", params={
        "appid": WOLFRAM_APPID,
        "input": equation_convd,
        "format": "plaintext",
        "output": "json"
    })
    print(response.url)

    return float(response.json()["queryresult"]["pods"][1]["subpods"][0]["plaintext"])


def compute_error(true_value: float, approx_value: float) -> list[float]:
    absolute_error = abs(true_value - approx_value)
    percentage_relative_error = abs(absolute_error / true_value) * 100
    return [absolute_error, percentage_relative_error]


def parse_roundingchopping(value: float, roundingchopping: str, numDigits: int):
    if roundingchopping == "chopping":
        return truncate(value, numDigits)
    else:
        return round(value, numDigits)
