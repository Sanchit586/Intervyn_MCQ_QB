"""Independently check numerical keys; conceptual answers require content review."""

import argparse
import ast
from fractions import Fraction as F
import itertools as it
import json
import math
from pathlib import Path
import statistics as stats

ROOT = Path(__file__).resolve().parents[1]
FILES = {"5.1": "5.1_statistics_probability.json"}
QUESTIONS = {}
CHECKED = set()


def number_expression(text):
    """Evaluate restricted numeric option arithmetic, never arbitrary Python."""
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            return visit(node.operand) * (-1 if isinstance(node.op, ast.USub) else 1)
        if isinstance(node, ast.BinOp):
            a, b = visit(node.left), visit(node.right)
            operations = {ast.Add: lambda: a+b, ast.Sub: lambda: a-b,
                          ast.Mult: lambda: a*b, ast.Div: lambda: a/b, ast.Pow: lambda: a**b}
            if type(node.op) in operations:
                return operations[type(node.op)]()
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "sqrt" and len(node.args) == 1 and not node.keywords):
            return math.sqrt(visit(node.args[0]))
        raise ValueError("Unsupported numeric expression")
    return visit(ast.parse(text, mode="eval").body)


def numeric(sid, index, value, tolerance=1e-10):
    qid = f"{sid}-{index:03}"
    q = QUESTIONS[qid]
    matches = []
    for key, text in q["options"].items():
        try:
            result = number_expression(text)
        except (ValueError, SyntaxError, ZeroDivisionError):
            continue
        if math.isclose(float(result), float(value), rel_tol=tolerance, abs_tol=tolerance):
            matches.append(key)
    assert matches == [q["correct_answer"]], (qid, value, matches)
    CHECKED.add(qid)


def exact(sid, index, text):
    qid = f"{sid}-{index:03}"
    q = QUESTIONS[qid]
    assert q["options"][q["correct_answer"]] == text, (qid, text)
    CHECKED.add(qid)


def foundations():
    sid = "5.1"
    calculations = {
        1: stats.mean([2, 4, 6, 8]), 2: stats.median([2, 3, 7, 9]),
        3: stats.mode([2, 2, 3, 5, 5, 5]), 4: stats.pvariance([1, 3]),
        5: stats.variance([2, 4, 6]), 6: math.sqrt(9), 7: 19-12,
        9: F(38, 10)-3, 10: F(12, 30), 11: 1-F(27, 100),
        12: 2*F(3, 4), 13: F(1, 5)*F(4, 5),
        15: (20*70+30*80)/50, 16: stats.pvariance([1, 3, 5, 7]),
        18: stats.stdev([1, 2, 3]),
        19: stats.median([8, 9, 11, 13])-stats.median([1, 2, 4, 6]),
        20: stats.pvariance([1]*2+[2]*5+[3]*3), 21: 4+9, 22: 4+9+2*(-2),
        23: F(40*5, 60*2+40*5), 24: F(90, 90+99*10),
        25: F(2, 3)/(F(2, 3)+F(1, 3)),
        29: F(3, 10)*F(2, 10)+F(7, 10)*F(1, 10),
        30: 10*F(1, 5)-1, 31: 2*3-5, 32: 2*4,
        33: F(2*8*8, 2*8*8+8), 34: F(1, 1+9*8),
        35: stats.pvariance([1, 1, 3, 5]), 36: -F(6, 10),
        43: (F(1, 10)*100)/(F(1, 10)*10)**2-3,
        44: (4*9+2*math.comb(4, 2)*3)/16,
    }
    for index, result in calculations.items():
        numeric(sid, index, result)
    exact(sid, 14, f"{stats.median([1, 2, 3, 4, 100])}, {stats.mean([1, 2, 3, 4, 100])}")
    exact(sid, 17, f"{3*4-2}, {3**2*5}")
    pairs = list(it.permutations(list(enumerate("RRRBB")), 2))
    numeric(sid, 26, F(sum(a[1] == b[1] == "R" for a, b in pairs), len(pairs)))
    coins = [p for p in it.product("HT", repeat=2) if "H" in p]
    numeric(sid, 27, F(coins.count(("H", "H")), len(coins)))
    wins = F(0)
    for prize in range(3):
        eligible = [d for d in range(3) if d != 0 and d != prize]
        for opened in eligible:
            switched = next(d for d in range(3) if d not in (0, opened))
            wins += F(switched == prize, 3*len(eligible))
    numeric(sid, 37, wins)
    observations = [(b, p) for b in ("GG", "GS", "SS") for p in range(2) if b[p] == "G"]
    numeric(sid, 38, F(sum(b[1-p] == "G" for b, p in observations), len(observations)))
    assert F(80, 100) > F(90, 120) and F(20, 100) > F(1, 10) and F(100, 200) < F(91, 130)
    exact(sid, 39, "A has a higher rate in each segment but a lower pooled rate")
    families = [(f, c) for f in it.product("BG", repeat=2) for c in range(2) if f[c] == "B"]
    numeric(sid, 40, F(sum(f == ("B", "B") for f, _ in families), len(families)))
    # Exact mixture PMF, independently checking the total-variance derivation.
    pmf = [sum(F(1, 2)*math.comb(10, k)*p**k*(1-p)**(10-k)
               for p in (F(1, 5), F(4, 5))) for k in range(11)]
    mean = sum(k*p for k, p in enumerate(pmf))
    numeric(sid, 41, sum((k-mean)**2*p for k, p in enumerate(pmf)))
    x = [-1, 0, 1]
    assert sum(v**3 for v in x) == 0 and F(x.count(0), 3) != 1
    exact(sid, 42, "Cov(X,Y)=0, but X and Y are dependent")
    dice = [p for p in it.product(range(1, 7), repeat=2) if max(p) == 4]
    numeric(sid, 45, F(sum(map(sum, dice)), len(dice)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subpart", choices=FILES, action="append")
    args = parser.parse_args()
    for sid in args.subpart or FILES:
        path = ROOT / "questions/module_5_data_science" / FILES[sid]
        QUESTIONS.update({q["id"]: q for q in json.loads(path.read_text(encoding="utf-8"))})
        {"5.1": foundations}[sid]()
    print(f"PASS: {len(CHECKED)} numerical/enumerated answer keys; conceptual answers need separate review.")


if __name__ == "__main__":
    main()
