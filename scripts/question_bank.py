"""Catalog access and original-source references for the reorganized bank."""

from collections import Counter
from functools import lru_cache
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "question_bank_catalog.json").read_text(encoding="utf-8"))


def module_parts(module_id):
    return [part for part in CATALOG["subparts"] if part["module_id"] == str(module_id)]


def question_path(part):
    return ROOT / part["path"]


def module_question_paths(module_id):
    return [question_path(part) for part in module_parts(module_id)]


@lru_cache(None)
def read_questions(relative_path):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def reference_questions(original_subpart_id):
    """Map original test-fixture IDs to the actual, currently numbered objects.

    Historical IDs are aliases only in verifier memory, never extra question
    fields or duplicate files. Ranges in the catalog identify their source.
    """
    for part in CATALOG["subparts"]:
        for source in part["sources"]:
            if source["id"] == original_subpart_id:
                start = source["start"] - 1
                rows = read_questions(part["path"])[start:start+source["count"]]
                if len(rows) != source["count"]:
                    raise ValueError(f"Incomplete source range for {original_subpart_id}")
                return {f"{original_subpart_id}-{i:03}": q for i, q in enumerate(rows, 1)}
    raise ValueError(f"Unknown original source {original_subpart_id}")


def validate_catalog():
    """Check numbering, canonical paths, quotas, and complete source partitions."""
    if CATALOG["schema_version"] != 2:
        raise ValueError("Expected question catalog schema version 2")
    modules = CATALOG["modules"]
    if [m["id"] for m in modules] != [str(i) for i in range(1, len(modules)+1)]:
        raise ValueError("Module IDs must be consecutive starting at 1")
    ids, paths, source_ids = set(), set(), set()
    for module in modules:
        mid = module["id"]
        if not module["directory"].startswith(f"module_{mid}_"):
            raise ValueError(f"Invalid module directory for {mid}")
        parts = module_parts(mid)
        groups = module.get("groups", [])
        if groups:
            if [g["id"] for g in groups] != [f"{mid}.{i}" for i in range(1, len(groups)+1)]:
                raise ValueError(f"Nonconsecutive parent groups in module {mid}")
            for group in groups:
                children = [p for p in parts if p["id"].startswith(group["id"]+".")]
                if not children or [p["id"] for p in children] != [f"{group['id']}.{i}" for i in range(1, len(children)+1)]:
                    raise ValueError(f"Nonconsecutive topics under {group['id']}")
        elif [p["id"] for p in parts] != [f"{mid}.{i}" for i in range(1, len(parts)+1)]:
            raise ValueError(f"Nonconsecutive groups in module {mid}")
        for part in parts:
            pid = part["id"]
            path = question_path(part).resolve()
            if pid in ids or path in paths:
                raise ValueError(f"Duplicate catalog ID/path: {pid}")
            ids.add(pid)
            paths.add(path)
            expected_parent = ROOT / "questions" / module["directory"]
            if groups:
                group = next(g for g in groups if pid.startswith(g["id"]+"."))
                if not group["directory"].startswith(group["id"]+"_"):
                    raise ValueError(f"Invalid parent group directory for {pid}")
                expected_parent /= group["directory"]
            if path.parent != expected_parent.resolve() or not path.name.startswith(pid+"_"):
                raise ValueError(f"Incorrect canonical question path for {pid}")
            count = part["count"]
            if type(count) is not int or count <= 0:
                raise ValueError(f"Invalid question count for {pid}")
            if set(part["difficulties"]) != {"Easy", "Medium", "Hard"} or sum(part["difficulties"].values()) != count:
                raise ValueError(f"Invalid difficulty quota for {pid}")
            cursor, combined = 1, Counter()
            for source in part["sources"]:
                if source["id"] in source_ids or not source["id"].startswith(mid+"."):
                    raise ValueError(f"Duplicate or mismatched source {source['id']}")
                source_ids.add(source["id"])
                if source["start"] != cursor or source["count"] <= 0:
                    raise ValueError(f"Noncontiguous source ranges in {pid}")
                if sum(source["difficulties"].values()) != source["count"]:
                    raise ValueError(f"Invalid source quota in {pid}")
                cursor += source["count"]
                combined.update(source["difficulties"])
            if cursor != count+1 or combined != Counter(part["difficulties"]):
                raise ValueError(f"Source ranges/quotas do not cover {pid}")
    if len(ids) != len(CATALOG["subparts"]):
        raise ValueError("Catalog contains a subpart with an unknown module")
