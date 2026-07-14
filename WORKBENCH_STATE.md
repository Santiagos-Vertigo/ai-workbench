# AI Workbench State

# Workbench Roadmap

v0.1 — Foundation
- README.md
- CLAUDE.md
- WORKBENCH_STATE.md

v0.2 — Behavior Contract
- Execution authorization
- Human-in-the-loop policy
- Git approval policy

v0.3 — Engineering Standards
- standards/git.md

v0.4 — Repository Exploration
- workflows/repository-exploration.md

v0.5 — Development Workflow

v0.6 — Code Review Workflow

v0.7 — Workbench Console Architecture and State Contract (specification only)

v0.8 — Workbench Console MVP (read-only `status` command)

v0.9 — Project State Contract and Console Integration

v1.0 — Portable AI Engineering Workbench

The roadmap is intentionally lightweight. Future versions are placeholders for direction only.

## Current Version

v0.9 (in progress) — Project State Contract and Console Integration

## Completed

- Layer 0 Foundation completed.
- Behavior Contract completed.
- Created standards/ — the first justified Layer 1 artifact.
- Created standards/git.md, defining universal Git engineering practice.
- standards/git.md reviewed and validated.
- Created workflows/repository-exploration.md — first Layer 1 workflow artifact.
- Reviewed and validated workflows/repository-exploration.md:
  - Added a Procedure step to determine repository purpose, closing a gap where the Repository
    Briefing Output template had no corresponding step.
  - Added staleness handling to the Git-state step so upstream tracking and divergence are tagged
    `[Inference]`, not `[Verified]`, when no fetch has occurred.
  - Identified a third finding (Prohibited Actions list drifts slightly from CLAUDE.md's tiers) and
    deferred it — see Open Questions.
- v0.4 marked complete.
- Conducted the v0.5 architectural assessment: defined the Standard / Workflow / Profile
  distinction and a five-mechanism judgment-resolution framework (repository evidence, explicit
  decision criteria, user clarification, risk-based escalation, authorization checkpoint) for
  deciding when a workflow step's judgment call would actually require a Profile.
- Created workflows/development.md — the Development Workflow, covering the full engineering-change
  lifecycle from confirming the requested outcome through reporting the exact Git state.
  Cross-references CLAUDE.md's authorization tiers rather than restating an itemized Prohibited
  Actions list.
- Applied the judgment-resolution framework to all 14 procedure steps in
  workflows/development.md: none required a Profile — every judgment call resolved via repository
  evidence, explicit decision criteria, user clarification, risk-based escalation, or an
  authorization checkpoint. The Profile hypothesis is not yet confirmed; profiles/ remains
  unjustified and was not created.
- v0.5 marked complete. Deliverable: workflows/development.md — the Development Workflow, covering
  the full engineering-change lifecycle from confirming the requested outcome through reporting the
  exact Git state, with commit and push always left as separate, unstarted actions.
- Validated workflows/development.md against all four reference documents before completion:
  - README.md: stays within Layer 1 (workflow), technology-agnostic, adds no application code or
    stack-specific detail, and follows composition-over-duplication by cross-referencing rather
    than restating.
  - CLAUDE.md: Execution Authorization tiers are cross-referenced, never redefined or restated;
    approval checkpoints (steps 8, 9, 14) directly encode "discussion is never authorization" and
    "approval for one action never authorizes another"; profiles/ was not created.
  - standards/git.md: step 10 (never bundle unrelated changes) and step 14 (commit/push as
    separate, explicit actions) align directly with its Commits and Review Before Action sections;
    no Git practice is redefined.
  - workflows/repository-exploration.md: invoked in full by step 3 rather than duplicated; its
    Evidence Classification tags are reused by reference in step 7; structural pattern (Purpose →
    Scope → Procedure → Output → Execution Reference) matches, with two additive sections
    (Authorization Reference, Judgment Resolution) justified by this workflow's mutating scope.
  - No concrete conflict was found in any of the four documents; none was modified.
- Confirmed no Profile requirement was demonstrated: every judgment point encountered while
  designing workflows/development.md resolved through repository evidence, explicit decision
  criteria, user clarification, risk-based escalation, or an authorization checkpoint. profiles/
  remains intentionally absent.
- v0.5 marked complete.
- An earlier v0.6 direction (Operational Workflow Validation against Logitrac GPS Console) was
  started, then explicitly stopped before any external modification occurred — Logitrac was
  accessed strictly read-only, its Git state was confirmed unchanged, and ai-workbench's own
  in-progress state was restored to the committed v0.5 baseline. That excursion surfaced a real,
  demonstrated gap: nothing in CLAUDE.md, standards/git.md, or either workflow governed *which*
  repository may be treated as in scope — only what actions may be taken once scope is already
  established. This motivated the current v0.6 direction below.
- Created workflows/session-initialization.md — the mandatory scope gate that must run before any
  capability workflow is invoked or any repository other than the active one is accessed. Composes
  with, and does not duplicate, workflows/repository-exploration.md and workflows/development.md;
  follows the cross-reference-only Authorization Reference pattern development.md established.
- Added one Core Rule to CLAUDE.md making workflows/session-initialization.md discoverable and
  operational: session scope must be established before invoking a capability workflow or
  accessing another repository, and prior context (a mention, an example, a hypothetical, or an
  AI-generated recommendation) never by itself authorizes selecting, accessing, modifying, or
  acting on a repository.
- Validated workflows/session-initialization.md against four simulated scenarios entirely inside
  ai-workbench (no external repository accessed): explicit Workbench-modification request;
  external repository mentioned only hypothetically; AI-recommended external repository; and
  user-selected external repository. Confirmed the incident that motivated this milestone would
  have been caught.
- Applied the judgment-resolution framework to the incident itself: resolved via explicit decision
  criteria, risk-based escalation, and an authorization checkpoint — not Profile evidence, since no
  recurring behavioral stance survived the five mechanisms. profiles/ remains intentionally absent.
- Completion review of v0.6: found that the CLAUDE.md Core Rule's original wording — "...never by
  itself authorizes selecting, accessing, modifying, or acting on it — only the user's...selection
  does" — grouped scope authorization (selecting/accessing) and action authorization
  (modifying/acting) under the same clause, which could be misread as selection alone authorizing
  modification. Corrected with the smallest necessary wording: selection now explicitly establishes
  scope only, and a new sentence states it never by itself authorizes modifying, staging,
  committing, pushing, deploying, or any other action already gated by CLAUDE.md's tiers.
  workflows/session-initialization.md was checked for the same ambiguity and does not share it — its
  language was already scoped precisely to "candidate scope" and "read-only inspection" — so it was
  left unmodified.
- Validated the corrected rule against four exact scenarios: (A) explicit Workbench-modification
  request — mode and target established with no redundant question, action authorization still
  gates the actual edit; (B) a repository named only inside a hypothetical, illustrative question —
  correctly classified as contextual, not selected, even though named in the current message, no
  access occurs; (C) an AI-generated recommendation to use an unselected external repository —
  stops at a direct scope checkpoint before any access; (D) an explicit request naming an external
  repository — scope established immediately with no redundant question, read-only initialization
  proceeds, but the recommended capability (Repository Exploration) is still only recommended, not
  auto-invoked. All four passed.
- Confirmed: Session Initialization runs before any capability workflow; it recommends rather than
  auto-executes; it produces a concise Session Scope Declaration; no Profile evidence was produced;
  no conflicting authorization model was introduced (the correction removed an internal ambiguity
  rather than adding a new rule surface); v0.1 through v0.5 history remains preserved and unaltered.
- v0.6 marked complete.
- Assessed a candidate v0.7 (Workbench Console) direction: found that a terminal console is
  executable application code with no existing Layer 1 folder to hold it, directly in tension with
  README's "not an application... never contains application code" statement — a Layer-0 identity
  question, not a routine content addition. Recommended splitting into a specification milestone
  (v0.7) and an implementation milestone (v0.8), and resolving the tension explicitly rather than
  silently proceeding either way.
- Resolved the tension: this repository may contain thin, optional, dependency-light operational
  tooling (`tools/`) that reports framework and repository state without becoming the source of
  truth, redefining authorization, or selecting workflows. The Markdown framework remains
  authoritative. Recorded in README.md's "What this is" section and a new "Optional Operational
  Tooling" note in the Architecture section.
- Created docs/console-specification.md — the first justified docs/ artifact — defining the
  console's purpose, its non-authoritative relationship to the framework, command syntax, required
  arguments, a 20-field State Discovery Contract (with an explicit, ordered project-state file
  discovery list and four evidence labels: `[Verified]`, `[Declared]`, `[Unknown]`,
  `[Stale Possible]`), exact output format, error behavior for nine distinct conditions, a zero-write
  requirement, security/scope restrictions, MVP exclusions, validation scenarios, criteria for
  proceeding to v0.8, and future boundaries (Claude launching, workflow recommendation, session
  history, Profiles, multiple agents, persistent monitoring — all explicitly deferred).
- Reconciled the roadmap: v0.7 relabeled "Workbench Console Architecture and State Contract
  (specification only)"; v0.8 relabeled "Workbench Console MVP (read-only `status` command)",
  replacing the stale "Technology Adapters"/"Project Initialization" placeholders.
- No Python or PowerShell code written; tools/ not created — both explicitly deferred to v0.8.
- Completion review of v0.7 applied five final corrections: (1) corrected README's identity
  language, which read as contradictory between "never contains application code" and "may contain
  thin, optional tooling" — now explicitly distinguishes application code of projects operated
  through the Workbench (never here) from operational tooling for the Workbench itself (may live
  under `tools/`, non-authoritative); (2) resolved the v0.8 MVP statelessness question — stdout/
  stderr only, with an explicit list of prohibited write targets, and future persistent state/
  caching/history/configuration requires its own separately approved milestone; (3) strengthened the
  Git read-only contract with explicit subprocess safeguards (no fetch, no push, no auth, disabled
  credential prompts, disabled optional locks/index-refresh, disabled lazy fetch,
  `GIT_OPTIONAL_LOCKS=0` / `GIT_TERMINAL_PROMPT=0` / `GIT_NO_LAZY_FETCH=1` as v0.8 requirements, not
  yet implemented); (4) clarified state-file precedence — `WORKBENCH_STATE.md` wins if both exist,
  and a malformed higher-priority file is never silently replaced by the secondary file, since that
  could conceal a broken authoritative state file; (5) labeled the output template as structural,
  not a fixed or permanently expected example.
- Revalidated the complete specification against all sixteen required elements (identity, Git
  state, phase, milestone/version, current/next objectives, blockers, instruction/state sources,
  assistant/workflow/Profile state, authorization state, evidence labels, stop condition, error/exit
  behavior, zero persistent writes, no network access, no inferred repository, no automatic workflow
  selection or AI launch) — all present.
- v0.7 marked complete.
- Verified Python 3 availability (3.14.4) via read-only version commands before implementing.
- Created tools/console/workbench.py — the first v0.8 artifact: a single, stdlib-only, stateless,
  read-only status reporter implementing docs/console-specification.md's `status` command exactly,
  including the 20-field State Discovery Contract, four evidence labels, the fixed
  WORKBENCH_STATE.md-then-PROJECT_STATE.md discovery order with no fallback on a malformed
  higher-priority file, and the specified Git subprocess safeguards
  (`GIT_OPTIONAL_LOCKS=0`, `GIT_TERMINAL_PROMPT=0`, `GIT_NO_LAZY_FETCH=1`, no stdin, no shell
  construction). `sys.dont_write_bytecode = True` is set before any other import.
- Applied a targeted correctness and validation pass before completion:
  - Fixed multiline declared-field extraction — the console previously read only the first
    physical (wrapped) source line of a Markdown section, producing truncated excerpts like
    "tools/console/workbench.py exists and". It now extracts the first complete paragraph or
    list item, joining wrapped lines with normalized spaces and stopping only at a blank line
    or the next structural block, truncating at a word boundary with an ellipsis when a length
    cap applies.
  - Corrected Project Phase semantics — it no longer derives phase from the parenthetical
    milestone status in Current Version ("in progress"/"complete" are milestone statuses, not
    project phases). It now reports `[Declared]` only from an explicit "Project Phase" or
    "Current Phase" field, otherwise "Unknown [Unknown]".
  - Corrected stateless session-state reporting — Active Assistant, Active Workflow, and Active
    Profile no longer hardcode "not launched" / "not selected" / "none configured" as if the
    console had knowledge of the surrounding session; a stateless invocation cannot know that.
    They now report `[Declared]` only from an explicit state-file field, otherwise
    "Unknown [Unknown]". Authorization State and Stop Condition are now explicitly labeled
    `[Verified]` and Authorization State separately, truthfully states that this command's own
    execution did not launch an assistant, select a workflow, or activate a Profile — without
    presenting that as knowledge of the external session.
  - Updated docs/console-specification.md to match all three corrections (items 8, 16–20, and
    the output template) so the specification and implementation agree.
- Ran the complete synthetic acceptance validation (14 scenarios: A–M plus the two missing-argument
  cases) using temporary fixtures created solely under the OS temp directory via Python's
  `tempfile`, with local-only Git identity, no remotes, and no network operation — including a
  clean repository with a locally configured upstream constructed via one local branch tracking
  another (zero `git remote` configured, proving ahead/behind reporting without any remote at
  all). All 14 scenarios passed. Every synthetic Git fixture was verified byte-for-byte unchanged
  (file listing plus `git status`/`HEAD`) before and after the console ran against it, and the
  entire fixture root was deleted afterward, with removal independently confirmed.
- v0.8 marked complete.

## Current Status

- v0.9 is in progress.
- standards/project-state.md has been reviewed and approved.
- Console specification, console implementation, persistent tests, and structural migration of
  WORKBENCH_STATE.md have not started.

## Architectural Decisions

- Repository responsibility split:
  - README.md defines the vision and architecture for humans.
  - CLAUDE.md defines operating instructions for AI assistants.
  - WORKBENCH_STATE.md records current state, decisions, and the resume point.
- Do not create Layer 1 folders speculatively.
- Create profiles, workflows, standards, adapters, templates, or docs only when a concrete engineering need justifies them.
- Prefer incremental growth through real use.
- The workbench follows a human-in-the-loop execution model.
- AI should recommend actions before executing repository modifications.
- Source control operations are always user-controlled.
- Safety and predictability take precedence over automation.
- CLAUDE.md remains the sole authority for execution permission; standards/ defines engineering
  practice, never permission to act.
- A Profile is justified only when a recurring behavioral stance survives all five
  judgment-resolution mechanisms (repository evidence, explicit decision criteria, user
  clarification, risk-based escalation, authorization checkpoint) and would recur the same way
  across multiple workflows — not merely because a single step "requires judgment."
- New workflow documents cross-reference CLAUDE.md's Execution Authorization tiers rather than
  restating an itemized Prohibited Actions list, to avoid the drift identified in the Open
  Questions item below. workflows/development.md follows this pattern; it is a precedent, not yet
  a retroactive fix — see Open Questions.

## Open Questions

- **Where should enumerated authorization detail live: CLAUDE.md or individual workflows?**
  workflows/repository-exploration.md's Prohibited Actions list bans `git fetch`, which is absent
  from CLAUDE.md's explicit-approval tier, and omits "Create directories," which is present in
  CLAUDE.md's approval-required tier. Neither is unsafe — the workflow is more conservative than
  CLAUDE.md, not less — but the drift means a workflow-local list can diverge from the document
  CLAUDE.md itself calls "the sole authority for execution permission." Unresolved: (a) update
  CLAUDE.md's tiers and reconcile the workflow's list against it, or (b) remove itemized
  enumeration from workflows entirely and rely solely on each workflow's cross-reference to
  CLAUDE.md's tiers, so no duplicate/divergent list can exist. workflows/development.md was written
  using approach (b), which is now a working precedent for that resolution — but
  workflows/repository-exploration.md's Prohibited Actions section has not been touched, and this
  question remains formally open. Do not modify it, and do not create a new docs/ directory for
  this question, until it is decided.
- **Does communication-style/explanation-depth calibration belong to a future Profile, or to
  CLAUDE.md's existing Role section?** It recurs across every workflow and isn't cleanly resolved
  by any of the five judgment-resolution mechanisms, which makes it structurally similar to what
  would justify a Profile — but CLAUDE.md already carries a single, repository-wide behavioral
  stance ("Role") for meta-work on this workbench. Unresolved whether a consuming-project-facing
  Profile would duplicate that or address a genuinely different scope. Not urgent — no workflow
  step has hit this concretely yet.

## Current Repository Structure

```text
ai-workbench/
├── README.md
├── CLAUDE.md
├── WORKBENCH_STATE.md
├── docs/
│   └── console-specification.md
├── standards/
│   ├── git.md
│   └── project-state.md
├── tools/
│   └── console/
│       └── workbench.py
└── workflows/
    ├── development.md
    ├── repository-exploration.md
    └── session-initialization.md
```

## Next Objective

Align docs/console-specification.md and tools/console/workbench.py with the approved Project State
Contract, add the persistent standard-library regression suite, and structurally migrate
WORKBENCH_STATE.md without creating an intermediate broken checkpoint. These edits require separate
authorization.

## Resume Instructions

1. Read README.md for vision and philosophy, then this file for current state.
2. Review the execution authorization policy before proposing repository changes.
3. Confirm no new Layer 1 structure has been added speculatively — profiles/ still does not exist.
4. Confirm v0.9 is in progress; standards/project-state.md is approved, and console integration
   has not started.
5. Before invoking any capability workflow or accessing another repository, run
   workflows/session-initialization.md first — this is a CLAUDE.md Core Rule, not optional.
6. Review Open Questions before touching workflows/repository-exploration.md's Prohibited
   Actions section.
7. Ask what concrete task motivates the next change before proposing new files or folders.
