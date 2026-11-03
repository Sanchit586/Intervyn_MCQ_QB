"""Exact arithmetic, enumeration, and finite-model checks for Module 6.

These checks complement the schema validator and editorial content review.
No numerical answer is established using approximate random simulation.
"""

import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import itertools as it
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {"6.1": "6.1_quantitative_arithmetic.json", "6.2": "6.2_higher_modern_math.json"}
QUESTIONS = {}
CHECKED = set()


def number(sid, index, value):
    qid = f"{sid}-{index:03}"
    q = QUESTIONS[qid]
    options = {key: F(text) for key, text in q["options"].items()}
    assert len(set(options.values())) == 4, (qid, "Equivalent numeric options")
    matches = [key for key, result in options.items() if result == value]
    assert matches == [q["correct_answer"]], (qid, value, matches)
    CHECKED.add(qid)


def exact(sid, index, text):
    qid = f"{sid}-{index:03}"
    q = QUESTIONS[qid]
    assert q["options"][q["correct_answer"]] == text, (qid, text)
    CHECKED.add(qid)


def alternate(rates):
    work, time = F(0), F(0)
    for rate in it.cycle(rates):
        assert rate > 0
        if work+rate >= 1:
            return time+(1-work)/rate
        work += rate
        time += 1


def arithmetic():
    v = {
        1: F(1, 10), 2: 1/(F(1, 6)+F(1, 3)),
        3: 1/(F(1, 8)-F(1, 24)), 4: F(12*10, 15),
        5: F(150, 3), 6: 60*F(5, 2), 7: 72*F(5, 18),
        8: 120/(54*F(5, 18)), 9: 10+2, 10: F(18, 100)*250,
        11: 400*F(115, 100), 12: F(30, 120)*100,
        13: F(1000-800, 800)*100, 14: F(500-450, 500)*100,
        15: 1000*F(80, 100), 16: 250*F(120, 100),
        17: 64*F(3, 8), 18: 18*F(2, 3), 19: F(150, 5)*8,
        20: 90*F(2, 5), 21: 1000*F(1, 10)*2,
        22: 2000*(1+F(5, 100)*3), 23: 1000*F(11, 10)**2,
        24: 1000*(F(11, 10)**2-1-F(2, 10)),
        25: 1/(F(1, 12)+F(1, 18)), 26: 1/(F(1, 6)-F(1, 10)),
        27: 10/(1-F(5, 15)), 28: 1/(F(1, 6)+F(1, 8)-F(1, 24)),
        29: 1/(F(1, 10)-F(1, 15)), 30: alternate([F(1, 5), F(1, 10)]),
        31: 6+F(20*18-20*6, 10), 32: 10*F(3, 2),
        33: F(12*6*10, 15*8), 34: 250/(90*F(5, 18)),
        35: 300/(18*F(5, 18)), 36: 250/(45*F(5, 18)),
        37: (F(24, 2)-F(24, 3))/2, 38: F(2*40*60, 40+60),
        39: F(40+60, 2), 40: F(300, 40+60),
        41: (F(60, 40)-F(60, 50))*60, 42: 750/(54*F(5, 18)),
        43: 100*F(6, 5)*F(4, 5), 44: (1-F(4, 5)*F(9, 10))*100,
        45: (F(7, 5)*F(9, 10)-1)*100,
        46: 900/F(9, 10), 47: 1080/F(6, 5),
        48: (1-F(2400, 1)/(1200/F(6, 5)+1200/F(4, 5)))*100,
        49: 720/F(9, 10), 50: (1-1/F(5, 4))*100,
        51: 7*100, 52: 3*F(6, 1), 53: F(30, 50+10),
        54: F(2, 3)*F(4, 5), 55: F(8*3, 6*4),
        56: 2000*F(21, 20)**2, 57: F(100, 8),
        58: 10000*(F(11, 10)**2-1), 59: F(450, 3000*3)*100,
        60: 4000*F(1, 20)**2, 61: 1/(F(1, 12)+F(1, 18)+F(1, 36)),
        62: 1/(F(1, 12)-F(1, 18)), 63: 360/(F(180, 60)+F(180, 45)),
        64: (F(6, 5)*F(9, 10)-1)*100,
        65: alternate([F(1, 8), F(1, 12)]),
        66: alternate([F(1, 6)-F(1, 12), F(1, 8)-F(1, 12)]),
        67: 10/(1-F(4, 12)),
        68: 1/((F(1, 6)+F(1, 8)+F(1, 12))/2-F(1, 8)),
        69: F(12*30-12*10-8*10, 12),
        70: (F(500, 50)+F(500, 10))/2*F(18, 5),
        71: 15, 72: (F(3, 2)*F(9, 10)*F(19, 20)-1)*100,
        73: (F(90, 80)-1)*100, 74: 18000*F(3*8, 2*12+3*8+4*6),
        75: 75*F(4, 5)**3,
        76: F(3*42-4*24, 4-3),
        77: (F(11, 10)*F(6, 5)-1)/2*100,
        78: 124/(F(11, 10)**3-1-3*F(1, 10)),
        79: 2100/(F(10, 11)+F(100, 121)),
        80: 1600*(F(21, 20)**4-1),
    }
    # Verify the word-problem systems rather than only their final totals.
    assert 3*100-2*100 == 4*100-3*100 == 100
    assert F(18+6, 30+6) == F(2, 3)
    assert F(24-6, 42-6) == F(1, 2) and F(24+30, 42+30) == F(3, 4)
    for index, value in v.items():
        number("6.1", index, value)


