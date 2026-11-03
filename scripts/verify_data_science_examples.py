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
FILES = {"5.1": "5.1_statistics_probability.json", "5.2": "5.2_distributions_tests.json",
         "5.3": "5.3_supervised_ml.json", "5.4": "5.4_evaluation_regularization.json"}
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


def testing():
    sid = "5.2"
    calculations = {
        2: (130-100)/15, 8: 1-.2, 13: 12/math.sqrt(36),
        14: (103-100)/(12/math.sqrt(36)), 15: (52-50)/(4/math.sqrt(16)),
        20: 40*30/100, 21: (18-12)**2/12, 22: (3-1)*(4-1),
        24: 12/3, 25: .8413-.1587, 26: 1-.9750,
        27: 2*(1-.97725), 28: 1-.0668,
        35: 1-.95**2, 36: F(90*5, 90*5+10*80),
        37: (sum(5*(mean-4)**2 for mean in [2, 4, 6])/2)/(24/12),
    }
    for index, value in calculations.items():
        numeric(sid, index, value)
    exact(sid, 1, "0, 1")
    exact(sid, 23, f"{4-1}, {20-4}")
    exact(sid, 31, f"Multiply sample size by {int((1/.5)**2)}")
    covariance_sum = sum(100 if i == j else 20 if i//10 == j//10 else 0
                         for i in range(100) for j in range(100))
    numeric(sid, 34, math.sqrt(covariance_sum/100**2))
    observed = [[30, 10], [10, 50]]
    rows = [sum(row) for row in observed]
    columns = [sum(row[j] for row in observed) for j in range(2)]
    chi = sum((observed[i][j]-rows[i]*columns[j]/100)**2/(rows[i]*columns[j]/100)
              for i in range(2) for j in range(2))
    assert chi > 3.841
    exact(sid, 38, f"{chi:.4f}; reject independence")
    cutoff = 50+1.645*10/math.sqrt(100)
    z_under_alternative = (cutoff-52)/(10/math.sqrt(100))
    assert math.isclose(z_under_alternative, -.355)
    assert abs(stats.NormalDist().cdf(z_under_alternative)-.3613) < .00005
    exact(sid, 39, f"{.3613:.4f}, {1-.3613:.4f}")
    assert math.isclose(.999**100, .9047921471, abs_tol=1e-10)
    exact(sid, 40, "No; np=0.1 and P(all zeros)=0.999^100 is about 0.905, so the finite-sample distribution is highly asymmetric")


def supervised():
    import numpy as np
    sid = "5.3"
    entropy = -sum(p*math.log2(p) for p in [.75, .25])
    child_gini = F(6, 10)*(1-F(4, 6)**2-F(2, 6)**2)+F(4, 10)*(1-F(1, 4)**2-F(3, 4)**2)
    corr = np.array([[1, .6, .6], [.6, 1, 0], [.6, 0, 1]])
    bootstraps = list(it.product(range(4), repeat=4))
    calculations = {
        4: 1/(1-.8), 5: 1/(1+math.exp(0)), 8: -1*math.log2(1),
        9: 1-.5**2-.5**2, 16: float(f"{1/(1-.9**2):.4f}"),
        17: math.sqrt(9), 18: 1/(1+math.exp(-math.log(3))),
        20: 1/(1+math.exp(-(math.log(3)+2*math.log(2)))),
        22: float(f"{entropy:.4f}"), 23: F(1, 2)-child_gini,
        24: float(f"{1-entropy:.4f}"), 26: stats.mean([1, 2, 6]),
        27: F(sum(0 not in draw for draw in bootstraps), len(bootstraps)),
        28: stats.mean([.9, .6]), 30: 2+.1*5,
        32: float(f"{-math.log(.8):.4f}"), 34: np.linalg.inv(corr)[0, 0],
        40: .5*(16/2+4/2-4/4)-1,
    }
    for index, value in calculations.items():
        numeric(sid, index, value)
    x = np.column_stack([np.ones(3), [0, 1, 2]])
    coef = np.linalg.lstsq(x, [1, 3, 5], rcond=None)[0]
    exact(sid, 13, f"{coef[0]:.0f}, {coef[1]:.0f}")
    y = np.array([1, 4, 4])
    residual = y-x@np.linalg.lstsq(x, y, rcond=None)[0]
    numeric(sid, 14, residual.sum(), tolerance=1e-9)
    assert math.isclose((math.log(.75/.25)+math.log(3))/math.log(3), 2)
    exact(sid, 21, "x>=2")
    gini_parent = 1-.5**2-.5**2
    gini_a = 0
    gini_b = 1-.75**2-.25**2
    assert gini_parent-gini_a > gini_parent-gini_b
    exact(sid, 25, f"Split A, {gini_parent-gini_a:g}")
    targets = np.array([3, 5])
    predictions = np.array([2, 2])
    exact(sid, 29, str((targets-predictions).tolist()))
    residuals = np.array([0, 4])-np.array([1, 1])
    exact(sid, 31, str((np.array([1, 1])+int(residuals.mean())).tolist()))
    duplicate = np.column_stack([[1, 2, 3], [1, 2, 3]])
    assert np.linalg.matrix_rank(duplicate) == 1
    assert np.allclose(duplicate@[1, 2], duplicate@[2, 1])
    exact(sid, 35, "Every pair satisfying beta1+beta2=3 is optimal; coefficients are nonunique but fitted values are unique")
    loss = lambda w: math.log1p(math.exp(-2*w))
    h = 1e-4
    gradient = (loss(h)-loss(-h))/(2*h)
    curvature = (loss(h)-2*loss(0)+loss(-h))/h**2
    assert abs(gradient+1) < 1e-6 and abs(curvature-1) < 1e-6
    exact(sid, 36, "-1, 1")
    cov = np.full((10, 10), 1.0)
    np.fill_diagonal(cov, 4)
    exact(sid, 38, f"{cov.sum()/100:g}, {4*.25:g}")
    q = lambda w: -6*w+.5*(2+1)*w*w
    candidates = np.linspace(-3, 5, 8001)
    best = float(candidates[np.argmin(q(candidates))])
    exact(sid, 39, f"{best:g}, {q(0)-q(best):g}")


