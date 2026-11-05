"""Run explicit Python output questions and compile self-contained C++17 examples."""

import argparse
import ast
import json
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from question_bank import module_question_paths

from verify_oop_examples import verify as verify_compiled


ROOT = Path(__file__).resolve().parents[1]


def check(question, folder, compiler):
    code = question["code_snippet"]
    if code and code.lstrip().startswith("#include"):
        return verify_compiled(question, folder, compiler, "", "")
    if code and question["question"].startswith("Python 3."):
        ast.parse(code)
        result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=20)
        expected = question["options"][question["correct_answer"]]
        assert result.returncode == 0 and " ".join(result.stdout.split()) == " ".join(expected.split()), (question["id"], expected, result.stdout, result.stderr)
        return "executed Python output"
    if code and question["question"].startswith("Python 3 (analysis)"):
        ast.parse(code)
        return "Python syntax checked; analysis reviewed separately"
    return "analytical/trace question reviewed separately"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--cxx", default="g++")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    paths = args.paths or module_question_paths(2)
    assert paths, "No DSA question files found"
    questions = [q for path in paths for q in json.loads(path.read_text(encoding="utf-8"))]
    assert len({q["id"] for q in questions}) == len(questions), "Duplicate question IDs"
    compiler = shutil.which(args.cxx) or args.cxx
    folder = Path(tempfile.mkdtemp(prefix=".dsa_verify_", dir=ROOT)).resolve()
    assert folder.parent == ROOT.resolve() and folder.name.startswith(".dsa_verify_"), folder
    try:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            results = list(pool.map(lambda q: check(q, folder, compiler), questions))
        print(f"Checked {len(questions)} questions: {dict(Counter(results))}")
    finally:
        for attempt in range(20):
            assert folder.parent == ROOT.resolve() and folder.name.startswith(".dsa_verify_"), folder
            try:
                shutil.rmtree(folder)
                break
            except PermissionError:
                if attempt == 19:
                    raise
                time.sleep(0.25)


if __name__ == "__main__":
    main()
