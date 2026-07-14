# Project State Contract

## Purpose and Scope

This Standard defines the minimum canonical vocabulary a repository's project-state file should
use to be reliably legible to both humans and Workbench tooling (e.g., the Workbench Console). It
is a rule about document *structure* — "WHAT rules always apply" — not a procedure and
not an execution-permission document. CLAUDE.md remains the sole authority for execution
permission; this Standard never grants or restricts it. Workflows remain the "WHAT steps to follow"
layer; this Standard does not define a procedure.

This document defines the contract. Any Workbench Console implementation must conform to it
exactly — canonical headings, required/optional classification, evidence-label behavior, and
legacy-alias precedence, as defined below (see "Console Integration Requirements"). Implementation
status (what is currently built, migrated, or still pending) is tracked in `WORKBENCH_STATE.md`,
not here.

## Canonical Field Table

| Field | Canonical Heading | Category |
|---|---|---|
| Project Purpose | `## Project Purpose` | Required |
| Current Milestone / Version | `## Current Milestone / Version` | Required |
| Current Objective | `## Current Objective` | Required |
| Next Objective | `## Next Objective` | Required* |
| Lifecycle Phase | `## Lifecycle Phase` | Optional, free-form |
| Intended Outcome | `## Intended Outcome` | Optional |
| Definition of Done | `## Definition of Done` | Optional |
| Completed Work | `## Completed Work` | Optional |
| Blockers / Open Questions | `## Blockers / Open Questions` | Optional |

\* Next Objective must be present, but its declared content may explicitly state that nothing has
been selected yet — see "Missing, Empty, Unresolved, and Malformed Behavior" below.

## Required vs. Optional Rules

- **Required** (Project Purpose, Current Milestone / Version, Current Objective, Next Objective) —
  must be present with non-empty declared content for the file to be a fully contract-compliant
  project-state source. "Required" means required for full compliance, not required for the file to
  be readable at all: a file missing every canonical heading is still read without error; each
  missing field simply reports `[Unknown]`.
- **Optional** (Lifecycle Phase, Intended Outcome, Definition of Done, Completed Work, Blockers /
  Open Questions) — declared when relevant; absence carries no compliance penalty and reports
  `[Unknown]`.
- **Lifecycle Phase remains free-form.** No closed enumeration is defined — see Non-Goals.
- **Active Assistant, Active Workflow, and Active Profile are excluded from this contract** because
  they are ephemeral session state, not persistent project state. Their correct home is
  workflows/session-initialization.md's Session Scope Declaration. This Standard does not govern
  them, does not rename them, and does not require or forbid a repository from writing them
  elsewhere in its own state file — they are simply outside this contract's canonical vocabulary.

## Evidence-Label Behavior

Reuses, without redefining, the four labels already established in
workflows/repository-exploration.md and docs/console-specification.md:

- `[Verified]` and `[Stale Possible]` do not apply to declared project-state content — those labels
  are reserved for filesystem- and Git-derived facts, which this Standard does not govern (see
  docs/console-specification.md's State Discovery Contract for those).
- `[Declared]` — a canonical field's heading (or a documented legacy alias — see below) is present
  with non-empty content in the state file the discovery order actually selected.
- `[Unknown]` — no heading in the field's precedence chain (canonical or any documented alias, see
  "Legacy Alias and Precedence Rules") is present, or the heading selected by that chain is present
  but empty.
- **No cross-heading inference, ever.** Fields must not be inferred from other headings — a field's
  value is never derived from a different field's content. For example, Lifecycle Phase is never
  derived from Current Milestone / Version's status word.

## Missing, Empty, Unresolved, and Malformed Behavior

- **Missing** (no heading in the field's precedence chain — canonical or any documented alias — is
  present anywhere in the file): `[Unknown]`.
- **Present, empty content** (the heading selected by the precedence walk in "Legacy Alias and
  Precedence Rules" has nothing beneath it): `[Unknown]` — a heading with nothing beneath it is not
  a declaration, and evaluation does not continue to a lower-precedence alias.
- **Present heading, explicitly unresolved content** (Next Objective only): `[Declared]` — the
  declared fact is "nothing has been selected yet." This requires actual text saying so; an empty
  section under the heading is still `[Unknown]`, not an implicit "unresolved."
- **Malformed or unreadable state file** (the file exists but cannot be read or parsed at all):
  every canonical field in this Standard reports `[Unknown]`, and the specific read/parse problem is
  reported alongside. This defers entirely to docs/console-specification.md's existing
  malformed-file handling — no fallback to a secondary file — which this Standard does not
  redefine.
- No canonical field is ever inferred from Git history, source code, or any file this Standard does
  not name.

## File Discovery Compatibility

This Standard does not define or alter which filename is checked or in what order — that remains
docs/console-specification.md's State Discovery Contract (`WORKBENCH_STATE.md`, then
`PROJECT_STATE.md`, first match wins, no fallback on a malformed higher-priority file). This
Standard governs content structure only, identically regardless of which filename a given
repository uses.

