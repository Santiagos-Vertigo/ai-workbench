# Session Initialization Workflow

## Purpose

The mandatory gate that runs before any capability workflow is invoked or any repository other
than the one already active is accessed. It establishes operating mode, requested outcome, and
exactly which repository is in scope, then recommends — but never selects or executes — the
Workbench capability appropriate to that scope.

## Scope and Constraints

- Runs before workflows/repository-exploration.md, workflows/development.md, or any future
  capability workflow — it does not duplicate their procedures, only gates entry to them.
- Operates only on the current conversation and the already-active repository's own Git state
  until a different repository's scope is explicitly confirmed. Never accesses an external
  repository — not even read-only — merely to determine whether it is in scope.
- Proportional by design:
  - Never re-ask for information the user's current request already stated explicitly and
    unambiguously.
  - Never introduce a confirmation loop beyond the single scope checkpoint a given situation
    actually requires.
  - Never automatically execute the capability it recommends.

## Authorization Reference

This workflow does not define or restate CLAUDE.md's Execution Authorization tiers — every action
taken while executing it is bound by those tiers exactly as written there, including the Core Rule
requiring session scope to be established before invoking a capability workflow or accessing
another repository. It adds only this workflow-specific constraint on top of them:

- Recommending a capability in step 8 is not authorization to invoke it — invocation is a separate,
  later confirmation, exactly as CLAUDE.md's "discussion is never authorization to execute" already
  requires.

## Scope-Selection Rule

- If the user's current request explicitly and unambiguously selects a repository, that
  establishes the candidate scope — do not ask a redundant question to re-confirm it.
- A repository mentioned only in prior context, an example, a hypothetical, or a recommendation
  this workflow or any other part of the session generated is **not** selected.
- The assistant's own navigation to a directory (for example, a shell `cd`) never itself selects
  or authorizes that directory — only the user's explicit statement does. Repeated `cd` commands
  reaching a location are not evidence of scope and must never be treated as if they were.
- If accessing a repository the user did not explicitly select is being proposed, stop and present
  a direct scope checkpoint; wait for confirmation before accessing it.
- Before Bounded Development Mode (see CLAUDE.md) is entered against a repository other than the
  one already active, that repository must also be an explicitly authorized accessible directory
  (e.g. via `--add-dir` or `/add-dir`) — naming it in a message is necessary but not sufficient for
  development actions, only for read-only inspection under the scope gate below.
- When the active target is ambiguous, ask rather than infer.

## Procedure

1. **Determine the operating mode and autonomy scope.** Operating mode is modifying the Workbench,
   using the Workbench, or architectural discussion only. Autonomy scope is Read-Only/Explore, the
   default, or Bounded Development (Build) — the latter requires an explicit statement from the
   user naming both the target repository and the objective and explicitly invoking bounded
   development/Build-mode autonomy, per CLAUDE.md's Bounded Development Mode. Resolve both from the
   user's current request; if unclear, ask — never infer from task shape alone. Re-run this
   determination whenever the requested outcome shifts to a materially different engineering
   objective within the same conversation — a prior autonomy-scope grant does not carry over to a
   new, unrelated objective.
2. **Establish the requested outcome** in the user's own terms.
3. **Identify candidate repositories** named anywhere in the current request.
4. **Distinguish explicit selection from contextual mention**, per the Scope-Selection Rule above —
   only an explicit, unambiguous selection in the user's current request establishes candidate
   scope; a prior mention, example, hypothetical, or AI-generated recommendation does not.
5. **Require confirmation** whenever repository selection was inferred, proposed by the AI,
   ambiguous, or would cross into a repository other than the one already active — presented as a
   direct scope checkpoint, not folded into approval of something else. Skip this step only when
   step 4 already found an explicit, unambiguous selection in the current request.
6. **Access no external repository** — including read-only inspection — before the scope gate in
   step 5 is satisfied.
7. **Once scope is established**, load the active repository's own local instructions (its own
   CLAUDE.md-equivalent, contract files, state files, if any) and current Git state, per
   standards/git.md's Repository Awareness practices.
8. **Recommend** — never select or execute — the Workbench capability (workflow) appropriate to
   the requested outcome.
9. **State, for the recommended capability**: allowed actions, prohibited actions, and required
   approval checkpoints, by cross-reference to CLAUDE.md's tiers and the target workflow's own
   Authorization Reference — not restated here; plus the expected output and the stop condition
   marking initialization complete and hand-off ready.
10. **Produce a Session Scope Declaration** (below) and stop for confirmation before invoking the
    recommended capability.

## Session Scope Declaration Output

```
# Session Scope Declaration

## Operating Mode
## Autonomy Scope
## Requested Outcome
## Active Repository
## In-Scope Repositories
## Excluded Repositories
## Current Git State
## Applicable Repository-Local Instructions
## Recommended Capability
## Allowed Actions
## Prohibited Actions
## Required Approval Checkpoints
## Expected Output
## Stop Condition
```

## Execution Reference

CLAUDE.md defines whether any action in this workflow may be executed, and requires this
workflow's scope gate to run before a capability workflow is invoked or another repository is
accessed — neither is redefined here. standards/git.md defines the Git engineering practice step 7
relies on. workflows/repository-exploration.md and workflows/development.md define the procedures
this workflow gates entry to, rather than duplicates. None of the three is restated here.
