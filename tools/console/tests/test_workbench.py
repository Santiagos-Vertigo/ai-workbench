#!/usr/bin/env python3
"""Persistent regression suite for tools/console/workbench.py.

Standard-library only (unittest, subprocess, tempfile, shutil, os, sys, stat, re,
pathlib). Runs the console as a real subprocess against synthetic, temporary Git
fixtures — the same black-box invocation a real user would perform — plus one
self-report scenario against ai-workbench itself. Every fixture is created under the
OS temp directory and removed in tearDown, including on failure; no repository other
than ai-workbench and ephemeral temp fixtures is ever touched.

Run with:
    python tools/console/tests/test_workbench.py
"""

import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
CONSOLE = THIS_DIR.parent / "workbench.py"
WORKBENCH_ROOT = THIS_DIR.parent.parent.parent  # tools/console/tests -> repo root


def run_console(*args: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, str(CONSOLE), *args],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def run_git(*args: str, cwd: Path, check: bool = True) -> str:
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, env=env)
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {args} in {cwd} failed: {proc.stderr}")
    return proc.stdout.strip()


def init_repo(path: Path, branch: str | None = None) -> None:
    args = ["init", "-q"]
    if branch:
        args += ["-b", branch]
    run_git(*args, cwd=path)
    run_git("config", "user.email", "test@example.invalid", cwd=path)
    run_git("config", "user.name", "Workbench Test Suite", cwd=path)


def commit_all(path: Path, message: str = "init") -> None:
    run_git("add", "-A", cwd=path)
    run_git("commit", "-q", "-m", message, cwd=path)


def snapshot(path: Path):
    entries = {}
    for p in sorted(path.rglob("*")):
        if p.is_file():
            entries[str(p.relative_to(path))] = p.stat().st_size
    git_state = None
    if (path / ".git").exists():
        status = run_git("status", "--porcelain", cwd=path, check=False)
        head = run_git("rev-parse", "HEAD", cwd=path, check=False)
        git_state = (status, head)
    return entries, git_state


def rm_tree(path: Path) -> None:
    def _on_rm_error(func, target, exc_info):
        os.chmod(target, stat.S_IWRITE)
        func(target)

    shutil.rmtree(path, onerror=_on_rm_error)


def field_pattern(label: str, value_pattern: str) -> "re.Pattern[str]":
    """Format-tolerant "<label> : <value>" matcher — does not assume exact column
    padding, since render_section() aligns labels per section dynamically."""
    return re.compile(re.escape(label) + r"[ \t]*:[ \t]*" + value_pattern)


class FixtureTestCase(unittest.TestCase):
    """Base class providing a fresh temp-directory fixture root per test, always
    removed in tearDown — including when the test itself fails."""

    def setUp(self) -> None:
        self.tmp_root = Path(tempfile.mkdtemp(prefix="workbench_test_"))

    def tearDown(self) -> None:
        rm_tree(self.tmp_root)
        self.assertFalse(self.tmp_root.exists(), "fixture root was not fully removed")

    def new_repo(self, name: str, branch: str | None = None) -> Path:
        repo = self.tmp_root / name
        repo.mkdir()
        init_repo(repo, branch=branch)
        return repo

    def assert_unchanged(self, repo: Path, before) -> None:
        after = snapshot(repo)
        self.assertEqual(before, after, f"console run changed fixture at {repo}")

    def assertField(self, out: str, label: str, value_pattern: str) -> None:
        pattern = field_pattern(label, value_pattern)
        self.assertRegex(out, pattern, f"field {label!r} did not match {value_pattern!r}\n{out}")

    def assertFieldNot(self, out: str, label: str, value_pattern: str) -> None:
        pattern = field_pattern(label, value_pattern)
        self.assertNotRegex(out, pattern, f"field {label!r} unexpectedly matched {value_pattern!r}\n{out}")


# ---------------------------------------------------------------------------
# Existing v0.8 acceptance scenarios (A-M plus the two argument-error cases)
# ---------------------------------------------------------------------------


