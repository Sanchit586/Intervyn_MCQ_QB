"""Run self-contained Bash output questions in fresh disposable directories.

Requires Bash and GNU utilities. Linux permission answers are checked by bit
arithmetic, not by pretending Windows/MSYS file ACLs implement Linux access rules.
Filesystem hierarchy and access-control concepts need separate content review.
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

from question_bank import reference_questions

ROOT = Path(__file__).resolve().parents[1]


def verify(bash, base):
    questions = list(reference_questions("4.3").values())
    env = {**os.environ, "LC_ALL": "C", "PATH": str(bash.parent) + os.pathsep + os.environ["PATH"]}
    # Do not load user initialization code or allow inherited tracing options.
    for name in ("BASH_ENV", "ENV", "SHELLOPTS", "BASHOPTS"):
        env.pop(name, None)
    checked = 0
    for question in questions:
        if not question["question"].startswith("Bash with GNU utilities"):
            continue
        folder = base / question["id"]
        folder.mkdir()
        result = subprocess.run([str(bash), "--noprofile", "--norc", "-c", question["code_snippet"]],
                                cwd=folder, env=env, capture_output=True, text=True, timeout=20)
        if result.returncode or result.stderr:
            raise ValueError(f'{question["id"]}: {result.returncode}: {result.stderr[:1000]}')
        actual = result.stdout.rstrip("\n")
        matches = [key for key, value in question["options"].items() if value == actual]
        if matches != [question["correct_answer"]]:
            raise ValueError(f'{question["id"]}: actual={actual!r}; expected={question["options"][question["correct_answer"]]!r}')
        checked += 1
    expected = {
        "4.3-004": "rw-r-----",
        "4.3-009": f"{((0o750 & ~0o100) | 0o020):03o}",
        "4.3-010": f"File {(0o666 & ~0o027):04o}; directory {(0o777 & ~0o027):04o}",
    }
    file_mode = 0o666 & ~0o077
    owner = (file_mode >> 6) & 7
    file_mode = (file_mode & ~0o070) | (owner << 3)
    file_mode = (file_mode & ~0o127) | 0o004
    expected["4.3-025"] = f"f is {file_mode:04o}; d is {(0o777 & ~0o027):04o}"
    for question in questions:
        if question["id"] in expected:
            assert question["options"][question["correct_answer"]] == expected[question["id"]], question["id"]
    print(f"PASS: {checked} exact shell outputs and {len(expected)} permission answer keys.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bash", type=Path)
    args = parser.parse_args()
    selected = args.bash or shutil.which("bash")
    if not selected:
        parser.error("Bash is required; select it with --bash")
    bash = Path(selected).resolve()
    base = Path(tempfile.mkdtemp(prefix=".systems_verify_", dir=ROOT)).resolve()
    try:
        verify(bash, base)
    finally:
        if base.parent != ROOT.resolve() or not base.name.startswith(".systems_verify_"):
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
