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

v0.7 — Technology Adapters

v0.8 — Project Initialization

v0.9 — Capability Composition

v1.0 — Portable AI Engineering Workbench

The roadmap is intentionally lightweight. Future versions are placeholders for direction only.

## Current Version

v0.4 (complete)

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

## Current Status

v0.4 Repository Exploration is complete. CLAUDE.md remains the sole authority for execution
permission.

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

## Open Questions

- **Where should enumerated authorization detail live: CLAUDE.md or individual workflows?**
  workflows/repository-exploration.md's Prohibited Actions list bans `git fetch`, which is absent
  from CLAUDE.md's explicit-approval tier, and omits "Create directories," which is present in
  CLAUDE.md's approval-required tier. Neither is unsafe — the workflow is more conservative than
  CLAUDE.md, not less — but the drift means a workflow-local list can diverge from the document
  CLAUDE.md itself calls "the sole authority for execution permission." Unresolved: (a) update
  CLAUDE.md's tiers and reconcile the workflow's list against it, or (b) remove itemized
  enumeration from workflows entirely and rely solely on each workflow's cross-reference to
  CLAUDE.md's tiers, so no duplicate/divergent list can exist. Do not modify
  workflows/repository-exploration.md's Prohibited Actions section, and do not create a new
  docs/ directory for this question, until it is decided.

## Current Repository Structure

```text
ai-workbench/
├── README.md
├── CLAUDE.md
├── WORKBENCH_STATE.md
├── standards/
│   └── git.md
└── workflows/
    └── repository-exploration.md
```

## Next Objective

No active objective. v0.5 — Development Workflow is next on the roadmap, but no file or folder
should be created speculatively. Ask what concrete task motivates the next change before proposing
new structure. Separately, the Open Questions item above (authorization detail placement) needs a
decision whenever it's picked up.

## Resume Instructions

1. Read README.md for vision and philosophy, then this file for current state.
2. Review the execution authorization policy before proposing repository changes.
3. Confirm no new Layer 1 structure has been added speculatively.
4. Confirm v0.4 is complete and no objective is currently active.
5. Review Open Questions before touching workflows/repository-exploration.md's Prohibited
   Actions section or creating a docs/ directory.
6. Ask what concrete task motivates the next change before proposing new files or folders.
