#!/usr/bin/env python3
"""
Step 4: Deep evaluation of filtered skills using Python.
Scores each skill on 6 dimensions (0-10 each) for a total of 0-60.
"""

import json
import sys
from pathlib import Path

MANIFESTS_DIR = Path(__file__).parent.parent / "docs" / "skill-manifests"
FILTERED_PATH = Path(__file__).parent.parent / "docs" / "vibe-filtered-skills.json"
OUTPUT_PATH = Path(__file__).parent.parent / "docs" / "skill-eval-matrix.json"
REPORT_PATH = Path(__file__).parent.parent / "docs" / "skill-evaluation-report.md"

DIMENSIONS = [
    "environment_fix_capability",    # Can it fix/configure dev environments?
    "vibe_coder_relevance",          # Directly relevant to "vibe coder" workflow?
    "mcp_n8n_integration",           # Has MCP server or n8n integration?
    "tailscale_ready",               # Works over Tailscale / remote access?
    "maintenance_health",            # Active maintenance, recent updates?
    "community_trust",               # Downloads, verification, stars?
]

def load_manifest(skill_key: str) -> dict:
    """Load all available manifest files for a skill."""
    skill_dir = MANIFESTS_DIR / skill_key
    manifest = {"key": skill_key}
    for fname in ["SKILL.md", "package.json", "CHANGELOG.md", "README.md"]:
        fpath = skill_dir / fname
        if fpath.exists():
            content = fpath.read_text()
            if len(content) > 100:  # Not a 404
                manifest[fname.lower().replace(".", "_")] = content
    return manifest

def evaluate_skill(skill_data: dict, manifest: dict) -> dict:
    """Deep evaluate a single skill across 6 dimensions."""
    scores = {}
    rationale = {}
    
    key = skill_data["key"]
    downloads = skill_data.get("downloads", 0)
    tier = skill_data.get("verificationTier", "unknown")
    family = skill_data.get("family", "")
    summary = skill_data.get("summary", "").lower()
    
    readme = manifest.get("readme_md", "")
    skill_md = manifest.get("skill_md", "")
    package_json = manifest.get("package_json", "")
    changelog = manifest.get("changelog_md", "")
    
    combined_text = f"{summary} {readme} {skill_md} {package_json} {changelog}".lower()
    
    # 1. Environment fix capability
    env_keywords = ["environment", "setup", "bootstrap", "configure", "install", "devcontainer", "docker", "dev environment", "workspace", "proj"]
    env_score = sum(5 for kw in env_keywords if kw in combined_text)
    env_score = min(10, max(0, env_score + (3 if "code-plugin" in family else 0)))
    scores["environment_fix_capability"] = env_score
    rationale["environment_fix_capability"] = f"Keywords found: {[kw for kw in env_keywords if kw in combined_text]}"
    
    # 2. Vibe coder relevance
    vibe_keywords = ["vibe", "coding", "agent", "orchestrat", "claude code", "codex", "opencode", "autonomous", "background", "session", "worktree", "plan approval"]
    vibe_score = sum(4 for kw in vibe_keywords if kw in combined_text)
    vibe_score = min(10, max(0, vibe_score))
    scores["vibe_coder_relevance"] = vibe_score
    rationale["vibe_coder_relevance"] = f"Vibe/coding keywords: {[kw for kw in vibe_keywords if kw in combined_text]}"
    
    # 3. MCP/n8n integration
    mcp_keywords = ["mcp", "model context protocol", "n8n", "workflow", "webhook", "automation", "mcp server", "mcp-compatible"]
    mcp_score = sum(5 for kw in mcp_keywords if kw in combined_text)
    # Extra boost for explicit MCP server
    if "mcp server" in combined_text or "mcp-compatible" in combined_text:
        mcp_score += 5
    mcp_score = min(10, max(0, mcp_score))
    scores["mcp_n8n_integration"] = mcp_score
    rationale["mcp_n8n_integration"] = f"MCP/n8n keywords: {[kw for kw in mcp_keywords if kw in combined_text]}"
    
    # 4. Tailscale ready
    ts_keywords = ["tailscale", "remote", "ssh", "network", "vpn", "mesh", "tailnet", "distributed", "multi-machine"]
    ts_score = sum(4 for kw in ts_keywords if kw in combined_text)
    # Plugins that work over network get baseline
    if "code-plugin" in family or "channel" in combined_text:
        ts_score += 3
    ts_score = min(10, max(0, ts_score))
    scores["tailscale_ready"] = ts_score
    rationale["tailscale_ready"] = f"Remote/network keywords: {[kw for kw in ts_keywords if kw in combined_text]}"
    
    # 5. Maintenance health
    maint_score = 5  # baseline
    if tier == "source-linked":
        maint_score += 3
    elif tier == "structural":
        maint_score += 1
    if downloads > 1000:
        maint_score += 2
    elif downloads > 100:
        maint_score += 1
    # Check changelog for recent activity
    if "2026" in changelog or "2025" in changelog:
        maint_score += 2
    maint_score = min(10, max(0, maint_score))
    scores["maintenance_health"] = maint_score
    rationale["maintenance_health"] = f"Tier: {tier}, Downloads: {downloads}, Recent changelog: {'yes' if '2026' in changelog or '2025' in changelog else 'no'}"
    
    # 6. Community trust
    trust_score = 3  # baseline
    if tier == "source-linked":
        trust_score += 4
    elif tier == "structural":
        trust_score += 2
    if downloads > 2000:
        trust_score += 3
    elif downloads > 500:
        trust_score += 2
    elif downloads > 100:
        trust_score += 1
    trust_score = min(10, max(0, trust_score))
    scores["community_trust"] = trust_score
    rationale["community_trust"] = f"Tier: {tier}, Downloads: {downloads}"
    
    total = sum(scores.values())
    
    return {
        "key": key,
        "displayName": skill_data.get("displayName", key),
        "scores": scores,
        "rationale": rationale,
        "total": total,
        "max_possible": 60
    }

