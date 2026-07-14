# Workbench Console Specification

Specification only — v0.7. No code is implemented by this document. Implementation is v0.8.

## Evidence Labels

Every field the console reports carries one of these labels, reusing and extending the vocabulary
workflows/repository-exploration.md already established:

- `[Verified]` — obtained directly from the filesystem or Git.
- `[Declared]` — explicitly stated in a recognized project-state or instruction file.
- `[Unknown]` — not available from an approved source; never guessed, never derived indirectly.
- `[Stale Possible]` — locally correct but dependent on a tracking reference that may be out of
  date because no fetch was performed.

## 1. Purpose

The console is optional, dependency-light tooling that reports Workbench and repository state. It
mechanizes the deterministic, evidence-gathering portion of workflows/session-initialization.md
(identify the repository, load its local instructions, capture its Git state) so a session can
start from an accurate snapshot instead of a human manually re-deriving it every time. It answers
"where does this project currently stand," not "what should happen next" — the latter remains
judgment, and stays with the AI session.

## 2. Relationship Between Framework Core and Optional Tooling

The Markdown framework — README.md, CLAUDE.md, standards/, workflows/, and the not-yet-created
profiles/, adapters/, templates/, docs/ — remains authoritative for behavior, rules, and
permission. `tools/` is a separate, optional layer that reads and reports; it never defines a rule,
never grants permission, never selects a workflow or capability, and is never treated as a source
of truth. If console output and the actual framework or repository state ever disagree, the
observed state wins — the same "observed state is Verified, claims are flagged" discipline
workflows/repository-exploration.md already applies to documentation-vs-code conflicts applies here
to console-output-vs-reality conflicts.

## 3. Why tools/console/ Belongs in This Repository

It reports on this framework's own state and a target repository's state using the same discovery
logic workflows/session-initialization.md already defines; keeping it in a separate repository
would duplicate or drift from that logic. "Optional" and "dependency-light" are load-bearing
constraints, not decoration: the Markdown framework must remain fully usable — by a human or an AI
— with zero tooling installed, and the tooling must never accrue dependencies that undermine
README's own "clone this repository alongside a project repository, on any machine" goal.

## 4. Non-Authoritative Nature of Console Output

Console output is a snapshot assembled at the moment it ran. It never redefines CLAUDE.md's
Execution Authorization tiers, never selects or silently recommends a workflow, and never grants
repository scope — the Scope-Selection Rule and workflows/session-initialization.md still govern
that, exercised by the AI session, not the console. Any AI session consuming console output must
treat it as a preview to be independently re-verified live (per session-initialization.md's own
steps), not as ground truth — this is the direct mitigation for the "stale context" risk identified
when this milestone was proposed.

## 5. Command Syntax

```
workbench status <repository-path>
```

During v0.8 development, before any packaging/installation exists:

```
python tools/console/workbench.py status <repository-path>
```

## 6. Required Arguments

`<repository-path>` — required, positional, given explicitly on every invocation. No default value,
no remembered "last used" repository, no inference from environment or prior context. This mirrors
the Scope-Selection Rule's "explicit, current, unambiguous" requirement exactly — a CLI argument the
user typed is the clearest possible instance of that.

## 7. State Discovery Contract

### Discovery order for project-state files

Checked at the repository root only, not recursively, in this exact order — first match wins:

1. `WORKBENCH_STATE.md`
2. `PROJECT_STATE.md`

If both exist, `WORKBENCH_STATE.md` wins.

