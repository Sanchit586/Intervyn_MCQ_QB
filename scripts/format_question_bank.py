"""Format math text, embedded programs, reference tables, and reading passages.

Use --check for a read-only audit. Development dependencies are pinned in
requirements_formatting.txt; ordinary schema/display validation is stdlib-only.
"""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import subprocess
import sys
import textwrap

from question_bank import CATALOG, ROOT, question_path
from question_display import display_text, presentation_content, reference_text, snippet_language


def align_table(code):
    lines = code.splitlines()
    if len(lines) < 2 or not all("|" in line for line in lines):
        return code
    rows = [[cell.strip() for cell in line.split("|")] for line in lines]
    if len({len(row) for row in rows}) != 1:
        return code
    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
    return "\n".join(" | ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip() for row in rows)


def shell_layout(code):
    # A pipeline permits a newline after an unquoted pipe without a backslash.
    output, quote, escaped, pipe_spacing = [], None, False, False
    for index, char in enumerate(code):
        if pipe_spacing:
            if char.isspace():
                continue
            pipe_spacing = False
        if escaped:
            output.append(char)
            escaped = False
        elif char == "\\" and quote != "'":
            output.append(char)
            escaped = True
        elif quote:
            output.append(char)
            if char == quote:
                quote = None
        elif char in ("'", '"'):
            output.append(char)
            quote = char
        elif char == "|" and code[index:index+2] != "||" and (index == 0 or code[index-1] != "|"):
            while output and output[-1] == " ":
                output.pop()
            output.append(" |\n    ")
            pipe_spacing = True
        else:
            output.append(char)
    code = "".join(output)
    # The two longest AWK programs get real block indentation, without changing
    # their tokens, strings, semicolons, or the commands around them.
    replacements = {
        '$2 >= 200 && $2 < 300 {sum[$1] += $3} END {for (key in sum) print key, sum[key]}':
            '\n        $2 >= 200 && $2 < 300 {\n            sum[$1] += $3\n        }\n        END {\n            for (key in sum)\n                print key, sum[key]\n        }\n    ',
        '$1 != previous {if (NR > 1) print previous, sum; previous = $1; sum = 0} {sum += $2} END {print previous, sum}':
            '\n        $1 != previous {\n            if (NR > 1) print previous, sum;\n            previous = $1;\n            sum = 0\n        }\n        {\n            sum += $2\n        }\n        END {\n            print previous, sum\n        }\n    ',
    }
    for before, after in replacements.items():
        code = code.replace("'"+before+"'", "'"+after+"'")
    return code


def reference_layout(question, code):
    code = display_text(reference_text(code))
    # Compact semaphore examples are procedural code, not one-line prose.
    if question["id"] == "1.1.2-003":
        code = code.replace("    while turn ≠ i: pass", "    while turn ≠ i:\n        pass")
    elif question["id"] in ("1.1.2-017", "1.1.2-028"):
        code = code.replace("if reader_count == 1: wait(resource)", "if reader_count == 1:\n        wait(resource)")
        code = code.replace("if reader_count == 0: signal(resource)", "if reader_count == 0:\n        signal(resource)")
        for writer in ("write_data()", "write_shared_data()"):
            code = code.replace(f"Writer: wait(resource); {writer}; signal(resource)",
                                f"Writer:\n    wait(resource);\n    {writer};\n    signal(resource)")
    elif question["id"] == "1.1.2-029":
        for process, action in (("P1", "insert one item"), ("C1", "remove one item")):
            code = code.replace(f"{process}: wait(mutex); {action}; signal(mutex)",
                                f"{process}:\n    wait(mutex);\n    {action};\n    signal(mutex)")
    if question["question"].startswith("Passage "):
        return textwrap.fill(" ".join(code.split()), width=88, break_long_words=False, break_on_hyphens=False)
    return align_table(code)


def format_question(question, clang_format, sql_formatter):
    import black
    result = dict(question)
    for key in ("question", "explanation"):
        result[key] = display_text(question[key])
    result["options"] = {key: display_text(value) for key, value in question["options"].items()}
    code = question["code_snippet"]
    if code:
        language = snippet_language(question)
        if language in ("cpp", "java"):
            formatted = subprocess.run(
                [str(clang_format), f"--assume-filename=snippet.{language}", f"--style=file:{ROOT / '.clang-format'}"],
                input=code, capture_output=True, text=True, encoding="utf-8", timeout=20,
            )
            if formatted.returncode:
                raise ValueError(f"{question['id']}: {formatted.stderr}")
            code = formatted.stdout
        elif language == "python":
            code = black.format_str(code, mode=black.Mode(line_length=88))
        elif language == "sql":
            module = json.dumps(str(sql_formatter.resolve()).replace("\\", "/"))
            script = ('const {format}=require('+module+'); '
                      'process.stdout.write(format(require("fs").readFileSync(0,"utf8"),'
                      '{language:"sqlite",tabWidth:4,expressionWidth:88,keywordCase:"preserve"}));')
            formatted = subprocess.run(["node", "-e", script], input=code, capture_output=True,
                                       text=True, encoding="utf-8", timeout=20)
            if formatted.returncode:
                raise ValueError(f"{question['id']}: {formatted.stderr}")
            code = formatted.stdout
        elif language == "bash":
            code = shell_layout(code)
        elif language == "reference":
            code = reference_layout(question, code)
        result["code_snippet"] = code.rstrip("\r\n")
    if presentation_content(result) != presentation_content(question):
        raise ValueError(f"{question['id']}: formatter changed assessment content or program syntax")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--clang-format", type=Path)
    parser.add_argument("--sql-formatter-module", type=Path,
                        default=ROOT / ".venv/sql-formatter/node_modules/sql-formatter")
    args = parser.parse_args()
    clang = args.clang_format or shutil.which("clang-format") or ROOT / ".venv/Scripts/clang-format.exe"
    paths = [question_path(part) for part in CATALOG["subparts"]]
    changes, pending, fields = [], {}, Counter()
    for path in paths:
        original = json.loads(path.read_text(encoding="utf-8"))
        with ThreadPoolExecutor(max_workers=4) as pool:
            updated = list(pool.map(lambda q: format_question(q, clang, args.sql_formatter_module), original))
        for old, new in zip(original, updated):
            if old != new:
                changes.append(old["id"])
                fields.update(key for key in old if old[key] != new[key])
        if original != updated:
            pending[path] = updated
    if args.check:
        print(f"{'FAIL' if changes else 'PASS'}: {len(changes)} questions need display formatting across {len(pending)} files.")
        if changes:
            print(", ".join(changes[:30]))
        return int(bool(changes))
    # Prepare and verify the whole bank before replacing any JSON file.
    for path, rows in pending.items():
        path.write_text(json.dumps(rows, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"Formatted {len(changes)} questions across {len(pending)} files: {dict(fields)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
