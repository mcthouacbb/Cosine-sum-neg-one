import math
from tabulate import tabulate
from collections import defaultdict
import sys
import argparse

sys.stdout.reconfigure(encoding='utf-8')

latex = True

def v2(n: int) -> int:
    # thanks chatgpt
    return (n & -n).bit_length() - 1

def split_2adic(terms: list[int]) -> list[list[int]]:
    g_n = defaultdict(list)
    max_2adic = 0
    for term in terms:
        n = v2(term)
        g_n[n].append(term)
        max_2adic = max(max_2adic, n)
    
    return [g_n[n] for n in range(max_2adic + 1)]

def compute_cosines(terms: list[int], input: float) -> list[float]:
    result = []
    for term in terms:
        result.append(math.cos(term * input))

    return result

def compute_cosine_sum(terms: list[int], input: float) -> float:
    result = 0
    for term in terms:
        result += math.cos(term * input)

    return result

def compute_theta_n(g_n: list[list[int]]) -> tuple[list[int], list[bool]]:
    denom = 2 ** (len(g_n) - 1)
    theta_n = [1]
    choice_n = [False]
    # we don't need g_t
    for (index, g) in enumerate(reversed(g_n[:-1])):
        prev_theta = theta_n[-1]
        val = compute_cosine_sum(g, prev_theta / denom * math.pi)
        if val > 0:
            theta_n.append(2 ** (index + 1) - prev_theta)
            choice_n.append(True)
        else:
            theta_n.append(prev_theta)
            choice_n.append(False)
        
    return theta_n, choice_n

def pi_str(num: int, denom: int) -> str:
    gcd = math.gcd(num, denom)
    num //= gcd
    denom //= gcd
    if latex:
        return f"\\frac{{{num}}}{{{denom}}}\\pi"
    return f"{num}/{denom} * pi"

def theta_n_str(n: int | str) -> str:
    if latex:
        if n == "":
            return "\\theta"
        return f"\\theta_{n}"
    if n == "":
        return "\u03B8"
    return f"\u03B8_{n}"

def compute_g_ns(g_n: list[list[int]], input: float) -> list[str]:
    result = []
    for subterms in g_n:
        result.append("{:.6f}".format(compute_cosine_sum(subterms, input)))
    return result

def compute_output_table(terms: list[int]) -> list[list[str | float]]:
    g_n = split_2adic(terms)
    theta_n, choice_n = compute_theta_n(g_n)
    denom = 2 ** (len(g_n) - 1)

    data = []
    data.append([f"{theta_n_str(0)} = {pi_str(theta_n[0], denom)}"])
    data[0] += compute_g_ns(g_n, theta_n[0] / denom * math.pi)

    for i in range(1, len(theta_n)):
        curr = theta_n[i]

        if choice_n[i]:
            data.append([f"{theta_n_str(i)} = {pi_str(2 ** i, denom)} - {theta_n_str(i - 1)} = {pi_str(curr, denom)}"])
        else:
            data.append([f"{theta_n_str(i)} = {pi_str(curr, denom)}"])
        
        data[i] += compute_g_ns(g_n, curr / denom * math.pi)

    if latex:
        for subdata in data:
            for i in range(len(subdata)):
                subdata[i] = f"${subdata[i]}$"
    return data

def output_table(terms: list[int]):
    headers = [f"${theta_n_str("n")}$"] if latex else [theta_n_str("n")]
    for subterms in split_2adic(terms):
        cos_str = ""
        for subterm in subterms:
            if not len(cos_str) == 0:
                cos_str += " + "
            if subterm == 1:
                subterm = ""
            cos_str += f"cos({subterm}{theta_n_str("")})"
        if cos_str == "":
            cos_str = " "
        if latex:
            headers.append(f"${cos_str}$")
        else:
            headers.append(cos_str)
    
    data = compute_output_table(terms)

    if latex:
        print(tabulate(data, headers=headers, tablefmt="latex_raw"))
    else:
        print(tabulate(data, headers=headers, tablefmt="grid"))

parser = argparse.ArgumentParser(description="Computing sum cosine(kx) <= -1")
parser.add_argument("-n", "--numbers", nargs="+", type=int, required=True, help="The list of integers")
parser.add_argument("-l", "--latex", action="store_true", help="Enable latex output")

args = parser.parse_args()

latex = args.latex

output_table(args.numbers)