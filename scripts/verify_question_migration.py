"""Audit this reorganization against its recorded original Git revision.

This migration-specific check compares every question's assessment content and
source order; the schema validator separately checks the current metadata.
"""

import argparse
import json
import subprocess

from question_bank import CATALOG, ROOT, question_path, validate_catalog


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default=CATALOG["migration"]["from_commit"])
    args = parser.parse_args()
    validate_catalog()
    metadata = {"id", "module", "subpart_id", "subpart_name"}
    count, sources = 0, 0
    for part in CATALOG["subparts"]:
        current = json.loads(question_path(part).read_text(encoding="utf-8"))
        assert len(current) == part["count"], part["id"]
        for source in part["sources"]:
            blob = subprocess.check_output(
                ["git", "show", f"{args.base}:{source['original_path']}"], cwd=ROOT,
            )
            original = json.loads(blob.decode("utf-8"))
            start = source["start"] - 1
            selected = current[start:start+source["count"]]
            assert len(original) == len(selected) == source["count"], source["id"]
            for old, new in zip(original, selected):
                old_content = {k:v for k,v in old.items() if k not in metadata}
                new_content = {k:v for k,v in new.items() if k not in metadata}
                assert old_content == new_content, (old["id"], new["id"], "Assessment content changed")
                count += 1
            sources += 1
    actual = {p.resolve() for p in (ROOT / "questions").rglob("*.json")}
    expected = {question_path(p).resolve() for p in CATALOG["subparts"]}
    assert actual == expected, ("Missing/unexpected files", actual ^ expected)
    print(f"PASS: all {count} questions retain their assessment content and source order; {sources} original files map to {len(expected)} current files.")


if __name__ == "__main__":
    main()
