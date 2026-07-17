# Development Workflow

## Purpose

A technology-agnostic workflow for making a scoped engineering change to a repository — from
confirming what outcome is wanted through reporting the result and the exact Git state. It covers
the full lifecycle of a change but never commits or pushes; those remain separate, explicit
actions this workflow can recommend but never performs on its own.

## Scope and Constraints

- Usable both for changes to this workbench (meta-development, governed by this repository's own
  CLAUDE.md) and for changes to a consuming project repository (governed by that project's own
  instructions and conventions, wherever they exist — this workflow does not assume this
  workbench's specific filenames apply elsewhere).
- Technology-agnostic — adapts to whatever tests, build, and lint tooling a repository actually
  has rather than prescribing a language or framework.
- Composes with, and never duplicates, workflows/repository-exploration.md — invoked in full when
  repository understanding is insufficient, not re-implemented here.
- Spans more of CLAUDE.md's authorization tiers than repository-exploration.md does: steps 1–9 stay
  within the Safe tier (read, analyze, propose); implementation (steps 10–11 onward) enters the
  approval-required tier only after the checkpoint in step 8. This workflow never performs `git
  add`, `git commit`, `git push`, or any other explicit-approval-every-time action — those are
  always separate decisions outside its scope.
- When Bounded Development Mode (CLAUDE.md) is already active for the declared repository and
  objective, steps 10–11's approval-required actions proceed under that existing pre-authorization
  rather than a fresh prompt before each one — this workflow does not redefine Bounded Development
  Mode, it only operates under it when active.

## Authorization Reference

This workflow does not define or restate CLAUDE.md's Execution Authorization tiers — every action
taken while executing it is bound by those tiers exactly as written there. It adds only these
workflow-specific constraints on top of them:

- Implementation (step 10 onward) never begins before scope, constraints, risks, and acceptance
  criteria have been stated in writing — presented as a checkpoint (step 8) outside an active
  Bounded Development Mode scope, or for transparency without blocking when that mode is already
  active for the declared repository and objective.
- Committing and pushing are always separate from "implement," "validate," and "report" — approval
  of any earlier step, and Bounded Development Mode itself, never implies approval of either; both
  remain in CLAUDE.md's explicit-approval-every-time tier, unaffected by Bounded Development Mode.

## Judgment Resolution

A workflow step requiring judgment is not automatically evidence that a Profile is needed. Before
treating any step's judgment call as unresolved, work through these in order:

1. **Repository evidence** — can the answer be read from the repository itself (code, config,
   tests, history, existing conventions)?
2. **Explicit decision criteria** — does an existing Standard, Workflow, or this document already
   supply a rule that decides it?
3. **Clarification from the user** — is this a scope or intent question only the requester can
   answer?
4. **Risk-based escalation** — does the action's risk already route it to a CLAUDE.md approval
   tier, making a standing behavioral stance unnecessary?
5. **Authorization checkpoint** — does pausing for explicit approval resolve it without requiring
   a standing stance at all?

Only flag a possible Profile requirement when a recurring behavioral stance survives all five —
i.e., it is not a one-off fact-finding or approval gap, and it would recur the same way across
multiple workflows, not just this one. Record the specific instance where this happens rather than
asserting the need generically.

## Procedure

1. **Confirm the requested outcome.** State the change in terms of the observable result expected,
   not the mechanism. If the request is ambiguous, resolve via clarification from the user
   (mechanism 3) — never by silent inference.
2. **Load repository instructions and current state.** Read the target repository's own operating
   instructions and state records if they exist. Resolved by repository evidence (mechanism 1).
3. **Use or refresh Repository Exploration when understanding is insufficient.** Apply an explicit
   check: can the files, contracts, and conventions the change will touch be named with
   confidence? If not, invoke workflows/repository-exploration.md in full before continuing.
4. **Inspect the relevant implementation before proposing changes.** Read the actual code,
   configuration, or content the change will touch — not just the structural briefing. Resolved by
   repository evidence.
5. **Establish the current validation baseline.** Identify repository-native checks (tests, build,
   lint, type-check) from manifests or scripts. Run what is Safe-tier read-only; request approval
   first for anything CLAUDE.md's tiers gate. Record the baseline before any mutation — step 11 has
   nothing to compare against without it.
6. **Define scope, constraints, risks, and acceptance criteria.** State them in writing before any
   mutation. Resolve ambiguous boundaries via explicit decision criteria already established in the
   repository, or, failing that, clarification from the user — never assumption.
7. **Separate verified facts, inferences, and unresolved questions.** Apply the Evidence
   Classification scheme from workflows/repository-exploration.md (`[Verified]` / `[Inference]` /
   `[Unknown]`) to everything gathered in steps 2–6; do not redefine it here.
8. **Propose an implementation plan proportional to the change, and present it as a checkpoint —
   or, if Bounded Development Mode is already active for this exact repository and objective,
   present it for transparency without waiting on a further approval before continuing.** Scale
   plan detail to blast radius — files touched, whether public interfaces or contracts change,
   reversibility, whether shared or production state is affected. Outside an active Bounded
   Development Mode scope, present scope, constraints, risks, acceptance criteria, and plan to the
   user before anything is created or edited; this is an authorization checkpoint (mechanism 5),
   not a formality.
9. **Observe CLAUDE.md's Execution Authorization boundaries before any mutation.** Plan approval in
   step 8 is not, by itself, execution approval. Outside an active Bounded Development Mode scope,
   each individual Edit, Create, Delete, dependency install, or configuration change still requires
   its own approval exactly as CLAUDE.md defines, regardless of what was approved earlier in this
   workflow. Inside an active Bounded Development Mode scope, Edit, Create, directory creation,
   dependency install, build, test, and lint actions proceed without a fresh prompt for each
   instance, per CLAUDE.md's Bounded Development Mode — but Delete, Rename/move, Execute
   migrations, and every action in CLAUDE.md's explicit-approval-every-time tier remain
   individually gated regardless of Bounded Development Mode.
10. **Implement narrowly and incrementally.** Match existing repository conventions observed in
    step 4 — repository evidence is the default resolution for implementation-choice judgment
    calls. Where no convention exists, default to the simplest option that satisfies the acceptance
    criteria and note the choice in the report rather than embedding an unstated opinion. Never
    bundle unrelated changes into the same unit of work (standards/git.md).
11. **Validate using repository-native tests, builds, linting, or checks.** Re-run the checks
    established in step 5 and compare against the baseline. Execution still requires whatever
    CLAUDE.md tier applies — the step 8 checkpoint does not cover it.
12. **Review the resulting diff for correctness, scope, security, documentation, and unintended
    changes.** Treat this review and the report in step 13 as the checkpoint that substitutes for
    domain-specific judgment this workflow cannot supply on its own (mechanism 5) — surface
    anything uncertain rather than silently deciding it looks fine.
13. **Report the result, remaining risks, and exact Git state.** Include what changed, baseline vs.
    post-change validation evidence, diff review findings, remaining risks, and current
    branch/status/ahead-behind state.
14. **Treat committing and pushing as separate, explicit actions.** Neither is implied by approval
    of the plan, the implementation, or the report. Each requires its own explicit approval per
    CLAUDE.md's explicit-approval-every-time tier, following standards/git.md's Review Before
    Action practice.

## Development Report Output

```
# Development Report: <change summary>

## Requested Outcome
## Repository Context Used
## Validation Baseline
## Scope, Constraints, and Acceptance Criteria
## Implementation Plan
## Changes Made
## Post-Change Validation
## Diff Review Findings
## Remaining Risks
## Exact Git State
## Commit/Push Status
```

`Commit/Push Status` always states the literal current state (e.g. "Not committed. Not pushed.")
until each is separately authorized and executed, per step 14.

## Execution Reference

CLAUDE.md defines whether any action in this workflow may be executed — this document does not
redefine its tiers, only sequences work within them. standards/git.md defines the Git engineering
practice steps 6, 10, 13, and 14 rely on, and governs commit/push once separately authorized.
workflows/repository-exploration.md defines the exploration procedure step 3 invokes rather than
duplicates. None of the three is restated here.
