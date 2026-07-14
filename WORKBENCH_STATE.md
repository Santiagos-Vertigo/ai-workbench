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

v0.5 (complete)

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

## Current Status

v0.5 Development Workflow is complete. workflows/development.md is the completed deliverable,
validated against README.md, CLAUDE.md, standards/git.md, and workflows/repository-exploration.md,
with no conflicts found and none of those four documents modified. No Profile requirement was
demonstrated; profiles/ remains intentionally absent. Both open architectural questions
(authorization detail placement; communication-style calibration) remain unresolved and are carried
forward unchanged. No next milestone has yet been approved. CLAUDE.md remains the sole authority
for execution permission.

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
├── standards/
│   └── git.md
└── workflows/
    ├── development.md
    └── repository-exploration.md
```

## Next Objective

No active objective. v0.5 is complete and no next milestone has been approved. v0.6 — Code Review
Workflow is next on the roadmap, but has not been started and must not begin speculatively. Ask
what concrete task motivates the next change before proposing new files or folders. Do not create
profiles/ — no Profile requirement has been demonstrated. Do not commit or push until separately
authorized.

## Resume Instructions

1. Read README.md for vision and philosophy, then this file for current state.
2. Review the execution authorization policy before proposing repository changes.
3. Confirm no new Layer 1 structure has been added speculatively — profiles/ still does not exist.
4. Confirm v0.5 is complete and no next milestone (v0.6 or otherwise) has been approved or started.
5. Review Open Questions before touching workflows/repository-exploration.md's Prohibited
   Actions section or creating a docs/ directory.
6. Ask what concrete task motivates the next change before proposing new files or folders.