def evaluation():
    import numpy as np
    sid = "5.4"
    def auc(positive, negative):
        comparisons = [float(p > n)+.5*float(p == n) for p in positive for n in negative]
        return stats.mean(comparisons)
    calculations = {
        4: (45+45)/(45+45+5+5), 7: F(1, 2),
        11: F(8, 8+9), 13: F(2*30, 2*30+10+20),
        15: auc([.9, .6], [.8, .1]), 17: 1-150/100,
        18: 1-(1-F(4, 5))*F(20, 18),
        25: auc([.8, .5], [.5, .2]),
    }
    for index, value in calculations.items():
        numeric(sid, index, value)
    exact(sid, 10, f"{F(40, 50)}, {F(40, 60)}")
    exact(sid, 12, f"{90/100:g}, {30/50:g}")
    exact(sid, 14, f"{990/1000:g}, {0/10:g}")
    grid = np.linspace(-5, 8, 13001)
    numeric(sid, 23, grid[np.argmin((6-grid)**2+2*grid**2)])
    numeric(sid, 24, grid[np.argmin(.5*(grid-3)**2+np.abs(grid))])
    old_adjusted = 1-F(90, 17)/F(190, 19)
    new_adjusted = 1-F(86, 16)/F(190, 19)
    assert 1-F(86, 190) > 1-F(90, 190) and old_adjusted > new_adjusted
    exact(sid, 26, f"R^2 increases; adjusted R^2 decreases from {old_adjusted} to {new_adjusted}")
    z = np.array([3, -.5, 2])
    lasso = np.sign(z)*np.maximum(np.abs(z)-1, 0)
    ridge = np.linalg.solve(2*np.eye(3), z)
    vector = lambda a: "["+",".join(f"{0 if v == 0 else v:g}" for v in a)+"]"
    exact(sid, 27, f"Lasso: {vector(lasso)}; ridge: {vector(ridge)}")
    # Independently compare the claimed lasso coordinate solution to a fine grid.
    for target, coefficient in zip(z, lasso):
        losses = .5*(grid-target)**2+np.abs(grid)
        assert abs(grid[np.argmin(losses)]-coefficient) < 1e-8
    beta = np.linalg.solve(np.array([[2, 1], [1, 2]])+np.eye(2), [3, 0])
    exact(sid, 28, "["+", ".join(str(F(float(v)).limit_denominator(1000)) for v in beta)+"]")
    lambdas = np.linspace(0, 3, 30001)
    # Evaluate the exact two-point noise law epsilon in {-1,+1} with probability 1/2.
    risk = .5*((1/(1+lambdas)-2)**2+(3/(1+lambdas)-2)**2)
    optimum = int(np.argmin(risk))
    exact(sid, 29, f"lambda={F(float(lambdas[optimum])).limit_denominator(1000)}; risk={F(float(risk[optimum])).limit_denominator(1000)}")
    ridge_pair = np.linalg.solve([[2, 1], [1, 2]], [3, 3])
    assert np.allclose(ridge_pair, [1, 1])
    lasso_objective = lambda a, b: (3-a-b)**2+2*(abs(a)+abs(b))
    for a in np.linspace(0, 2, 21):
        assert math.isclose(lasso_objective(a, 2-a), 5)
    assert min(lasso_objective(a, b) for a in np.linspace(-1, 3, 41)
               for b in np.linspace(-1, 3, 41)) >= 5-1e-12
    exact(sid, 30, "Ridge uniquely gives (1,1); lasso permits every nonnegative pair with sum 2")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subpart", choices=FILES, action="append")
    args = parser.parse_args()
    for sid in args.subpart or FILES:
        path = ROOT / "questions/module_5_data_science" / FILES[sid]
        QUESTIONS.update({q["id"]: q for q in json.loads(path.read_text(encoding="utf-8"))})
        {"5.1": foundations, "5.2": testing, "5.3": supervised, "5.4": evaluation}[sid]()
    print(f"PASS: {len(CHECKED)} numerical/enumerated answer keys; conceptual answers need separate review.")


if __name__ == "__main__":
    main()
