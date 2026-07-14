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

v0.4 (in progress)

## Completed

- Layer 0 Foundation completed.
- Behavior Contract completed.
- Created standards/ — the first justified Layer 1 artifact.
- Created standards/git.md, defining universal Git engineering practice.
- standards/git.md reviewed and validated.
- Created workflows/repository-exploration.md — first Layer 1 workflow artifact.

## Current Status

v0.4 Repository Exploration is in progress. CLAUDE.md remains the sole authority for execution
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

Review and validate workflows/repository-exploration.md before marking v0.4 complete.

## Resume Instructions

1. Read README.md for vision and philosophy, then this file for current state.
2. Review the execution authorization policy before proposing repository changes.
3. Confirm no new Layer 1 structure has been added speculatively.
4. Confirm the next objective is reviewing and validating workflows/repository-exploration.md
   before marking v0.4 complete.
5. Ask what concrete task motivates the next change before proposing new files or folders.
