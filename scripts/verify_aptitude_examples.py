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
FILES = {"6.1": "6.1_quantitative_arithmetic.json", "6.2": "6.2_higher_modern_math.json",
         "6.3": "6.3_logical_reasoning.json", "6.4": "6.4_verbal_ability.json"}
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


def categorical_satisfiable(statements, labels):
    """Exact unary-set satisfiability by allowed Venn regions and witnesses.

    Universal clauses eliminate regions; every existential clause needs a
    surviving witness region. Different witnesses may be different objects.
    No bound on the number of category members is imposed by this method.
    """
    def membership(region, name):
        return bool(region & (1 << labels.index(name)))
    def test(clause, region):
        kind, a, *rest = clause
        av = membership(region, a)
        bv = membership(region, rest[0]) if rest else False
        return {"all": not av or bv, "no": not (av and bv), "empty": not av,
                "some": av and bv, "some_not": av and not bv, "exists": av}[kind]
    universal = [s for s in statements if s[0] in ("all", "no", "empty")]
    existential = [s for s in statements if s[0] not in ("all", "no", "empty")]
    allowed = [r for r in range(1 << len(labels)) if all(test(s, r) for s in universal)]
    return bool(allowed) and all(any(test(s, r) for r in allowed) for s in existential)


def categorical_entails(premises, conclusion, labels):
    negative = {"all": "some_not", "no": "some", "some": "no",
                "some_not": "all", "exists": "empty", "empty": "exists"}
    negation = (negative[conclusion[0]],)+conclusion[1:]
    return not categorical_satisfiable(premises+[negation], labels)


