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
        return [round(value, numDigits), truncate(value, numDigits)]

    if roundingchopping == "CHOPPING":
        return [truncate(value, numDigits)]
    else:
        return [round(value, numDigits)]


def ln_taylormaclaurin(xvar: int, nthDegree: int):
    dvs = []

    for cd in range(1, nthDegree+1):
        # print("cd: ", cd)
        if cd == 1:
            dvs.append(1)
        elif cd % 2 == 0:
            #   - (1    * d1)
            d = -((cd-1)*dvs[cd-2]/(0+1)**cd)
            dvs.append(d)
        elif cd % 2 != 0:
            d = ((cd-1)*-dvs[cd-2]/(0+1)**cd)
            dvs.append(d)
        # print("dvs: ", dvs)

    print("derivatives: ", dvs)

    # COMPUTING TRUE VALUE:
    final_ans = 0
    dlast = dvs[-1]
    print("last derivative: ", dlast)

    # ct = current term
    for ct in range(1, nthDegree+1):
        if ct == 1:
            final_ans = xvar
        elif ct % 2 == 0:
            final_ans -= (xvar**ct)/ct
        else:
            final_ans += (xvar**ct)/ct
        print(ct)

    print("final_ans: ", final_ans)
    return final_ans
