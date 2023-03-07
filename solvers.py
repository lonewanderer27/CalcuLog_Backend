import requests
import math
from constants import WOLFRAM_APPID
from pprint import pprint


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
        "podtitle": "Decimal approximation",
        "format": "plaintext",
        "output": "json"
    })
    print("Wolfram: ", response.url)

    # pprint(response.json(), indent=2)
    init_result: str = response.json(
    )["queryresult"]["pods"][0]["subpods"][0]["plaintext"]
    print("init_result:", init_result)
    final_result = init_result.replace("...", "")
    print("final_result:", final_result)

    return float(final_result)


def compute_error(true_value: float, approx_value: float) -> list[float]:
    absolute_error = abs(true_value - approx_value)
    percentage_relative_error = abs(absolute_error / true_value) * 100
    return [absolute_error, percentage_relative_error]


def parse_roundingchopping(value: float, roundingchopping: str, numDigits: int) -> float:
    if roundingchopping == "CHOPPING":
        return truncate(value, numDigits)
    else:
        return round(value, numDigits)


def approx_ln(x) -> float:
    if x <= -1:
        print("float-inf")
        return float('-inf')
    else:
        print("math.log has value!")
        return math.log(x + 1)


def approx_taylormaclaurin(x: int, point: int, nthDegree: int) -> float:
    if x <= -1:
        return float('-int')
    else:
        terms = [((-1)**n * (x - point)**(n+1)) / (n+1)
                 for n in range(nthDegree)]
        return sum(terms)
