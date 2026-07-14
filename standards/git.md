# Git Standard

## Purpose

This document defines universal Git engineering practice — rules that hold across every project
and technology stack this workbench touches. It describes how to use Git well. It does not define
what may be executed; execution permission is defined solely by CLAUDE.md.

## Repository Awareness

- Confirm the repository root before taking any action.
- Inspect the current branch and working-tree status before proposing changes.
- Determine whether the current branch tracks a remote, and how far it has diverged.
- Never assume the working tree is clean.
- Never mix unrelated changes into the same unit of work.

## Branches

- Protect the default branch.
- Use a separate branch for any meaningful unit of work.
- Keep a branch scoped to a single objective.
- Treat branch deletion and renaming as deliberate actions, never an incidental side effect of
  other work.
- Naming conventions are project-specific and are defined outside this standard.

## Commits

- Make focused, coherent commits.
- Review the diff before staging.
- Never bundle unrelated changes into one commit.
- Write clear, descriptive commit messages.
- Never commit secrets, local environment files (e.g. `.env`), generated dependencies, or
  machine-specific state.
- Treat published history as immutable by default — amending or rewriting it is an exceptional
  action, not routine practice.
- Commit message format and convention are project-specific and are defined outside this
  standard.

## Pull Requests

- Use a pull request as the review boundary where the project requires one.
- Keep pull request scope aligned with the branch's objective.
- Provide a clear title, summary, validation evidence, risks, and follow-up work.
- Distinguish "ready for review" from "ready to merge."
- Approval and merge policy are project- or organization-specific and are defined outside this
  standard.
- This standard does not define, and never duplicates, who may authorize pull request actions —
  see CLAUDE.md.

## History Safety

- Never force-push shared history by default.
- Avoid destructive reset operations.
- Preserve recoverability of prior state wherever possible.
- Prefer reversible actions over irreversible ones.
- Inspect history before rebasing or rewriting it.

## Review Before Action

Before any Git action:

1. Inspect status.
2. Inspect diff.
3. Identify files to include.
4. Identify files to exclude.
5. Verify no secrets or unrelated changes are present.
6. Recommend the next Git action rather than assuming it.

## Execution Reference

CLAUDE.md defines whether Git and pull request operations may be executed. This document defines
correct engineering practice, not permission to act.
