# 🐾 OpenClaw Code Agent Bootstrap

This is the target repository workspace for OpenClaw Code Agent (goldmar/openclaw-code-agent).

## On First Run (Self-Merge)

1. Read any provided `_soul_source.md`, `_user_source.md`, `_agent_source.md` or similar bootstrap sources.
2. Merge relevant identity/context into:
   - `SOUL.md`
   - `IDENTITY.md`
   - `USER.md`
   - `AGENTS.md`
3. Review and adopt skills from the `skills/` directory or referenced sources.
4. Initialize or update the codebase structure for the project this repo represents.
5. Delete this `BOOTSTRAP.md` (and any `_*_source.md` files) after successful merge.

## Purpose

This workspace serves as the primary repo for:
- Code understanding / ingestion pipeline
- Long-running coding sessions launched via the `openclaw-code-agent` plugin
- Worktree-based development with plan/review/execute flow

## Plugin

Requires `openclaw-code-agent` (goldmar) enabled.

Launch coding work from chat with instructions like:
- "Use oca to implement..."
- "Let the code agent review and fix..."

## Current Status

- Plugin: installed + enabled
- Workspace git: initialized
- This file: present for agent self-bootstrapping

After bootstrap, remove this file.
