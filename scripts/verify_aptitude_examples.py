"""Exact arithmetic, enumeration, and finite-model checks for Module 6.

These checks complement the schema validator and editorial content review.
No numerical answer is established using approximate random simulation.
"""

import argparse
from fractions import Fraction as F
import itertools as it
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {"6.1": "6.1_quantitative_arithmetic.json"}
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subpart", choices=FILES, action="append")
    args = parser.parse_args()
    for sid in args.subpart or FILES:
        path = ROOT / "questions/module_6_aptitude" / FILES[sid]
        QUESTIONS.update({q["id"]: q for q in json.loads(path.read_text(encoding="utf-8"))})
        {"6.1": arithmetic}[sid]()
    print(f"PASS: {len(CHECKED)} exact/model-checked keys; editorial review remains separate.")


if __name__ == "__main__":
    main()