## Copyable Generic Markdown Skeleton

```markdown
## Project Purpose
<One to two sentences: why this repository/project exists.>

## Current Milestone / Version
<Current milestone or version label and its status, e.g. "v2.3 (in progress)".>

## Current Objective
<What is actively being worked on right now.>

## Next Objective
<What comes after the current objective — or state plainly that nothing has been
chosen yet. Either way, write something; do not leave this heading empty.>

## Lifecycle Phase
<Optional. A short, free-form description of where this project stands,
e.g. "early prototyping," "in production, maintenance only.">

## Intended Outcome
<Optional. What will exist or be true once the current objective is achieved.>

## Definition of Done
<Optional. Concrete, checkable criteria for confirming the current objective
is actually complete.>

## Completed Work
<Optional. Notable completed work, most relevant or recent first.>

## Blockers / Open Questions
<Optional. Known blockers or unresolved questions.>
```

Nothing in this skeleton references ai-workbench, Claude, or any Workbench-specific concept — it is
generic project documentation any repository could plausibly already be close to satisfying.

## Legacy Alias and Precedence Rules

| Canonical Heading | Legacy Alias(es), in precedence order |
|---|---|
| `## Current Milestone / Version` | `## Current Version` |
| `## Current Objective` | `## Current Status` |
| `## Lifecycle Phase` | 1. `## Project Phase`  2. `## Current Phase` |
| `## Completed Work` | `## Completed` |
| `## Blockers / Open Questions` | `## Open Questions` |

**Precedence algorithm.** For any canonical field, evaluate in this fixed order, stopping at the
first heading found present in the file — whether or not its content is empty:

1. The canonical heading. If present, it is authoritative, even when empty. An empty canonical
   section reports `[Unknown]`; any legacy alias present in the same file is ignored for that
   field.
2. Each documented legacy alias for that field, in the order listed above. If the canonical heading
   is absent and multiple documented aliases exist, the first alias in the documented order that is
   present is authoritative — even when empty. A present but empty higher-precedence alias reports
   `[Unknown]`; lower-precedence aliases are ignored and never consulted as a fallback.
3. If no heading in the chain (canonical or any documented alias) is present at all, the field
   reports `[Unknown]`.

**No undocumented heading is ever recognized** as equivalent to a canonical field or alias, however
similar it looks — only the exact mappings in the table above apply.

Legacy aliases exist solely so an already-existing project-state file — for example, this
repository's own pre-migration `WORKBENCH_STATE.md`, or any other repository's pre-existing state
file — can eventually be read without immediate rewriting. New files should use canonical headings
directly.

**Workbench Console implementations must recognize the documented aliases and precedence exactly**
— this document defines the mapping and precedence; conformance is a console-implementation
responsibility, not something this document performs itself.

## Adoption Guidance

- AI Workbench dogfoods this contract through its own `WORKBENCH_STATE.md`. External repository
  adoption remains voluntary and incremental.
- Satisfying only the four required fields already materially improves how legible a project's
  state is — the five optional fields add detail but are not a barrier to basic compliance.
- No repository is ever required to add a schema/version marker or a closed Lifecycle Phase value —
  neither exists.

## Non-Goals

- No closed Lifecycle Phase enumeration.
- No schema/version marker.
- No session/runtime fields (Active Assistant, Active Workflow, Active Profile) — session state,
  not project state; they belong to workflows/session-initialization.md's Session Scope
  Declaration.
- No mandated filename or discovery-order change.
- No requirement that any external repository adopt this contract.
- No console implementation — this document defines the contract only.
- Does not standardize changelog or history tracking beyond the current-state snapshot.

## Console Integration Requirements

These are durable conformance requirements for any Workbench Console implementation — not
requirements this document itself fulfills:

- A console implementation, its specification, and its regression suite must stay in agreement at
  every commit — no commit may leave the console unable to accurately self-report on this
  repository's own state file.
- The regression suite for this contract must be stored in the repository itself, written using
  only the Python standard library — consistent with the console's dependency-free discipline —
  never left only as an ephemeral scratchpad script.
- The regression suite must cover: canonical headings only; every documented legacy alias;
  canonical-over-alias precedence; missing headings; empty headings; and an explicitly unresolved
  Next Objective.
- External repository validation is never required for conformance with this Standard.
- No schema-version marker is required or introduced by conformance with this Standard.

## Execution Reference

CLAUDE.md determines whether an action related to drafting or applying this Standard is authorized
to execute — this document does not redefine its tiers. docs/console-specification.md defines the
console contract that implements this Standard — not restated here.
workflows/repository-exploration.md's and workflows/development.md's Evidence Classification
schemes are reused here, not redefined.