class TestArgumentAndPathErrors(FixtureTestCase):
    def test_no_arguments_at_all(self):
        rc, out, err = run_console()
        self.assertEqual(rc, 2)
        self.assertIn("usage", err)

    def test_status_with_no_path(self):
        rc, out, err = run_console("status")
        self.assertEqual(rc, 2)
        self.assertIn("usage", err)

    def test_nonexistent_path(self):
        fake = self.tmp_root / "does-not-exist"
        rc, out, err = run_console("status", str(fake))
        self.assertEqual(rc, 1)
        self.assertIn("does not exist", err)

    def test_file_instead_of_directory(self):
        f = self.tmp_root / "afile.txt"
        f.write_text("x")
        rc, out, err = run_console("status", str(f))
        self.assertEqual(rc, 1)
        self.assertIn("not a directory", err)

    def test_empty_non_git_directory(self):
        d = self.tmp_root / "empty_nongit"
        d.mkdir()
        before = snapshot(d)
        rc, out, err = run_console("status", str(d))
        self.assert_unchanged(d, before)
        self.assertEqual(rc, 1)
        self.assertIn("Not a Git repository", out)


class TestGitStateVariants(FixtureTestCase):
    def test_detached_head(self):
        repo = self.new_repo("detached")
        (repo / "a.txt").write_text("1")
        commit_all(repo, "one")
        (repo / "a.txt").write_text("2")
        commit_all(repo, "two")
        first_commit = run_git("rev-list", "--max-parents=0", "HEAD", cwd=repo)
        run_git("checkout", "-q", first_commit, cwd=repo)
        before = snapshot(repo)
        rc, out, err = run_console("status", str(repo))
        self.assert_unchanged(repo, before)
        self.assertEqual(rc, 0)
        self.assertField(out, "Branch", r"detached HEAD \[Verified\]")

    def test_no_upstream_configured(self):
        repo = self.new_repo("no_upstream")
        (repo / "a.txt").write_text("1")
        commit_all(repo)
        before = snapshot(repo)
        rc, out, err = run_console("status", str(repo))
        self.assert_unchanged(repo, before)
        self.assertEqual(rc, 0)
        self.assertField(out, "Ahead/Behind Upstream", r"no upstream configured \[Verified\]")

    def test_dirty_working_tree(self):
        repo = self.new_repo("dirty")
        (repo / "a.txt").write_text("1")
        commit_all(repo)
        (repo / "a.txt").write_text("2-modified")
        before = snapshot(repo)
        rc, out, err = run_console("status", str(repo))
        after = snapshot(repo)
        self.assertEqual(before, after)
        self.assertEqual(rc, 0)
        self.assertField(out, "Working-Tree Condition", r"dirty \(1 changed path\) \[Verified\]")

    def test_clean_repo_local_upstream_no_remote(self):
        repo = self.new_repo("local_upstream", branch="main")
        (repo / "a.txt").write_text("1")
        commit_all(repo)
        run_git("branch", "--track", "feature", "main", cwd=repo)
        run_git("checkout", "-q", "feature", cwd=repo)
        before = snapshot(repo)
        rc, out, err = run_console("status", str(repo))
        self.assert_unchanged(repo, before)
        remotes = run_git("remote", cwd=repo, check=False)
        self.assertEqual(remotes, "", "fixture must have zero git remotes configured")
        self.assertField(out, "Ahead/Behind Upstream", r"0 ahead, 0 behind \[Stale Possible\]")
        self.assertField(out, "Working-Tree Condition", r"clean \[Verified\]")