If the higher-priority file exists but is malformed or unreadable, the console does **not** fall
back to the secondary file — falling back could conceal a broken authoritative state file rather
than surfacing it. Instead: the affected fields (8–13) are reported `[Unknown]`, and the source
problem is reported clearly and specifically (e.g. "`WORKBENCH_STATE.md` found but could not be
parsed") rather than silently substituted.

If neither file exists, state-dependent fields (8–13) remain `[Unknown]`. The console does not
assume every repository has one, does not derive phase or objective from Git history, does not
invent a development stage, and does not silently treat `README.md` as structured project state. If
`README.md` information is surfaced at all, it is labeled a **source excerpt**, never an inferred
purpose — a README does not constitute declared project state.

### The 20 fields

1. **Repository identity** — the directory name (basename of the resolved path) `[Verified]`. If
   `README.md` exists, its first heading line may be shown alongside as a labeled source excerpt
   (`README heading (source excerpt)`), never presented as a verified or inferred purpose.
2. **Resolved repository path** — the absolute, normalized form of the argument `[Verified]`.
3. **Git branch** — from `git branch --show-current` `[Verified]`. If HEAD is detached, reported
   explicitly as `detached HEAD`, never left blank.
4. **HEAD commit** — short hash plus subject line `[Verified]`.
5. **Working-tree condition** — `clean` or `dirty (n changed paths)` from `git status --porcelain`
   `[Verified]`. A dirty tree is a normal, valid, reportable state, never an error.
6. **Ahead/behind state** — relative to the locally available tracking reference (`@{u}`), if one
   exists `[Stale Possible]`. If no upstream is configured, reported as `no upstream configured`,
   not attempted or guessed.
7. **Remote freshness limitation** — a standing disclaimer shown whenever item 6 is shown: no fetch
   is ever performed, so ahead/behind reflects local remote-tracking refs only.
8. **Project phase** — `[Declared]` from the state file's own phase/version/status field if present;
   `[Unknown]` otherwise. Never derived from Git history.
9. **Current milestone or version** — `[Declared]` from the state file's own version/milestone
   field; `[Unknown]` otherwise.
10. **Current objective** — `[Declared]` from the state file's current-status/objective field;
    `[Unknown]` otherwise.
11. **Completed work** — `[Declared]`, a short excerpt (not a full reproduction) of the state
    file's completed-work section; `[Unknown]` otherwise.
12. **Next objective** — `[Declared]` from the state file's next-objective field; `[Unknown]`
    otherwise.
13. **Known blockers or unresolved questions** — `[Declared]` from an open-questions/blockers
    section if present; `[Unknown]` otherwise. Never inferred from TODOs, code, or Git history.
14. **Repository-local instruction files found** — `[Verified]` presence check against a fixed,
    documented list: `README.md`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, and the project-state
    filenames from the discovery order above. Presence only — contents are not parsed except for the
    one file selected per item 15.
15. **Project-state file used as the source** — `[Verified]` the exact filename actually read to
    populate items 8–13, chosen via the discovery order above. If none matched: `[Unknown]`, "no
    recognized state file found," and items 8–13 all report `[Unknown]` accordingly — never
    silently substitutes `README.md`.
16. **Active assistant** — `not launched`, `Claude`, `Codex`, or another explicitly selected tool.
    MVP always reports `not launched`, since v0.8 never launches anything; never inferred from
    environment variables or running processes.
17. **Active workflow** — `not selected` or `explicitly declared`, never inferred by the console.
    MVP always reports `not selected` — recommending or selecting a workflow remains the AI
    session's job via workflows/session-initialization.md.
18. **Active Profile** — `none configured` or `explicitly declared`, never invented. MVP always
    reports `none configured`, since `profiles/` does not exist; even after `profiles/` exists, the
    console may only report a Profile if a repository explicitly declares one through a mechanism
    defined separately — none exists yet.
19. **Authorization state** — a fixed statement: report-only console operation, no files modified,
    no additional action authorized by this command. Not derived from repository content — a
    statement of what the console itself just did.
20. **Stop condition** — a fixed statement: the command has completed and exited; no process
    remains running; re-run to refresh. The console is single-shot, never a background process.

## 8. Exact Output Fields and Evidence Labels

```
Workbench Console — Status Report

Repository Identity: <directory name> [Verified]
  README heading (source excerpt): "<text>" [Verified] — not a verified or inferred purpose
Resolved Repository Path: <absolute path> [Verified]

Git Branch: <branch | "detached HEAD"> [Verified]
HEAD Commit: <short hash> <subject> [Verified]
Working-Tree Condition: <clean | dirty (n changed paths)> [Verified]
Ahead/Behind Upstream: <n ahead, m behind | "no upstream configured"> [Stale Possible]
Remote Freshness: No fetch was performed. Ahead/behind reflects local remote-tracking refs only.

Project Phase: <value> [Declared]  |  [Unknown]
Current Milestone/Version: <value> [Declared]  |  [Unknown]
Current Objective: <value> [Declared]  |  [Unknown]
Completed Work (excerpt): <value> [Declared]  |  [Unknown]
Next Objective: <value> [Declared]  |  [Unknown]
Known Blockers/Unresolved Questions: <value> [Declared]  |  [Unknown]

Repository-Local Instruction Files Found: <list> [Verified]
Project-State File Used: <filename> [Verified]  |  "None found" [Unknown]

Active Assistant: not launched
Active Workflow: not selected
Active Profile: none configured

Authorization State: Report-only console operation. No files modified. No additional action
authorized by this command.
Stop Condition: Command complete. No process remains running. Re-run to refresh.
```

This is a structural template, not a fixed or permanently expected output. Any concrete, filled-in
example shown elsewhere (in review, discussion, or documentation) using a real path, commit hash, or
dirty-tree count must be explicitly labeled illustrative and is not authoritative — actual output
always reflects the state at the moment a given invocation ran.

## 9. Error Behavior

- **Missing path** (no argument given) — print usage, exit non-zero, no further output.
- **Nonexistent path** — report "Path does not exist: `<path>`", exit non-zero.
- **Non-directory path** (e.g. a file) — report "Path is not a directory: `<path>`", exit non-zero.
- **Non-Git directory** — report the facts that are available (identity, resolved path), explicitly
  report "Not a Git repository — Git fields unavailable" for items 3–7, exit non-zero. A graceful
  partial report, not a crash.
- **Missing state file** — not an error; report `[Unknown]` for items 8–13 and 15 as specified above
  and exit zero. Many legitimate repositories won't have one.
- **Malformed or unreadable state file** — report the file itself as found `[Verified]`, but items
  8–13 as `[Unknown]` with an explicit note that the file could not be parsed. Never guess partial
  content, never crash, and never fall back to the secondary discovery-order file — see the
  precedence rule in the State Discovery Contract above.
- **Detached HEAD** — report Git Branch as `detached HEAD` explicitly; HEAD commit still reports
  normally.
- **Missing upstream** — report Ahead/Behind as `no upstream configured`; never attempted or
  guessed, never crashes.
- **Dirty working tree** — a normal, valid state; reported as `dirty (n changed paths)`, never an
  error, never a reason to block the report.

## 10. Statelessness Requirement (v0.8 MVP)

The v0.8 console MVP must be fully stateless. It may write only to stdout and stderr. Under any
code path — including error paths — it must not intentionally create or modify:

- files in the target repository;
- files in the ai-workbench installation;
- cache files;
- log files;
- configuration files;
- temporary report files;
- session-history files;
- Python bytecode or `__pycache__` inside the Workbench;
- Git metadata or index state.

Future persistent state, caching, history, or configuration is explicitly out of scope for v0.8 and
requires a separately approved milestone — it is not assumed, and this specification does not
authorize it. Verified in every validation scenario via before/after `git status` (and a filesystem
check where relevant) on both the target repository and the ai-workbench installation.

## 11. Security and Scope Restrictions

- Local filesystem paths only — no URLs, no remote cloning, no network access in the MVP.
- Never executes code found inside the target repository — no running scripts, no importing
  modules, no evaluating config files as code. Filesystem and Git inspection only.
- Never reads or displays file contents beyond what is explicitly specified above (declared state
  fields, the README's first heading) — never dumps arbitrary file contents, avoiding accidental
  secret exposure, the same discipline workflows/repository-exploration.md already applies.
- Runs with whatever OS-level permissions the invoking user already has. Requests no elevation,
  installs nothing, modifies no system state.

### Git Subprocess Safeguards (v0.8 requirement, not yet implemented)

Every Git inspection subprocess the console invokes must:

- perform no fetch;
- perform no push;
- perform no authentication;
- disable terminal credential prompts;
- disable optional locks and index-refresh side effects;
- disable lazy network fetching when supported;
- operate only against locally available repository state.

The implementation must use the equivalent of:

- `GIT_OPTIONAL_LOCKS=0`
- `GIT_TERMINAL_PROMPT=0`
- `GIT_NO_LAZY_FETCH=1` when supported

These are specified here as v0.8 requirements; none are implemented by this document.

## 12. MVP Exclusions

Full GUI; VS Code replacement; automatic code modification; automatic capability execution;
multi-agent orchestration; Profiles without evidence; remote repository access; deployment;
background monitoring; launching Claude or any assistant; workflow recommendation; session history
or memory across runs; a remembered or inferred repository path.

## 13. Validation Scenarios

1. Run against ai-workbench itself — accurate self-report, `WORKBENCH_STATE.md` selected as source,
   zero writes.
2. Run with no argument — usage message, non-zero exit, zero writes.
3. Run against a nonexistent path — clear error, non-zero exit, zero writes.
4. Run against a file, not a directory — clear error, non-zero exit.
5. Run against a directory that is not a Git repository — graceful partial report, zero writes.
6. Run against a Git repository with no recognized state file — `[Unknown]` for items 8–13/15, no
   fallback to README, zero writes.
7. Run against a repository in detached HEAD — explicit report, no crash.
8. Run against a repository with no upstream configured — explicit report, no crash.
9. Run against a repository with a dirty working tree — accurate report, no attempt to modify,
   stash, or clean it.
10. *(Deferred, separately authorized)* run against a second real external repository to prove
    technology-agnosticism — explicitly reserved for actual v0.8 implementation review, not part of
    this specification's own validation.

## 14. Criteria for Proceeding to v0.8

- This specification reviewed and approved as its own checkpoint, separate from this draft.
- Python 3 availability on the target machine explicitly verified at implementation time, never
  assumed.
- No scope creep: v0.8 implements exactly the State Discovery Contract above and nothing more — no
  launch, no recommendation.
- Validation scenarios 1–9 above serve as the acceptance test suite before v0.8 is marked complete.

## 15. Future Boundaries

- **Claude launching** — a distinct, later increment; must introduce its own explicit
  confirmation/preview step before spawning anything — never silent.
- **Workflow recommendation** — requires judgment; remains the AI session's job via
  workflows/session-initialization.md indefinitely, unless a narrow, well-evidenced mechanical
  heuristic is separately proposed and justified.
- **Session history** — no persistence across runs in any future increment considered so far; each
  run stays independent by default.
- **Profiles** — the console must never invent or declare one; may only report one a repository
  explicitly declares through a mechanism that does not exist yet and is not designed here.
- **Multiple agents** — out of scope indefinitely absent a demonstrated need; no orchestration logic
  without its own separate architectural review.
- **Persistent monitoring** — excluded; the console remains single-shot by design in every future
  increment considered so far.