def modern():
    c, p = math.comb, math.perm
    v = {
        1: p(5, 2), 2: c(6, 2), 3: math.factorial(4), 4: c(5, 1),
        5: sum(d[0] != 0 for d in it.permutations(range(10), 3)), 6: c(5, 3),
        7: F(3, 6), 8: F(1, 4), 9: F(13, 52), 10: F(3, 5),
        11: F(2, 5)*F(1, 2), 12: 1-F(1, 2)**3, 13: 29%5, 14: 7**2%10,
        15: next(x for x in range(10) if (4502+10*x)%9 == 0),
        16: 3+5*4, 17: sum(range(1, 11)), 18: 18*3,
        19: len(set(it.permutations("LEVEL"))), 20: 2*math.factorial(5),
        21: math.factorial(6)-2*math.factorial(5), 22: math.factorial(4),
        23: c(4, 2)*c(5, 3), 24: math.factorial(5), 25: c(7, 2), 26: p(7, 3),
        27: F(c(5, 2), c(8, 2)), 28: F(3*2, c(5, 2)),
        29: F(c(4, 2), c(52, 2)), 32: F(3, 10)*F(3, 5)+F(7, 10)*F(2, 5),
        33: F(c(4, 2), 2**4), 34: F(2, 5)**3, 35: F(4+13-1, 52),
        36: F(c(5, 2), c(10, 2)), 37: pow(2, 10, 7), 38: pow(3, 27, 10),
        39: -17%5, 40: math.lcm(12, 18), 41: math.gcd(84, 126),
        42: sum((3204+10*x)%6 == 0 for x in range(10)),
        43: sum(5+3*k for k in range(20)), 44: 31+2*F(31-11, 8-3),
        45: sum(3*2**k for k in range(6)), 46: 12/(1-F(1, 3)),
        47: math.isqrt(225), 48: 80*F(1, 2)**4,
        52: sum(sum(counts) == 8 for counts in it.product(range(1, 5), repeat=3)),
        53: F(c(4, 2)*c(48, 3), c(52, 5)), 54: F(4*3*2, c(9, 3)),
        55: F(sum(all(i != val for i, val in enumerate(order)) for order in it.permutations(range(5))), math.factorial(5)),
        57: next(x for x in range(1, 106) if x%3 == 2 and x%5 == 3 and x%7 == 2),
        58: pow(7, 100, 13), 59: (3*10**2+2*10)-(3*9**2+2*9), 60: 2,
    }
    dice = list(it.product(range(1, 7), repeat=2))
    v[30] = F(sum(sum(pair) == 9 for pair in dice), len(dice))
    conditional = [pair for pair in dice if pair[0]%2 == 0]
    v[31] = F(sum(sum(pair) == 7 for pair in conditional), len(conditional))
    conditional = [pair for pair in dice if 6 in pair]
    v[56] = F(sum(sum(pair) == 8 for pair in conditional), len(conditional))
    @lru_cache(None)
    def multiset(counts):
        if not any(counts):
            return 1
        return sum(multiset(counts[:i]+(count-1,)+counts[i+1:])
                   for i, count in enumerate(counts) if count)
    v[49] = multiset(tuple(Counter("MISSISSIPPI").values()))
    v[50] = sum(all(abs(order.index(a)-order.index(b)) == 1 for a, b in [(0, 1), (2, 3), (4, 5), (6, 7)])
                for order in it.permutations(range(8)))
    # Fix A at index zero to quotient only by rotation.
    v[51] = sum(order.index(1) not in (1, 5) for order in ((0,)+tail for tail in it.permutations(range(1, 6))))
    assert sum([3, 6, 12]) == 21 and math.prod([3, 6, 12]) == 216
    for index, value in v.items():
        number("6.2", index, value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subpart", choices=FILES, action="append")
    args = parser.parse_args()
    for sid in args.subpart or FILES:
        path = ROOT / "questions/module_6_aptitude" / FILES[sid]
        QUESTIONS.update({q["id"]: q for q in json.loads(path.read_text(encoding="utf-8"))})
        {"6.1": arithmetic, "6.2": modern}[sid]()
    print(f"PASS: {len(CHECKED)} exact/model-checked keys; editorial review remains separate.")


if __name__ == "__main__":
    main()
