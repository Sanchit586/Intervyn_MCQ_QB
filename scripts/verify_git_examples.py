"""Exercise the Git questions in disposable local repositories, without remotes.

No command changes the question-bank repository or the user's global Git config.
Conceptual SDLC and Scrum answers require separate source/content review.
"""

import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import time

from question_bank import reference_questions

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = reference_questions("4.2")

ENV = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
       "GIT_EDITOR": "true", "GIT_SEQUENCE_EDITOR": "true", "GIT_TERMINAL_PROMPT": "0"}


class Repository:
    def __init__(self, base, name):
        self.path = base / name
        self.path.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Assessment Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "core.autocrlf", "false")
        self.git("config", "commit.gpgSign", "false")
        self.a = self.commit("A", {"base.txt": "root", "f.txt": "base"})

    def git(self, *args, ok=True):
        result = subprocess.run(["git", *args], cwd=self.path, env=ENV,
                                capture_output=True, text=True, timeout=30)
        if ok and result.returncode:
            raise RuntimeError(f"{self.path.name}: git {args}: {result.stderr}")
        if not ok and not result.returncode:
            raise AssertionError(f"Expected rejection: git {args}")
        return result.stdout.strip()

    def write(self, name, value):
        (self.path / name).write_text(value + "\n", encoding="utf-8")

    def read(self, name):
        return (self.path / name).read_text(encoding="utf-8").strip()

    def commit(self, label, changes):
        for name, value in changes.items():
            self.write(name, value)
        self.git("add", "--", *changes)
        self.git("commit", "-m", label)
        return self.git("rev-parse", "HEAD")

    def parents(self):
        return self.git("show", "-s", "--format=%P", "HEAD").split()

    def ancestor(self, older):
        result = subprocess.run(["git", "merge-base", "--is-ancestor", older, "HEAD"],
                                cwd=self.path, env=ENV, capture_output=True, timeout=30)
        assert result.returncode in (0, 1)
        return result.returncode == 0


def keyed(number, text):
    q = QUESTIONS[f"4.2-{number:03}"]
    assert q["options"][q["correct_answer"]] == text, q["id"]


def diverge(base, name, conflict=False):
    r = Repository(base, name)
    m = r.commit("M", {"f.txt": "main", "main.txt": "main"} if conflict else {"m.txt": "M"})
    r.git("switch", "-c", "feature", r.a)
    f = r.commit("F", {"f.txt": "feature", "extra.txt": "extra"} if conflict else {"f1.txt": "F"})
    return r, m, f