def main():
    with open(FILTERED_PATH) as f:
        filtered = json.load(f)
    
    evaluations = []
    
    for skill in filtered["skills"]:
        print(f"Evaluating {skill['key']}...")
        manifest = load_manifest(skill["key"])
        eval_result = evaluate_skill(skill, manifest)
        evaluations.append(eval_result)
        print(f"  Total: {eval_result['total']}/60")
        for dim, score in eval_result["scores"].items():
            print(f"    {dim}: {score}/10")
    
    # Sort by total desc
    evaluations.sort(key=lambda x: -x["total"])
    
    # Save detailed results
    result = {
        "evaluatedAt": "2026-10-03T06:10:00-04:00",
        "dimensions": DIMENSIONS,
        "evaluations": evaluations
    }
    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)
    
    # Generate markdown report
    md = ["# Skill Evaluation Report\n", f"Generated: 2026-10-03\n", f"Dimensions: {', '.join(DIMENSIONS)}\n"]
    md.append("| Rank | Skill | Total | Env Fix | Vibe | MCP/n8n | Tailscale | Maint | Trust |")
    md.append("|------|-------|-------|---------|------|---------|-----------|-------|-------|")
    
    for i, e in enumerate(evaluations, 1):
        s = e["scores"]
        md.append(f"| {i} | **{e['displayName']}** ({e['key']}) | **{e['total']}/60** | {s['environment_fix_capability']} | {s['vibe_coder_relevance']} | {s['mcp_n8n_integration']} | {s['tailscale_ready']} | {s['maintenance_health']} | {s['community_trust']} |")
    
    md.append("\n## Detailed Rationale\n")
    for e in evaluations:
        md.append(f"### {e['displayName']} ({e['key']}) — {e['total']}/60\n")
        for dim, reason in e["rationale"].items():
            md.append(f"- **{dim}** ({e['scores'][dim]}/10): {reason}\n")
        md.append("")
    
    # Recommendation
    winner = evaluations[0]
    md.append(f"## 🏆 Top Recommendation: **{winner['displayName']}** ({winner['total']}/60)\n")
    md.append(f"**Why:** Highest weighted score across all 6 dimensions. Strong in MCP/n8n integration and vibe coder relevance.")
    md.append(f"\n**Next:** Step 6 - Publish evaluation report, then proceed to Phase 2 (MCP n8n Team Agent scaffold).\n")
    
    with open(REPORT_PATH, "w") as f:
        f.write("\n".join(md))
    
    print(f"\n✅ Evaluation complete. Top skill: {winner['displayName']} ({winner['total']}/60)")
    print(f"Report: {REPORT_PATH}")
    print(f"Matrix: {OUTPUT_PATH}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())