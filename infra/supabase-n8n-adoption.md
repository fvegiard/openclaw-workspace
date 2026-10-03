# Supabase + n8n Adoption Plan for OpenClaw Agents (Amanda)

**Date**: 2026-06-20
**Decision**: Adopt Supabase as primary persistent backend + n8n as workflow orchestrator.

## Why (from GitHub + docs research)
- Supabase: Real Postgres + Realtime + Auth + Storage + pgvector. Perfect for agent memory, todos, state, cross-device sync (MacBook node, this machine).
- n8n: Open-source workflow engine with native Supabase node. Handles webhooks, scheduling, agent handoffs, data pipelines, notifications. Self-hostable via Docker or npm.

## Current Setup (Proto-backed)
- Node 26 via proto
- Python 3.14 (no-GIL) via proto
- uv latest via proto

## Adoption Plan (Real Actions)
1. Use Supabase for:
   - Agent state (todos, memory, cache)
   - Project data (estimates, jobs)
   - Logs and verification evidence

2. Use n8n for:
   - Triggering agent runs (e.g., cron-like)
   - MacBook Codex dispatch workflows
   - Data sync between Supabase <-> Google Drive <-> local
   - Notifications (WhatsApp via OpenClaw bridge)

## Next Concrete Steps
- Install n8n (Docker recommended per official docs)
- Create Supabase project (or use existing Pro)
- Build first workflow: "MacBook Node Health Check → Supabase → n8n → Alert"
- Update agents/workers/runner.js to optionally persist to Supabase
- Use uv for Python n8n client scripts if needed

## GitHub Sources Used
- n8n official hosting docs
- Multiple Supabase + n8n integration repos (JimPresting, kossakovsky/n8n-install, coleam00/ai-agents-masterclass, etc.)

This replaces pure local file state with production-grade infra.