def verify(base):
    r = Repository(base, "staging")
    r.write("f.txt", "B")
    r.git("add", "f.txt")
    r.write("f.txt", "C")
    r.git("commit", "-m", "staged only")
    assert r.git("show", "HEAD:f.txt") == "B" and r.read("f.txt") == "C"
    keyed(10, "Commit contains B; working tree contains C")
    r.git("branch", "feature")
    assert r.git("branch", "--show-current") == "main"
    assert r.git("symbolic-ref", "HEAD") == "refs/heads/main"
    keyed(7, "The current index, also called the staging area")
    keyed(8, "Create feature at the current commit while leaving main checked out")
    keyed(9, "refs/heads/main")

    r = Repository(base, "fast-forward")
    r.git("switch", "-c", "feature")
    r.commit("B", {"b.txt": "B"})
    c = r.commit("C", {"c.txt": "C"})
    r.git("switch", "main")
    r.git("merge", "--ff-only", "feature")
    assert r.git("rev-parse", "main") == c and len(r.parents()) == 1
    keyed(11, "Move main to C without creating a new merge commit")

    r, m, f = diverge(base, "merge")
    r.git("switch", "main")
    r.git("merge", "--no-ff", "feature", "-m", "merge")
    assert r.parents() == [m, f] and r.read("m.txt") == "M" and r.read("f1.txt") == "F"
    keyed(12, "A merge commit with first parent M and second parent F")
    keyed(19, "Divergence alone does not imply a content conflict; Git can merge both additions")

    r, m, f = diverge(base, "merge-conflict", True)
    r.git("switch", "main")
    r.git("merge", "feature", ok=False)
    assert r.git("show", ":2:f.txt") == "main"
    assert r.git("show", ":3:f.txt") == "feature"
    r.git("merge", "--abort")
    assert r.git("rev-parse", "HEAD") == m and r.read("f.txt") == "main"
    keyed(25, "Stage 2 is main; stage 3 is feature; abort restores main at M")
    r.git("merge", "feature", ok=False)
    r.write("f.txt", "combined")
    r.git("add", "f.txt")
    r.git("commit", "-m", "resolve")
    assert r.parents() == [m, f] and r.read("f.txt") == "combined"
    keyed(13, "git add config.txt, then git commit")

    r = Repository(base, "stash-default")
    r.write("f.txt", "changed")
    r.write("notes.txt", "untracked")
    r.git("stash", "push")
    assert r.read("f.txt") == "base" and r.read("notes.txt") == "untracked"
    keyed(14, "Tracked-file changes only; notes.txt remains untracked in the working tree")
    r.git("stash", "apply")
    assert len(r.git("stash", "list").splitlines()) == 1
    r.git("restore", "f.txt")
    r.git("stash", "pop")
    assert r.git("stash", "list") == "" and r.read("f.txt") == "changed"
    keyed(15, "apply keeps the stash entry; successful pop removes it")

    r = Repository(base, "detached")
    r.git("switch", "--detach", r.a)
    x = r.commit("X", {"x.txt": "X"})
    r.git("switch", "-c", "rescue")
    assert r.git("branch", "--show-current") == "rescue" and r.git("rev-parse", "rescue") == x
    keyed(16, "git switch -c rescue")

    r = Repository(base, "cherry-single")
    r.git("switch", "-c", "feature")
    r.commit("F1", {"one.txt": "one"})
    f2 = r.commit("F2", {"two.txt": "two"})
    r.git("switch", "main")
    r.git("cherry-pick", f2)
    assert not (r.path / "one.txt").exists() and r.read("two.txt") == "two"
    assert r.parents() == [r.a] and r.git("rev-parse", "HEAD") != f2
    keyed(17, "F2's patch only, recorded as a new commit on main")

    r, m, f = diverge(base, "rebase")
    g = r.commit("G", {"g.txt": "G"})
    r.git("rebase", "main")
    assert r.git("rev-parse", "main") == m and r.parents() != [f]
    assert r.git("rev-parse", "HEAD~2") == m and not r.ancestor(f) and not r.ancestor(g)
    keyed(18, "A--M--F'--G', with feature at G' and main still at M")

    r, m, f = diverge(base, "rebase-ours", True)
    r.git("rebase", "main", ok=False)
    assert r.git("show", ":2:f.txt") == "main" and r.git("show", ":3:f.txt") == "feature"
    r.git("checkout", "--ours", "--", "f.txt")
    r.git("add", "f.txt")
    r.git("rebase", "--continue")
    assert r.read("f.txt") == "main" and r.read("extra.txt") == "extra" and r.parents() == [m]
    keyed(26, "f.txt uses main's version; extra.txt remains; feature's replayed commit has main as parent")

    r = Repository(base, "onto")
    m = r.commit("M", {"m.txt": "M"})
    r.git("switch", "-c", "feature", r.a)
    b = r.commit("B", {"b.txt": "B"})
    r.commit("C", {"c.txt": "C"})
    r.commit("D", {"d.txt": "D"})
    r.git("rebase", "--onto", "main", b, "feature")
    assert r.git("rev-parse", "HEAD~2") == m and not (r.path / "b.txt").exists()
    assert all((r.path / name).exists() for name in ("m.txt", "c.txt", "d.txt"))
    keyed(27, "M, then new C' and D'; files m.txt, c.txt, d.txt are present and b.txt is absent")

    r = Repository(base, "stash-index")
    r.write("f.txt", "B")
    r.git("add", "f.txt")
    r.write("f.txt", "C")
    r.git("stash", "push")
    r.git("stash", "apply", "--index")
    assert r.git("show", ":f.txt") == "B" and r.read("f.txt") == "C"
    r.git("commit", "-m", "staged only")
    assert r.git("show", "HEAD:f.txt") == "B" and r.read("f.txt") == "C"
    assert len(r.git("stash", "list").splitlines()) == 1
    keyed(28, "Commit contains B; working tree contains C; stash entry remains")

    r = Repository(base, "cherry-abort")
    m = r.commit("M", {"f.txt": "main"})
    r.git("switch", "-c", "source", r.a)
    c = r.commit("C", {"c.txt": "C"})
    d = r.commit("D", {"f.txt": "source"})
    r.git("switch", "main")
    r.git("cherry-pick", c, d, ok=False)
    assert r.git("show", "-s", "--format=%s", "HEAD") == "C"
    r.git("cherry-pick", "--abort")
    assert r.git("rev-parse", "HEAD") == m and not (r.path / "c.txt").exists()
    assert r.read("f.txt") == "main"
    keyed(29, "main and tracked files return to their pre-sequence state at M, removing C' from the branch history")

    for operation in ("merge", "rebase"):
        r, m, f = diverge(base, "comparison-" + operation)
        g = r.commit("G", {"g.txt": "G"})
        if operation == "merge":
            r.git("merge", "--no-ff", "main", "-m", "merge")
            assert r.parents() == [g, m] and r.ancestor(f) and r.ancestor(g)
        else:
            r.git("rebase", "main")
            assert len(r.parents()) == 1 and not r.ancestor(f) and not r.ancestor(g)
    keyed(30, "Merge retains original F and G as ancestors of its two-parent tip; rebase creates F' and G' after M and need not retain original F or G as ancestors")
    print("PASS: 19 Git answer keys checked against disposable-repository operations.")


def cleanup(base):
    base = base.resolve()
    if base.parent != ROOT.resolve() or not base.name.startswith(".systems_verify_"):
        raise RuntimeError("Unsafe temporary cleanup path")

    def remove_readonly(operation, name, error):
        path = Path(name).resolve()
        path.relative_to(base)
        if not isinstance(error[1], PermissionError):
            raise error[1]
        # Git objects are read-only on Windows, even after Git has exited.
        path.chmod(stat.S_IREAD | stat.S_IWRITE)
        operation(path)

    for attempt in range(20):
        try:
            shutil.rmtree(base, onerror=remove_readonly)
            break
        except PermissionError:
            if attempt == 19:
                raise
            time.sleep(0.25)


def main():
    base = Path(tempfile.mkdtemp(prefix=".systems_verify_", dir=ROOT)).resolve()
    try:
        verify(base)
    finally:
        cleanup(base)


if __name__ == "__main__":
    main()