class TestStateFileDiscovery(FixtureTestCase):
    def test_no_recognized_state_file(self):
        repo = self.new_repo("no_state")
        (repo / "README.md").write_text("# Fixture\n")
        commit_all(repo)
        before = snapshot(repo)
        rc, out, err = run_console("status", str(repo))
        self.assert_unchanged(repo, before)
        self.assertEqual(rc, 0)
        self.assertField(out, "Project-State File Used", r"None found \[Verified\]")
        self.assertField(out, "Project Purpose", r"\[Unknown\]")

    def test_project_state_md_only(self):
        repo = self.new_repo("project_state_only")
        (repo / "PROJECT_STATE.md").write_text(
            "## Current Milestone / Version\n\nG-1.0\n\n## Current Objective\n\nWorking on it.\n"
        )
        commit_all(repo)
        before = snapshot(repo)
        rc, out, err = run_console("status", str(repo))
        self.assert_unchanged(repo, before)
        self.assertEqual(rc, 0)
        self.assertField(out, "Project-State File Used", r"PROJECT_STATE\.md \[Verified\]")
        self.assertIn("G-1.0", out)

    def test_both_state_files_workbench_state_wins(self):
        repo = self.new_repo("both_state_files")
        (repo / "WORKBENCH_STATE.md").write_text("## Current Milestone / Version\n\nWINS\n")
        (repo / "PROJECT_STATE.md").write_text("## Current Milestone / Version\n\nLOSES\n")
        commit_all(repo)
        before = snapshot(repo)
        rc, out, err = run_console("status", str(repo))
        self.assert_unchanged(repo, before)
        self.assertField(out, "Project-State File Used", r"WORKBENCH_STATE\.md \[Verified\]")
        self.assertIn("WINS", out)
        self.assertNotIn("LOSES", out)

    def test_malformed_primary_no_fallback(self):
        repo = self.new_repo("malformed_primary")
        (repo / "WORKBENCH_STATE.md").write_bytes(b"\xff\xfe\x00\x01bad-\x80\x81")
        (repo / "PROJECT_STATE.md").write_text(
            "## Current Milestone / Version\n\nSHOULD-NOT-APPEAR\n"
        )
        commit_all(repo)
        before = snapshot(repo)
        rc, out, err = run_console("status", str(repo))
        self.assert_unchanged(repo, before)
        self.assertEqual(rc, 0)
        self.assertIn("State Source Problem", out)
        self.assertNotIn("SHOULD-NOT-APPEAR", out)


class TestSelfReportAndArtifacts(unittest.TestCase):
    def test_self_report_against_ai_workbench(self):
        rc, out, err = run_console("status", str(WORKBENCH_ROOT))
        self.assertEqual(rc, 0)
        self.assertIn("Workbench Status", out)
        self.assertIn("[Declared]", out)

    def test_no_pycache_or_bytecode_created(self):
        before = set(WORKBENCH_ROOT.rglob("__pycache__"))
        run_console("status", str(WORKBENCH_ROOT))
        after = set(WORKBENCH_ROOT.rglob("__pycache__"))
        self.assertEqual(before, after)
        self.assertFalse(list(WORKBENCH_ROOT.rglob("*.pyc")))


# ---------------------------------------------------------------------------
# v0.9 Project State Contract: canonical headings, legacy aliases, precedence
# ---------------------------------------------------------------------------


class ProjectFieldFixture(FixtureTestCase):
    """Shared helper for tests that only vary WORKBENCH_STATE.md's content."""

    def report_for(self, content: str) -> str:
        repo = self.new_repo("fixture")
        (repo / "WORKBENCH_STATE.md").write_text(content)
        commit_all(repo)
        before = snapshot(repo)
        rc, out, err = run_console("status", str(repo))
        self.assert_unchanged(repo, before)
        self.assertEqual(rc, 0, f"console exited {rc}\nstderr: {err}")
        return out


class TestCanonicalHeadings(ProjectFieldFixture):
    def test_all_canonical_headings_recognized(self):
        out = self.report_for(
            "## Project Purpose\n\nPURPOSE-TEXT\n\n"
            "## Lifecycle Phase\n\nPHASE-TEXT\n\n"
            "## Current Milestone / Version\n\nMILESTONE-TEXT\n\n"
            "## Current Objective\n\nOBJECTIVE-TEXT\n\n"
            "## Intended Outcome\n\nOUTCOME-TEXT\n\n"
            "## Definition of Done\n\nDOD-TEXT\n\n"
            "## Completed Work\n\nCOMPLETED-TEXT\n\n"
            "## Next Objective\n\nNEXT-TEXT\n\n"
            "## Blockers / Open Questions\n\nBLOCKERS-TEXT\n"
        )
        for text in (
            "PURPOSE-TEXT", "PHASE-TEXT", "MILESTONE-TEXT", "OBJECTIVE-TEXT",
            "OUTCOME-TEXT", "DOD-TEXT", "COMPLETED-TEXT", "NEXT-TEXT", "BLOCKERS-TEXT",
        ):
            self.assertIn(text, out)