def logic():
    sid = "6.3"
    def syll(index, labels, premises, conclusion, text):
        assert categorical_satisfiable(premises, labels), index
        assert categorical_entails(premises, conclusion, labels), index
        exact(sid, index, text)
    syll(1, "ABC", [("all", "A", "B"), ("all", "B", "C")], ("all", "A", "C"), "All A are C.")
    syll(2, "ABC", [("no", "A", "B"), ("some", "C", "A")], ("some_not", "C", "B"), "Some C are not B.")
    syll(3, "PQR", [("some", "P", "Q"), ("all", "Q", "R")], ("some", "P", "R"), "Some P are R.")
    assert categorical_satisfiable([("all", "A", "B"), ("empty", "A")], "AB")
    assert categorical_satisfiable([("all", "A", "B"), ("exists", "A")], "AB")
    exact(sid, 4, "No; A may be empty.")
    syll(5, "AB", [("some", "A", "B")], ("some", "B", "A"), "Some B are A.")
    syll(6, "CD", [("no", "C", "D")], ("no", "D", "C"), "No dogs are cats.")
    syll(7, "RT", [("all", "R", "T"), ("exists", "R")], ("exists", "T"), "Some round objects exist.")
    syll(28, "ABC", [("some", "A", "B"), ("no", "B", "C")], ("some_not", "A", "C"), "Some A are not C.")
    syll(29, "ABC", [("all", "A", "B"), ("no", "A", "C"), ("exists", "A")], ("some_not", "B", "C"), "Some B are not C.")
    syll(30, "ABC", [("no", "A", "B"), ("all", "C", "B"), ("exists", "C")], ("some_not", "B", "A"), "Some B are not A.")
    pre = [("all", "A", "B"), ("all", "C", "B")]
    assert categorical_satisfiable(pre+[("some", "A", "C")], "ABC")
    assert categorical_satisfiable(pre+[("no", "A", "C")], "ABC")
    exact(sid, 31, "Whether A and C overlap is not determined.")
    syll(32, "ABC", [("some", "A", "B"), ("some", "B", "C")], ("some", "B", "A"), "Some B are A.")
    syll(33, "ABC", [("all", "A", "B"), ("some_not", "C", "B")], ("some_not", "C", "A"), "Some C are not A.")
    syll(34, "ABC", [("no", "A", "B"), ("all", "B", "C"), ("all", "C", "A")], ("empty", "B"), "No B exist.")
    syll(35, "ABCD", [("all", "A", "B"), ("some", "B", "C"), ("no", "C", "D")], ("some_not", "B", "D"), "Some B are not D.")
    syll(73, "ABCDE", [("some", "A", "B"), ("all", "B", "C"), ("no", "C", "D"), ("some", "D", "E")], ("some_not", "E", "B"), "Some E are not B.")
    assert not categorical_satisfiable([("no", "A", "B"), ("all", "C", "A"), ("some", "C", "B")], "ABC")
    exact(sid, 74, "No interpretation satisfies all three premises.")
    syll(75, "MREA", [("all", "R", "M"), ("some", "E", "R"), ("no", "E", "A")], ("some_not", "M", "A"), "Some managers are not auditors.")

    def arrangements(index, people, constraint, query, circle=False):
        candidates = ((people[0],)+tail for tail in it.permutations(people[1:])) if circle else it.permutations(people)
        solutions = [order for order in candidates if constraint({name: i for i, name in enumerate(order)})]
        assert solutions, (index, "No seating solution")
        answers = {query(order, {name: i for i, name in enumerate(order)}) for order in solutions}
        assert len(answers) == 1, (index, solutions, answers)
        exact(sid, index, answers.pop())
    arrangements(8, "ABCDE", lambda p: p['A']==0 and p['B']==p['A']+1 and p['C']==p['B']+1, lambda o,p:str(p['C']+1))
    arrangements(9, "ABCD", lambda p:p['A']<p['B']<p['C']<p['D'], lambda o,p:o[1])
    exact(sid, 10, str(7+1-3))
    arrangements(11, "ABCD", lambda p:p['C']==2 and p['B']==1, lambda o,p:o[(p['B']+2)%4], True)
    arrangements(36, "PQRSTU", lambda p:p['P']==0 and p['U']==5 and p['Q']+1==p['R'] and p['R']+1==p['S'] and p['S']+1==p['T'], lambda o,p:o[3])
    exact(sid, 37, "ABCDE"[2+1])
    exact(sid, 38, "ABCDEF"[(2+1)%6])
    exact(sid, 39, "ABCDEF"[(2-1)%6])
    exact(sid, 40, "ABCDEFGH"[(5-2)%8])
    arrangements(41, "ABCDEFG", lambda p:p['C']==3 and p['A']==p['C']-2 and p['A']<p['B']<p['C'] and p['D']==0 and p['E']==6 and p['F']==5, lambda o,p:str(p['G']+1))
    arrangements(42, "ABCDEF", lambda p:p['D']==p['A']+3 and p['B']==p['A']+1 and p['C']==p['D']-1 and p['E']==0, lambda o,p:o[p['B']+1])
    arrangements(43, "ABCDE", lambda p:p['B']+1==p['D'] and p['C']==p['D']+1 and p['A']<p['B'] and p['E']==4, lambda o,p:o[2])
    exact(sid, 44, "ABCDEF"[(1-1)%6])
    exact(sid, 45, str(5+8-1))
    arrangements(77, "ABCDEF", lambda p:p['F']==1 and p['E']==3 and (p['C']-p['D'])%6==3 and (p['B']-p['D'])%6==5, lambda o,p:o[(p['F']+2)%6], True)
    arrangements(78, "ABCDEFGH", lambda p:p['A']==1 and p['H']==0 and p['G']==7 and p['D']==6 and p['E']==p['F']+2 and p['C']==p['F']+1 and p['B']==p['D']-1, lambda o,p:o[p['D']-2])
    arrangements(79, "ABCDEFGH", lambda p:p['D']==4 and p['B']==3 and p['C']==1 and p['F']==2 and p['H']==5 and p['G']==7, lambda o,p:o[(p['F']+3)%8], True)
    arrangements(81, "ABCDEF", lambda p:p['D']==3 and p['B']==1 and p['E']==4 and p['F']==5, lambda o,p:o[((p['B']+3)%6+1)%6], True)
    role_answers = set()
    for order in it.permutations("ABCDE"):
        p = {name:i for i,name in enumerate(order)}
        if not (p['C']==2 and p['B']==1 and p['A']<p['B'] and p['E']==4):
            continue
        for roles in it.permutations(["Analyst", "Coder", "Designer", "Manager", "Tester"]):
            r = {role:i for i,role in enumerate(roles)}
            if r['Coder']==p['B']+1 and r['Designer']==r['Coder']-1 and r['Analyst']==p['D'] and r['Manager']==4:
                role_answers.add(roles[p['A']])
    assert len(role_answers)==1
    exact(sid, 76, role_answers.pop())
    color_answers = set()
    for order in it.permutations("PQRST"):
        p = {name:i for i,name in enumerate(order)}
        if not (p['R']==0 and p['Q']==3 and p['T']==p['P']+1):
            continue
        for colors in it.permutations(["Blue", "Green", "Red", "White", "Black"]):
            r = {color:i for i,color in enumerate(colors)}
            if r['Red']==2 and r['Black']==p['Q']+1 and r['Green']==p['P'] and r['Blue']==p['R']:
                color_answers.add(colors[r['Black']-1])
    assert len(color_answers)==1
    exact(sid, 80, color_answers.pop())

    # Coordinate vectors and turns are derived without interpreting prose at run time.
    exact(sid, 16, f"{math.isqrt(3**2+4**2)} km")
    compass = ["North", "East", "South", "West"]
    exact(sid, 17, compass[(1-1)%4])
    exact(sid, 18, f"{5-2} km north")
    exact(sid, 19, "Northwest" if -4<0 and 3>0 else "invalid")
    exact(sid, 54, f"{6-2} km east")
    exact(sid, 55, compass[(0+1+1-1)%4])
    exact(sid, 56, f"{4+3} km north")
    exact(sid, 57, f"{math.isqrt(6**2+8**2)} km")
    exact(sid, 58, "Northwest" if 3-7<0 and 4-1>0 else "invalid")
    exact(sid, 59, f"{6-2} km north")
    exact(sid, 85, f"{8-3} km north; facing {compass[(1-1+1+1+1)%4].lower()}")
    exact(sid, 86, f"{math.isqrt((12-6)**2+(5-13)**2)} km")
    shift = lambda word, amount: ''.join(chr((ord(ch)-65+amount)%26+65) for ch in word)
    exact(sid, 20, shift("CAT", 1))
    exact(sid, 21, str(sum(ord(ch)-64 for ch in "DOG")))
    exact(sid, 22, "TEAM"[::-1])
    exact(sid, 23, ''.join(chr(90-(ord(ch)-65)) for ch in "CODE"))
    exact(sid, 24, (set("ka mi".split()) & set("mi tu".split())).pop())
    exact(sid, 60, shift("ZOO", 2))
    exact(sid, 61, shift("TRAIN"[::-1], 1))
    exact(sid, 62, ''.join(shift(ch, 1 if i%2==0 else -1) for i,ch in enumerate("CODE")))
    exact(sid, 63, str(sum((i+1)*(ord(ch)-64) for i,ch in enumerate("CAB"))))
    exact(sid, 64, (set("ti so".split())-set("ti pa".split())).pop())
    exact(sid, 65, f"{'CLOUD'[-1]}{len('CLOUD')}{'CLOUD'[0]}")
    exact(sid, 87, ''.join(shift(ch, i+1) for i,ch in enumerate("CODE"[::-1])))

    classifications = ["Statement 1 alone is sufficient; Statement 2 alone is not.",
                       "Statement 2 alone is sufficient; Statement 1 alone is not.",
                       "Both statements together are sufficient, but neither alone is.",
                       "Even both statements together are insufficient."]
    def suff(index, domain, first, second, query):
        domain = list(domain)
        sets = [[case for case in domain if condition(case)] for condition in (first, second, lambda c:first(c) and second(c))]
        assert all(sets), (index, "Inconsistent sufficiency statements")
        sufficient = [len({query(case) for case in cases})==1 for cases in sets]
        a,b,together = sufficient
        assert not (a and b), (index, "Unlisted both-alone classification")
        category = 0 if a else 1 if b else 2 if together else 3
        exact(sid, index, classifications[category])
    suff(25, range(-3,4), lambda x:x==3, lambda x:x*x==9, lambda x:x>0)
    suff(26, range(10), lambda x:x>2, lambda x:x==4, lambda x:x)
    suff(27, it.product(range(10), repeat=2), lambda p:p[0]==1, lambda p:p[1]==2, sum)
    suff(66, range(1,21), lambda x:x%4==0, lambda x:x%3==0, lambda x:x%2==0)
    suff(67, range(10), lambda x:x%2==1, lambda x:x%3==0, lambda x:x)
    suff(68, it.product(range(1,11), repeat=2), lambda p:sum(p)==10, lambda p:p[0]-p[1]==-2, lambda p:p[0]>p[1])
    suff(69, it.product(range(1,11), repeat=2), lambda p:2*sum(p)==20, lambda p:p[0]-p[1]==2, math.prod)
    suff(70, range(-3,4), lambda x:x in (2,-2), lambda x:x>0, lambda x:x*x)
    suff(71, it.permutations([1,2,3]), lambda p:p[0]==1, lambda p:p[1]==2, lambda p:p[2])
    suff(72, it.product(range(10), repeat=2), lambda p:p[0]==0, lambda p:p[1]==5, lambda p:math.prod(p)==0)
    suff(88, it.product(range(1,10), repeat=2), lambda p:math.prod(p)==12, lambda p:p[0]<p[1], sum)
    suff(89, it.permutations(range(40,81),3), lambda p:p[0]+p[1]==120, lambda p:p[0]+p[2]==140, lambda p:p[0]>p[1])
    suff(90, range(1,31), lambda x:x%4==0, lambda x:x<=10, lambda x:x%6==0)


