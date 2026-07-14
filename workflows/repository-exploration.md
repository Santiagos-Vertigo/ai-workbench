# Repository Exploration Workflow

## Purpose

A read-only, technology-agnostic workflow for inspecting an unfamiliar repository and producing
a structured briefing before any development work begins.

## Scope and Constraints

- Read-only by default — no repository modification during exploration.
- Technology-agnostic — must remain usable against any stack, including unknown ones.
- Usable against a repository with no prior context.
- Concise and repeatable — same procedure, same output structure, every time.
- Evidence-driven — every claim traces to something actually observed.
- Compatible with CLAUDE.md's Execution Authorization tiers and standards/git.md's Repository
  Awareness practices.

## Prohibited Actions

This workflow operates entirely within CLAUDE.md's Safe tier. It must never:

- Edit, create, delete, or move files.
- Install or update dependencies, or update lockfiles.
- Run migrations, start services, or execute build or test commands.
- Change configuration.
- Run `git add`, `git commit`, `git push`, `git pull`, or `git fetch`.
- Create, update, approve, close, or merge a pull request.
- Call any external system in a way that modifies state.

See CLAUDE.md's Execution Authorization for the full authorization tiers this workflow operates
under — this section does not redefine them, only confirms this workflow never leaves the Safe
tier.

## Procedure

1. Confirm the repository root and orient to the top-level structure.
2. Determine the repository's purpose from README, package manifest description, or equivalent
   top-level documentation; tag per Evidence Classification.
3. Determine current Git state per standards/git.md's Repository Awareness practices (branch,
   status, upstream tracking, divergence) — read-only, no fetch. Divergence and upstream tracking
   reflect the local remote-tracking state only; tag `[Inference]` rather than `[Verified]` when
   no fetch has occurred.
4. Identify languages and frameworks from manifests and file conventions.
5. Identify package managers and lockfiles present.
6. Locate application entry points.
7. Identify configuration and environment requirements (e.g. `.env.example`, config files)
   without reading secret values into the output.
8. Identify local initialization, development, build, and test commands from manifests or
   scripts — read only, never execute.
9. Identify test structure and locations.
10. Gather deployment evidence (CI/CD config, Dockerfiles, deployment manifests).
11. Identify architectural boundaries and important directories.
12. Locate documentation and decision records.
13. Cross-check documentation claims against observed code and repository state; flag conflicts.
14. Compile risks, missing information, and unresolved questions.
15. Assess development readiness.
16. Recommend next investigation steps — not next development actions; that belongs to a future
    workflow.

## Evidence Classification

Tag every claim in the briefing:

- `[Verified]` — directly observed in code, config, or repository state.
- `[Inference]` — a reasonable conclusion from partial or indirect evidence, not directly
  confirmed.
- `[Contradicted]` — a documentation or source claim that disagrees with observed code or
  repository state (see Handling Conflicting Evidence).
- `[Unknown]` — no evidence found; state this rather than guessing.

## Handling Conflicting Evidence

When documentation and observed code or state disagree, treat the code/state as `[Verified]` and
tag the documentation claim `[Contradicted]`. Surface the conflict under both Risks and
Unresolved Questions. Never silently prefer one without disclosing the conflict. Never edit
documentation to resolve it — this workflow is read-only.

## Handling Unknown or Unsupported Stacks

Report the raw evidence actually observed — file extensions, directory conventions, unrecognized
manifest filenames — rather than guessing a framework identity. Mark the relevant briefing
sections `[Unknown]` and list what was seen. Log the gap under Missing Information and Unresolved
Questions. Do not create an adapter speculatively; a recurring gap across projects is what would
justify one later.

## Repository Briefing Output

```
# Repository Briefing: <name>

## Repository Purpose
## Current Git State
## Top-Level Structure
## Languages and Frameworks
## Package Managers and Lockfiles
## Application Entry Points
## Configuration and Environment Requirements
## Local Initialization Commands
## Development Commands
## Build Commands
## Test Commands and Test Structure
## Deployment Evidence
## Architectural Boundaries
## Important Directories
## Documentation and Decision Records
## Risks
## Missing Information
## Unresolved Questions
## Development Readiness
## Recommended Next Investigation
```

## Execution Reference

CLAUDE.md defines whether an action may be executed; this workflow never leaves its Safe tier.
standards/git.md defines the Git engineering practice this workflow's Git-state step relies on.
Neither is restated here.
