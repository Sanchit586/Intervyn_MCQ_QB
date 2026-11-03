"""Validate question files using only the Python standard library."""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIELDS = {
    "id", "module", "subpart_id", "subpart_name", "difficulty", "question",
    "code_snippet", "options", "correct_answer", "explanation",
}
TEXT_FIELDS = FIELDS - {"code_snippet", "options"}
LETTERS = {"A", "B", "C", "D"}
DIFFICULTIES = {"Easy", "Medium", "Hard"}
# Add exact quotas here when another subpart is populated.
SUBPARTS = {
    "3.2": {
        "module": "Module 3: Pseudocode, Bitwise & Code Tracing",
        "name": "Iterative Loop Execution & Flow Control",
        "count": 50,
        "difficulties": {"Easy": 15, "Medium": 25, "Hard": 10},
    },
    "3.1": {
        "module": "Module 3: Pseudocode, Bitwise & Code Tracing",
        "name": "Bitwise Operations & Number Manipulation",
        "count": 50,
        "difficulties": {"Easy": 15, "Medium": 25, "Hard": 10},
    },
    "1.1.1": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "CPU Scheduling & Process Lifecycle",
        "count": 30,
        "difficulties": {"Easy": 9, "Medium": 15, "Hard": 6},
    },
    "1.1.2": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "Concurrency, Synchronization & Deadlocks",
        "count": 30,
        "difficulties": {"Easy": 9, "Medium": 15, "Hard": 6},
    },
    "1.1.3": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "Memory Management & Virtual Memory",
        "count": 30,
        "difficulties": {"Easy": 9, "Medium": 15, "Hard": 6},
    },
    "1.1.4": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "Storage Systems, File Systems & Disk Scheduling",
        "count": 20,
        "difficulties": {"Easy": 6, "Medium": 10, "Hard": 4},
    },
    "1.2.1": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "Relational Schema Design & Normalization",
        "count": 30,
        "difficulties": {"Easy": 9, "Medium": 15, "Hard": 6},
    },
    "1.2.2": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "Transactions, Concurrency & Recovery",
        "count": 30,
        "difficulties": {"Easy": 9, "Medium": 15, "Hard": 6},
    },
    "1.2.3": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "Storage, Indexing & ER Modeling",
        "count": 25,
        "difficulties": {"Easy": 8, "Medium": 12, "Hard": 5},
    },
    "1.2.4": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "SQL Queries & Output Prediction",
        "count": 35,
        "difficulties": {"Easy": 10, "Medium": 18, "Hard": 7},
    },
    "1.3.1": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "Network Architecture & Physical/Data Link Layers",
        "count": 25,
        "difficulties": {"Easy": 8, "Medium": 12, "Hard": 5},
    },
    "1.3.2": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "Network Layer, IP Addressing & Routing",
        "count": 25,
        "difficulties": {"Easy": 7, "Medium": 13, "Hard": 5},
    },
    "1.3.3": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "Transport Layer Protocols",
        "count": 25,
        "difficulties": {"Easy": 8, "Medium": 12, "Hard": 5},
    },
    "1.3.4": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "Application Layer Protocols & Network Security",
        "count": 25,
        "difficulties": {"Easy": 7, "Medium": 13, "Hard": 5},
    },
    "1.4.1": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "Core Architecture & Class Mechanics",
        "count": 30,
        "difficulties": {"Easy": 9, "Medium": 15, "Hard": 6},
    },
    "1.4.2": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "Object Lifecycle & Memory Management",
        "count": 30,
        "difficulties": {"Easy": 9, "Medium": 15, "Hard": 6},
    },
    "1.4.3": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "Runtime Polymorphism & Dynamic Dispatch",
        "count": 30,
        "difficulties": {"Easy": 9, "Medium": 15, "Hard": 6},
    },
    "1.4.4": {
        "module": "Module 1: Core Computer Science Fundamentals",
        "name": "Language-Specific OOP Outputs & Exception Handling",
        "count": 30,
        "difficulties": {"Easy": 9, "Medium": 15, "Hard": 6},
    },
    "2.1": {
        "module": "Module 2: Data Structures & Algorithms",
        "name": "Asymptotic Complexity & Recurrence Analysis",
        "count": 35,
        "difficulties": {"Easy": 11, "Medium": 17, "Hard": 7},
    },
    "2.2": {
        "module": "Module 2: Data Structures & Algorithms",
        "name": "Linear Data Structures (Arrays, Strings & Linked Lists)",
        "count": 45,
        "difficulties": {"Easy": 13, "Medium": 23, "Hard": 9},
    },
    "2.3": {
        "module": "Module 2: Data Structures & Algorithms",
        "name": "Stacks & Queues",
        "count": 40,
        "difficulties": {"Easy": 12, "Medium": 20, "Hard": 8},
    },
    "2.4": {
        "module": "Module 2: Data Structures & Algorithms",
        "name": "Trees & Binary Search Trees",
        "count": 60,
        "difficulties": {"Easy": 18, "Medium": 30, "Hard": 12},
    },
    "2.5": {
        "module": "Module 2: Data Structures & Algorithms",
        "name": "Priority Queues (Heaps) & Hashing",
        "count": 45,
        "difficulties": {"Easy": 14, "Medium": 22, "Hard": 9},
    },
    "2.6": {
        "module": "Module 2: Data Structures & Algorithms",
        "name": "Graph Algorithms & Representations",
        "count": 45,
        "difficulties": {"Easy": 13, "Medium": 23, "Hard": 9},
    },
    "2.7": {
        "module": "Module 2: Data Structures & Algorithms",
        "name": "Searching, Sorting & Algorithmic Paradigms",
        "count": 40,
        "difficulties": {"Easy": 12, "Medium": 20, "Hard": 8},
    },
}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"invalid JSON constant: {value}")


