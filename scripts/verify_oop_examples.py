"""Compile self-contained OOP snippets and check their keyed output or rejection."""

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from question_bank import module_question_paths


ROOT = Path(__file__).resolve().parents[1]


def run(command):
    return subprocess.run(command, capture_output=True, text=True, timeout=30)


def verify(question, folder, cxx, java, javac):
    code = question["code_snippet"]
    if code is None:
        return "conceptual"
    expected = question["options"][question["correct_answer"]]
    directory = folder / question["id"]
    directory.mkdir()
    if code.lstrip().startswith("#include"):
        source = directory / "main.cpp"
        source.write_text(code, encoding="utf-8")
        executable = directory / ("program.exe" if os.name == "nt" else "program")
        compilation = run([cxx, "-std=c++17", "-pedantic-errors", "-Wall", "-Wextra", "-O0", str(source), "-o", str(executable)])
        execution = [str(executable)]
    elif code.lstrip().startswith("public class Main"):
        source = directory / "Main.java"
        source.write_text(code, encoding="utf-8")
        compilation = run([javac, "--release", "17", "-encoding", "UTF-8", "-d", str(directory), str(source)])
        execution = [java, "-cp", str(directory), "Main"]
    else:
        raise AssertionError(f"{question['id']}: unsupported snippet format")
    if expected == "Compilation error":
        assert compilation.returncode != 0 and "error" in compilation.stderr.lower(), (question["id"], compilation.stdout, compilation.stderr)
        return "compile rejection"
    assert compilation.returncode == 0, (question["id"], compilation.stderr)
    if expected.startswith("Undefined behavior"):
        return "UB classified; not executed"
    result = run(execution)
    actual = " ".join(result.stdout.split())
    assert result.returncode == 0 and actual == " ".join(expected.split()), (question["id"], expected, actual, result.stderr)
    return "executed output"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--cxx", default="g++")
    parser.add_argument("--java-home", type=Path)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    paths = args.paths or [path for path in module_question_paths(1) if path.name.startswith("1.4.")]
    assert paths, "No OOP question files found"
    questions = [question for path in paths for question in json.loads(path.read_text(encoding="utf-8"))]
    assert len({q["id"] for q in questions}) == len(questions), "Duplicate question IDs"
    cxx = shutil.which(args.cxx) or args.cxx
    suffix = ".exe" if os.name == "nt" else ""
    java = str(args.java_home / f"bin/java{suffix}") if args.java_home else shutil.which("java") or "java"
    javac = str(args.java_home / f"bin/javac{suffix}") if args.java_home else shutil.which("javac") or "javac"
    folder = Path(tempfile.mkdtemp(prefix=".oop_verify_", dir=ROOT)).resolve()
    assert folder.parent == ROOT.resolve() and folder.name.startswith(".oop_verify_"), folder
    try:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            results = list(pool.map(lambda q: verify(q, folder, cxx, java, javac), questions))
        print(f"Checked {len(questions)} questions: {dict(Counter(results))}")
    finally:
        # Windows scanners can briefly retain a handle after a program exits.
        for attempt in range(20):
            assert folder.parent == ROOT.resolve() and folder.name.startswith(".oop_verify_"), folder
            try:
                shutil.rmtree(folder)
                break
            except PermissionError:
                if attempt == 19:
                    raise
                time.sleep(0.25)


if __name__ == "__main__":
    main()