class TestLegacyAliases(ProjectFieldFixture):
    def test_current_version_alias(self):
        out = self.report_for("## Current Version\n\nLEGACY-MILESTONE\n")
        self.assertIn("LEGACY-MILESTONE", out)

    def test_current_status_alias(self):
        out = self.report_for("## Current Status\n\nLEGACY-OBJECTIVE\n")
        self.assertIn("LEGACY-OBJECTIVE", out)

    def test_completed_alias(self):
        out = self.report_for("## Completed\n\nLEGACY-COMPLETED\n")
        self.assertIn("LEGACY-COMPLETED", out)

    def test_open_questions_alias(self):
        out = self.report_for("## Open Questions\n\nLEGACY-BLOCKERS\n")
        self.assertIn("LEGACY-BLOCKERS", out)

    def test_project_phase_alias(self):
        out = self.report_for("## Project Phase\n\nLEGACY-PHASE-1\n")
        self.assertIn("LEGACY-PHASE-1", out)

    def test_current_phase_alias(self):
        out = self.report_for("## Current Phase\n\nLEGACY-PHASE-2\n")
        self.assertIn("LEGACY-PHASE-2", out)


class TestPrecedence(ProjectFieldFixture):
    def test_canonical_wins_over_alias(self):
        out = self.report_for(
            "## Current Milestone / Version\n\nCANONICAL-WINS\n\n"
            "## Current Version\n\nALIAS-LOSES\n"
        )
        self.assertIn("CANONICAL-WINS", out)
        self.assertNotIn("ALIAS-LOSES", out)

    def test_empty_canonical_masks_populated_alias(self):
        out = self.report_for(
            "## Current Milestone / Version\n\n\n\n"
            "## Current Version\n\nSHOULD-BE-MASKED\n"
        )
        self.assertNotIn("SHOULD-BE-MASKED", out)
        self.assertField(out, "Current Milestone / Version", r"\[Unknown\]")

    def test_lifecycle_phase_project_phase_beats_current_phase(self):
        out = self.report_for(
            "## Project Phase\n\nFIRST-ALIAS-WINS\n\n"
            "## Current Phase\n\nSECOND-ALIAS-LOSES\n"
        )
        self.assertIn("FIRST-ALIAS-WINS", out)
        self.assertNotIn("SECOND-ALIAS-LOSES", out)

    def test_lifecycle_phase_falls_through_to_current_phase(self):
        out = self.report_for("## Current Phase\n\nFALLBACK-WINS\n")
        self.assertIn("FALLBACK-WINS", out)

    def test_empty_higher_precedence_alias_masks_lower_alias(self):
        out = self.report_for(
            "## Project Phase\n\n\n\n"
            "## Current Phase\n\nSHOULD-BE-MASKED-TOO\n"
        )
        self.assertNotIn("SHOULD-BE-MASKED-TOO", out)
        self.assertField(out, "Lifecycle Phase", r"\[Unknown\]")

    def test_missing_canonical_and_all_aliases(self):
        out = self.report_for("## Something Unrelated\n\nirrelevant\n")
        self.assertField(out, "Lifecycle Phase", r"\[Unknown\]")
        self.assertField(out, "Current Milestone / Version", r"\[Unknown\]")

    def test_undocumented_heading_never_recognized(self):
        out = self.report_for("## Milestone\n\nNOT-A-RECOGNIZED-HEADING\n")
        self.assertNotIn("NOT-A-RECOGNIZED-HEADING", out)
        self.assertField(out, "Current Milestone / Version", r"\[Unknown\]")


class TestNextObjective(ProjectFieldFixture):
    def test_explicitly_unresolved_is_declared(self):
        out = self.report_for("## Next Objective\n\nNothing has been selected yet.\n")
        self.assertIn("Nothing has been selected yet.", out)
        self.assertField(out, "Next Objective", r"Nothing has been selected yet\. \[Declared\]")

    def test_missing_heading_is_unknown(self):
        out = self.report_for("## Current Objective\n\nsomething\n")
        self.assertField(out, "Next Objective", r"\[Unknown\]")

    def test_empty_heading_is_unknown(self):
        out = self.report_for("## Next Objective\n\n\n\n## Current Objective\n\nsomething\n")
        self.assertNotIn("Nothing has been selected yet.", out)
        self.assertField(out, "Next Objective", r"\[Unknown\]")


if __name__ == "__main__":
    unittest.main(verbosity=2)
