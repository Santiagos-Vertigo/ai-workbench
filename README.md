# AI Workbench

A portable, technology-agnostic engineering framework for working with AI coding assistants.

## What this is

This repository is **not an application** and **not a product**. It is the reusable engineering
framework — an Engineering Operating System — used across every software project, regardless of
technology stack or AI vendor (Claude Code, Codex, ChatGPT, or whatever comes next).

Projects **consume** this repository. They never become part of it. The repository does not contain
the application code of projects operated through the Workbench. It may contain thin, optional,
dependency-light operational tooling for the Workbench itself (see `tools/` below). That tooling
remains non-authoritative and cannot redefine framework state, authorization, or workflow
selection — the Markdown framework remains authoritative.

The goal: sit at any machine, clone this repository alongside a project repository, launch an AI
coding assistant, and immediately work under the same methodology — regardless of project or
stack.

## Design Principles

- Modular, reusable, technology-agnostic
- Version controlled, easy to extend and maintain
- Minimal duplication, clear separation of concerns
- Composition over duplication
- Never over-engineered — no complexity without demonstrated need
- Every document has a single responsibility

## Philosophy

Capability is separated from technology.

- **Capabilities** are the constant: explore, develop, debug, review, deploy, document, learn.
  They are repeatable processes — the *what*.
- **Technologies** are the variable: Laravel, React, React Native, AWS, Docker, Python, ROS,
  networking, etc. They supply stack-specific convention — the *how, for this stack*.

A workflow (a capability) should work across multiple technologies whenever possible. Adapters
supply the stack-specific detail so workflows don't have to duplicate it per stack.

## Architecture

The repository grows in layers, populated only as real usage demands.

**Layer 0 — Foundation** (always present)
- `README.md` — this file: what the workbench is and why
- `CLAUDE.md` — how an AI agent should operate inside this repository

**Layer 1 — Structure** (created only when a folder has real content)

| Folder | Responsibility | Answers |
|---|---|---|
| `profiles/` | Behavioral roles: Explorer, Developer, Reviewer, Architect, Mentor | HOW the AI behaves |
| `workflows/` | Repeatable processes: onboarding, feature development, debugging, deployment, PR review, documentation | WHAT steps to follow |
| `standards/` | Cross-project rules: git, testing, documentation, security, architecture principles | WHAT rules always apply |
| `adapters/` | Stack-specific conventions: Laravel, React, AWS, Docker, Python, ... | WHICH detail applies for this stack (never duplicates workflow steps) |
| `templates/` | Reusable artifacts: project init, repo docs, architecture docs, PR/issue templates | WHAT to start from |
| `docs/` | Long-form reference: decision logs, architecture notes, research, learning material | WHY a decision was made |

**Layer 2 — Content**
Individual files within Layer 1 folders, added one at a time as a concrete, demonstrated need
arises — never speculatively.

**Optional Operational Tooling**

`tools/` is not one of the Markdown capability layers above. It is optional, dependency-light
tooling that helps operate the framework — reporting on framework and repository state — and is
never authoritative. The Markdown framework (Layers 0–2 above) remains the sole source of truth for
behavior, rules, and permission; `tools/` consumes and reports that state, never redefines it,
never selects a workflow, and never grants authorization. Populated only when a concrete, validated
need exists — the same discipline as every Layer 1 folder.

