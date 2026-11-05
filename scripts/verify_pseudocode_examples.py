"""Compile the repository's typed pseudocode conventions to Java and check outputs.

Requires a JDK supporting --release 17. No third-party Python packages are used.
The translation preserves Java's defined int arithmetic, evaluation order, loops,
switch fall-through, and recursion. It is not a general pseudocode interpreter.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path

from question_bank import module_question_paths
import re
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def translate(source):
    fields = []
    translated = []
    function = None
    depth = 0
    aliases = {}
    for line in source.splitlines():
        declaration = re.match(r"Function (Integer|Void) (\w+)\(", line)
        if declaration:
            function = declaration.group(2)
            aliases = {}
        static = re.fullmatch(r"\s*Static Integer (\w+) = (-?\d+);", line)
        if static:
            if not function:
                raise ValueError("Static local outside function")
            name, initial = static.groups()
            aliases[name] = f"{function}_{name}"
            fields.append(f"static int {aliases[name]} = {initial};")
            continue
        for name, replacement in aliases.items():
            line = re.sub(rf"\b{re.escape(name)}\b", replacement, line)
        line = re.sub(r"^Global Integer\b", "static int", line)
        line = re.sub(r"^Function Integer\b", "static int", line)
        line = re.sub(r"^Function Void\b", "static void", line)
        line = re.sub(r"^Main \{", "public static void main(String[] args) {", line)
        for before, after in [("Integer", "int"), ("mod", "%"),
                              ("div", "/"), ("and", "&&"),
                              ("or", "||"), ("not", "!")]:
            line = re.sub(rf"\b{before}\b", after, line)
        translated.append(line)
        depth += line.count("{") - line.count("}")
        if depth == 0:
            function = None
            aliases = {}
    return "\n".join([
        "public class Main {",
        "static void Print(int... values) {",
        '    for (int value : values) System.out.print(value + " ");',
        "}", *fields, *translated, "}",
    ])


def check(question, base, java, javac):
    folder = base / question["id"]
    folder.mkdir()
    (folder / "Main.java").write_text(translate(question["code_snippet"]), encoding="utf-8")
    compiled = subprocess.run(
        [str(javac), "--release", "17", "Main.java"], cwd=folder,
        capture_output=True, text=True, timeout=30,
    )
    if compiled.returncode:
        raise ValueError(f'{question["id"]}: compilation failed\n{compiled.stderr}')
    executed = subprocess.run(
        [str(java), "-cp", str(folder), "Main"], cwd=folder,
        capture_output=True, text=True, timeout=10,
    )
    if executed.returncode:
        raise ValueError(f'{question["id"]}: execution failed\n{executed.stderr}')
    actual = " ".join(executed.stdout.split())
    options = question["options"]
    matching = [key for key, value in options.items() if " ".join(value.split()) == actual]
    if matching != [question["correct_answer"]]:
        raise ValueError(f'{question["id"]}: actual={actual!r}; keyed={options[question["correct_answer"]]!r}')
    return question["id"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--java-home", type=Path)
    args = parser.parse_args()
    suffix = ".exe" if os.name == "nt" else ""
    java = args.java_home / "bin" / f"java{suffix}" if args.java_home else shutil.which("java")
    javac = args.java_home / "bin" / f"javac{suffix}" if args.java_home else shutil.which("javac")
    if not java or not javac:
        parser.error("A JDK is required; select one with --java-home")
    paths = args.paths or module_question_paths(3)
    questions = [q for path in paths for q in json.loads(path.read_text(encoding="utf-8"))]
    base = Path(tempfile.mkdtemp(prefix=".pseudocode_verify_", dir=ROOT)).resolve()
    try:
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda q: check(q, base, java, javac), questions))
        print(f"PASS: {len(results)} pseudocode outputs compiled and executed; exactly one matching option each.")
    finally:
        if base.parent != ROOT.resolve() or not base.name.startswith(".pseudocode_verify_"):
            raise RuntimeError("Unsafe temporary cleanup path")
        for attempt in range(20):
            try:
                shutil.rmtree(base)
                break
            except PermissionError:
                if attempt == 19:
                    raise
                time.sleep(0.25)


if __name__ == "__main__":
    main()
