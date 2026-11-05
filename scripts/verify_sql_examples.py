"""Execute the 35 self-contained SQLite output questions and check every option."""

import json
import sqlite3

from question_bank import reference_questions


def main():
    questions = reference_questions("1.2.4")
    for question in questions.values():
        with sqlite3.connect(":memory:") as connection:
            result = [list(row) for row in connection.execute(question["code_snippet"]).fetchall()]
        matching = [key for key, value in question["options"].items() if json.loads(value) == result]
        assert matching == [question["correct_answer"]], (question["id"], result, matching)
    print(f"PASS: {len(questions)} SQLite outputs; exactly one matching option each (SQLite {sqlite3.sqlite_version}).")


if __name__ == "__main__":
    main()