def normalized(value):
    return " ".join(value.split()).casefold()


def validate_file(path, seen_ids, seen_questions):
    errors = []

    def fail(message):
        errors.append(f"{path}: {message}")

    try:
        data = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except (OSError, UnicodeError, ValueError) as exc:
        fail(str(exc))
        return errors, 0
    if not isinstance(data, list) or not data:
        fail("expected a nonempty JSON array")
        return errors, 0

    subpart = path.stem.split("_", 1)[0]
    if not re.fullmatch(r"\d+(?:\.\d+)+", subpart):
        fail("filename must begin with a numeric subpart ID followed by '_' ")
    module_match = re.match(r"module_(\d+)_", path.parent.name)
    if not module_match or module_match[1] != subpart.split(".")[0]:
        fail("parent directory must be module_<number>_<name> matching the subpart")
    quota = SUBPARTS.get(subpart)
    counts = Counter()

    for index, entry in enumerate(data, 1):
        label = f"entry {index}"
        if not isinstance(entry, dict):
            fail(f"{label}: expected an object")
            continue
        missing = FIELDS - entry.keys()
        extra = entry.keys() - FIELDS
        if missing:
            fail(f"{label}: missing fields {sorted(missing)}")
        if extra:
            fail(f"{label}: unknown fields {sorted(extra)}")
        for field in sorted(TEXT_FIELDS):
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip():
                fail(f"{label}: {field} must be a nonempty string")

        question_id = entry.get("id")
        if isinstance(question_id, str):
            if not re.fullmatch(re.escape(subpart) + r"-\d{3}", question_id):
                fail(f"{label}: id must use {subpart}-NNN format")
            if question_id in seen_ids:
                fail(f"{label}: duplicate id {question_id!r}; first at {seen_ids[question_id]}")
            else:
                seen_ids[question_id] = f"{path}, entry {index}"
        if entry.get("subpart_id") != subpart:
            fail(f"{label}: subpart_id must match filename prefix {subpart!r}")
        if quota:
            if entry.get("module") != quota["module"]:
                fail(f"{label}: unexpected module name")
            if entry.get("subpart_name") != quota["name"]:
                fail(f"{label}: unexpected subpart_name")

        difficulty = entry.get("difficulty")
        if not isinstance(difficulty, str) or difficulty not in DIFFICULTIES:
            fail(f"{label}: difficulty must be Easy, Medium, or Hard")
        else:
            counts[difficulty] += 1
        snippet = entry.get("code_snippet")
        if snippet is not None and (not isinstance(snippet, str) or not snippet.strip()):
            fail(f"{label}: code_snippet must be null or a nonempty string")
        options = entry.get("options")
        if not isinstance(options, dict) or set(options) != LETTERS:
            fail(f"{label}: options must be an object with exactly A, B, C, D")
        else:
            values = list(options.values())
            if any(not isinstance(value, str) or not value.strip() for value in values):
                fail(f"{label}: option text must be a nonempty string")
            elif len({normalized(value) for value in values}) != 4:
                fail(f"{label}: option text must be distinct")
        answer = entry.get("correct_answer")
        if not isinstance(answer, str) or answer not in LETTERS:
            fail(f"{label}: correct_answer must be one of A, B, C, D")

        question = entry.get("question")
        if isinstance(question, str) and (snippet is None or isinstance(snippet, str)):
            fingerprint = (normalized(question), normalized(snippet or ""))
            if fingerprint in seen_questions:
                fail(f"{label}: duplicate question; first at {seen_questions[fingerprint]}")
            else:
                seen_questions[fingerprint] = f"{path}, entry {index}"

    if quota:
        if len(data) != quota["count"]:
            fail(f"expected {quota['count']} questions, found {len(data)}")
        if counts != Counter(quota["difficulties"]):
            fail(f"expected difficulty counts {quota['difficulties']}, found {dict(counts)}")
    return errors, len(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="JSON files or directories (default: questions/)")
    args = parser.parse_args()
    files = set()
    errors = []
    for path in args.paths or [ROOT / "questions"]:
        if path.is_dir():
            files.update(path.rglob("*.json"))
        elif path.is_file() and path.suffix == ".json":
            files.add(path)
        else:
            errors.append(f"{path}: expected an existing JSON file or directory")
    if not files:
        errors.append("no question JSON files found")
    seen_ids, seen_questions = {}, {}
    total = 0
    for path in sorted({path.resolve() for path in files}):
        file_errors, count = validate_file(path, seen_ids, seen_questions)
        errors.extend(file_errors)
        total += count
    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {total} questions across {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
