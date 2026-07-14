# Workbench Console Specification

Defines the Workbench Console's `status` command. Project-state field definitions, canonical
headings, evidence-label behavior for declared state, and legacy-alias precedence are governed by
standards/project-state.md and referenced here, not restated.

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

Before any packaging/installation exists:

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
than surfacing it. Instead: the project-state fields (item 8 below) are reported `[Unknown]`, and
the source problem is reported clearly and specifically (e.g. "`WORKBENCH_STATE.md` found but could
not be parsed") rather than silently substituted.

If neither file exists, the project-state fields remain `[Unknown]`. The console does not
assume every repository has one, does not derive phase or objective from Git history, does not
invent a development stage, and does not silently treat `README.md` as structured project state. If
`README.md` information is surfaced at all, it is labeled a **source excerpt**, never an inferred
purpose — a README does not constitute declared project state.

Wherever a field below is described as an "excerpt," it means the first complete paragraph, or
first complete list item, beneath the relevant heading — Markdown-wrapped physical lines are joined
with normalized spaces, and extraction stops only at a blank line or the next structural block
(the next list item, or the next heading), never merely because the source text wrapped to another
physical line. An excerpt still never reproduces an entire long section; if a maximum length
applies, it truncates at a word boundary with a visible ellipsis.

### The fields

1. **Repository identity** — the directory name (basename of the resolved path) `[Verified]`. If
   `README.md` exists, its first heading line may be shown alongside as a labeled source excerpt
   (`README Heading`), never presented as a verified or inferred purpose.
2. **Resolved repository path** — the absolute, normalized form of the argument `[Verified]`.
3. **Git branch** — from `git branch --show-current` `[Verified]`. If HEAD is detached, reported
   explicitly as `detached HEAD`, never left blank.
4. **HEAD commit** — short hash plus subject line `[Verified]`.
5. **Working-tree condition** — `clean` or `dirty (n changed paths)` from `git status --porcelain`
   `[Verified]`. A dirty tree is a normal, valid, reportable state, never an error.
6. **Ahead/behind state** — relative to the locally available tracking reference (`@{u}`), if one
   exists. The ahead/behind count itself is `[Stale Possible]`, since no fetch is ever performed and
   the local remote-tracking ref may be out of date. If no upstream is configured, that fact is
   directly observable from local Git state and is reported as `no upstream configured`
   `[Verified]` — not attempted, not guessed, and not tagged `[Stale Possible]`, since "no upstream
   exists" does not depend on remote freshness the way an actual count would.
7. **Remote freshness limitation** — a standing disclaimer shown whenever item 6 is shown. When an
   upstream exists: no fetch is ever performed, so ahead/behind reflects local remote-tracking refs
   only. When no upstream is configured: wording states plainly that no ahead/behind comparison is
   available because no upstream is configured — the generic no-fetch caveat does not apply, since
   there is no tracking reference to be stale in the first place.
8. **Project-state fields** — Project Purpose, Lifecycle Phase, Current Milestone / Version,
   Current Objective, Intended Outcome, Definition of Done, Completed Work, Next Objective, and
   Blockers / Open Questions. Their canonical headings, required/optional classification,
   evidence-label behavior, and legacy-alias precedence (including the ordered Lifecycle Phase
   chain — `Project Phase`, then `Current Phase`) are defined entirely by
   standards/project-state.md and are not restated here. The console implements that contract
   exactly: a canonical heading wins whenever present, even if empty (which reports `[Unknown]` and
   masks any legacy alias); if the canonical heading is absent, the first present legacy alias in
   documented order wins, even if empty; no undocumented heading is ever recognized. No
   project-state field is ever inferred from another field, from `README.md`, from Git history, or
   from source code.
9. **Repository-local instruction files found** — `[Verified]` presence check against a fixed,
   documented list: `README.md`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, and the project-state
   filenames from the discovery order above. Presence only — contents are not parsed except for the
   one file selected per item 10.
10. **Project-state file used as the source** — `[Verified]` the exact filename actually read to
    populate item 8's fields, chosen via the discovery order above. If none matched, that absence is
    itself directly observable and is reported as `None found` `[Verified]` — the *fact* that no
    recognized state file exists is verified, even though it means every project-state field
    reports `[Unknown]` accordingly. Never silently substitutes `README.md`.
11. **Active assistant** — `[Declared]` only if an `Active Assistant` field/heading is explicitly
    present in the recognized state file; otherwise `Unknown` `[Unknown]`. A stateless, independent
    invocation of the console has no way to know whether Claude, Codex, or another assistant is
    already running in the surrounding session — it must never guess, and must never report
    `not launched` as if that were a verified fact about that external session. (The console may
    separately, truthfully state that *this command's own execution* did not launch an assistant —
    see Authorization State below — but that is a fact about itself, not knowledge of the session.)
    Not part of the Project State Contract — session/runtime state, not project state.
12. **Active workflow** — `[Declared]` only if an `Active Workflow` field/heading is explicitly
    present in the recognized state file; otherwise `Unknown` `[Unknown]`, for the same reason as
    item 11. Recommending or selecting a workflow remains the AI session's job via
    workflows/session-initialization.md; the console never infers this.
13. **Active Profile** — `[Declared]` only if an `Active Profile` field/heading is explicitly
    present in the recognized state file; otherwise `Unknown` `[Unknown]`, for the same reason as
    item 11. `profiles/` does not exist yet; even after it does, the console may only report a
    Profile a repository explicitly declares — never invented, never assumed absent.
14. **Authorization state** — `[Verified]`, since this is a fact the program controls about its own
    execution, not repository content: report-only console operation; this command did not modify
    files, launch an assistant, select a workflow, or activate a Profile. This is a statement about
    what the command itself just did — it must not be read as knowledge of the surrounding session
    (see items 11–13).
15. **Stop condition** — `[Verified]`, for the same reason as item 14: the command has completed and
    exited; no process remains running. The console is single-shot, never a background process.

## 8. Output Presentation Contract

Output is grouped into seven titled sections, in this order, each containing the fields listed:

1. **REPOSITORY** — Repository Identity, README Heading (if `README.md` exists), Resolved
   Repository Path.
2. **GIT** — Branch, HEAD Commit, Working-Tree Condition, Ahead/Behind Upstream, Remote Freshness.
3. **PROJECT** — Project Purpose, Lifecycle Phase, Current Milestone / Version, Current Objective,
   Intended Outcome, Definition of Done, Completed Work (excerpt), Next Objective — in this order,
   per standards/project-state.md's Canonical Field Table.
4. **BLOCKERS / OPEN QUESTIONS** — Blockers / Open Questions.
5. **CONFIG** — Instruction Files Found, Project-State File Used, and, only when the higher-priority
   state file could not be read or parsed, State Source Problem.
6. **SESSION** — Active Assistant, Active Workflow, Active Profile.
7. **RESULT** — Authorization State, Stop Condition.

Every field from the State Discovery Contract above appears exactly once, in the section it
semantically belongs to. Splitting fields into sections changes nothing about how they are
discovered, parsed, classified, or truncated — it is presentation only.

**Alignment:** within each section, field labels are aligned to that section's own longest label —
not aligned across sections. A section-context label may drop a redundant prefix implied by the
section title (e.g. "Git Branch" becomes "Branch" inside GIT; "Repository-Local Instruction Files
Found" becomes "Instruction Files Found" inside CONFIG) without changing the field's meaning or
evidence label.

**Wrapping:** a value too long for the terminal wraps onto further lines whose continuation begins
under the *value* column (immediately after the label and its separator), never under the label.
Wrapping adapts to the terminal's actual width (with a reasonable fallback when none is detected);
this specification does not mandate one fixed column width or exact whitespace — only that
continuation lines align under the value, sections stay in the order above, and no field, meaning,
or evidence label changes as a result of how a given terminal happens to wrap it.

**Never hidden for visual cleanliness:** `Unknown` values, `[Stale Possible]` staleness, a dirty
working tree, blockers/open questions, and the Authorization State line must always be shown in
full — grouping and alignment are cosmetic and must never cause a field to be omitted, truncated
beyond the existing excerpt rule, or softened.

Illustrative shape (structural — exact spacing, terminal width, and the concrete values shown are
not part of the contract; only the sections, fields, order, and evidence labels are):

```
Workbench Status — <repository-identity>

REPOSITORY
  Repository Identity      : <directory name> [Verified]
  README Heading           : "<text>" [Verified] — source excerpt, not a verified or inferred
                              purpose
  Resolved Repository Path : <absolute path> [Verified]

GIT
  Branch                  : <branch | "detached HEAD"> [Verified]
  HEAD Commit             : <short hash> <subject> [Verified]
  Working-Tree Condition  : <clean | dirty (n changed paths)> [Verified]
  Ahead/Behind Upstream   : <n ahead, m behind> [Stale Possible]  |  no upstream configured [Verified]
  Remote Freshness        : No fetch was performed; ahead/behind reflects local remote-tracking
                            refs only.  (or, when no upstream: No upstream is configured, so no
                            ahead/behind comparison is available.)

PROJECT
  Project Purpose              : <value> [Declared]  |  [Unknown]
  Lifecycle Phase              : <value> [Declared]  |  [Unknown]
  Current Milestone / Version  : <value> [Declared]  |  [Unknown]
  Current Objective            : <value> [Declared]  |  [Unknown]
  Intended Outcome             : <value> [Declared]  |  [Unknown]
  Definition of Done           : <value> [Declared]  |  [Unknown]
  Completed Work (excerpt)     : <value> [Declared]  |  [Unknown]
  Next Objective                : <value> [Declared]  |  [Unknown]

BLOCKERS / OPEN QUESTIONS
  Blockers / Open Questions : <value> [Declared]  |  [Unknown]

CONFIG
  Instruction Files Found : <list> [Verified]
  Project-State File Used : <filename> [Verified]  |  None found [Verified]
  State Source Problem    : <message>   (only present if the higher-priority state file was
                             found but could not be read or parsed)

SESSION
  Active Assistant : <value> [Declared]  |  Unknown [Unknown]
  Active Workflow  : <value> [Declared]  |  Unknown [Unknown]
  Active Profile   : <value> [Declared]  |  Unknown [Unknown]

RESULT
  Authorization State : Report-only console operation; this command did not modify files, launch
                        an assistant, select a workflow, or activate a Profile. [Verified]
  Stop Condition       : Command complete; no process remains running. [Verified]
```

This is a structural template, not a fixed or permanently expected output. Any concrete, filled-in
example shown elsewhere (in review, discussion, or documentation) using a real path, commit hash,
dirty-tree count, or exact column spacing must be explicitly labeled illustrative and is not
authoritative — actual output always reflects the state at the moment a given invocation ran, and
its exact spacing depends on the terminal it ran in.

## 9. Error Behavior

- **Missing path** (no argument given) — print usage, exit non-zero, no further output.
- **Nonexistent path** — report "Path does not exist: `<path>`", exit non-zero.
- **Non-directory path** (e.g. a file) — report "Path is not a directory: `<path>`", exit non-zero.
- **Non-Git directory** — report the facts that are available (identity, resolved path), explicitly
  report "Not a Git repository — Git fields unavailable" for items 3–7, exit non-zero. A graceful
  partial report, not a crash.
- **Missing state file** — not an error; report Project-State File Used as `None found` `[Verified]`
  (the absence itself is directly observable) and every project-state field as `[Unknown]`, and exit
  zero. Many legitimate repositories won't have one.
- **Malformed or unreadable state file** — report the file itself as found `[Verified]`, but every
  project-state field as `[Unknown]` with an explicit note that the file could not be parsed. Never
  guess partial content, never crash, and never fall back to the secondary discovery-order file —
  see the precedence rule in the State Discovery Contract above.
- **Canonical heading present but empty, or a higher-precedence legacy alias present but empty** —
  reports `[Unknown]` for that field; never falls through to a lower-precedence alias — per
  standards/project-state.md's precedence algorithm, applied exactly.
- **Detached HEAD** — report Git Branch as `detached HEAD` explicitly; HEAD commit still reports
  normally.
- **Missing upstream** — report Ahead/Behind as `no upstream configured` `[Verified]` (not
  `[Stale Possible]` — the absence of an upstream is directly observable, not dependent on remote
  freshness); never attempted or guessed, never crashes.
- **Dirty working tree** — a normal, valid state; reported as `dirty (n changed paths)`, never an
  error, never a reason to block the report.

## 10. Statelessness Requirement (Workbench Console)

The Workbench Console must be fully stateless. It may write only to stdout and stderr. Under any
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

Future persistent state, caching, history, or configuration is explicitly out of scope for the
Workbench Console and requires a separately approved milestone — it is not assumed, and this
specification does not authorize it. Verified in every validation scenario via before/after
`git status` (and a filesystem check where relevant) on both the target repository and the
ai-workbench installation.

## 11. Security and Scope Restrictions

- Local filesystem paths only — no URLs, no remote cloning, no network access at all.
- Never executes code found inside the target repository — no running scripts, no importing
  modules, no evaluating config files as code. Filesystem and Git inspection only.
- Never reads or displays file contents beyond what is explicitly specified above (declared state
  fields, the README's first heading) — never dumps arbitrary file contents, avoiding accidental
  secret exposure, the same discipline workflows/repository-exploration.md already applies.
- Runs with whatever OS-level permissions the invoking user already has. Requests no elevation,
  installs nothing, modifies no system state.

### Git Subprocess Safeguards (Workbench Console requirement)

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

These are Workbench Console requirements; this document specifies them but does not itself
implement them.

## 12. Exclusions (Workbench Console)

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
    technology-agnosticism — explicitly reserved for actual implementation review, not part of
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
