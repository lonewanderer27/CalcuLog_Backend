import requests
import math
from constants import WOLFRAM_APPID
from pprint import pprint
import re


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
        "podtitle": ["Decimal approximation", "Result"],
        "format": "plaintext",
        "output": "json"
    })
    print("Wolfram: ", response.url)

    # display the result
    # pprint(response.json(), indent=2)

    init_result = ""
    try:
        for x in response.json()["queryresult"]["pods"]:
            if x["title"] == "Decimal approximation":
                init_result = x["subpods"][0]["plaintext"]
            elif x["title"] == "Result":
                init_result = x["subpods"][0]["plaintext"]
    except:
        print("There is no result!")

    # remove all special characters
    init_result = re.sub("[^A-Za-z0-9.]", "", init_result)

    print("init_result:", init_result)
    final_result = init_result.replace("...", "")
    print("final_result:", final_result)

    return float(final_result)


def compute_error(true_value: float, approx_value: float) -> list[float]:
    absolute_error = abs(true_value - approx_value)
    percentage_relative_error = abs(absolute_error / true_value) * 100
    return [absolute_error, percentage_relative_error]


def parse_roundingchopping(value: float, roundingchopping: str, numDigits: int) -> list[float]:
    if roundingchopping == "BOTH":
        return [truncate(value, numDigits), round(value, numDigits)]

    if roundingchopping == "CHOPPING":
        return [truncate(value, numDigits)]
    else:
        return [round(value, numDigits)]


def approx_taylormaclaurin_ln(x: int, n: int):
    result = 0
    for i in range(1, n+1):
        result += (-1)**(i+1) * (x**i / i)
    return result