def verbal():
    # These authored edges record the dependencies identified in editorial review.
    # Their presence is not an automated proof of English grammar or comprehension.
    constraints = json.loads((ROOT / "scripts/verbal_order_constraints.json").read_text(encoding="utf-8"))
    assert len(constraints) == 14
    for qid, edges in constraints.items():
        question = QUESTIONS[qid]
        labels = {line.split(":", 1)[0] for line in question["code_snippet"].splitlines()}
        assert len(labels) in (4, 5)
        assert {label for edge in edges for label in edge} == labels
        def valid(order):
            position = {label:i for i,label in enumerate(order)}
            return all(position[before] < position[after] for before,after in edges)
        solutions = [order for order in it.permutations(labels) if valid(order)]
        assert len(solutions) == 1, (qid, solutions)
        matches = []
        for key, text in question["options"].items():
            order = text.split("-")
            assert set(order) == labels and len(order) == len(labels), (qid, text)
            if valid(order):
                matches.append(key)
        assert matches == [question["correct_answer"]], (qid, matches)
        CHECKED.add(qid)
    print("Checked 14 paragraph-order keys against editorial precedence constraints; grammar and passage answers require editorial review.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subpart", choices=FILES, action="append")
    args = parser.parse_args()
    for sid in args.subpart or FILES:
        path = ROOT / "questions/module_6_aptitude" / FILES[sid]
        QUESTIONS.update({q["id"]: q for q in json.loads(path.read_text(encoding="utf-8"))})
        {"6.1": arithmetic, "6.2": modern, "6.3": logic, "6.4": verbal}[sid]()
    print(f"PASS: {len(CHECKED)} exact/model-checked keys; editorial review remains separate.")


if __name__ == "__main__":
    main()
