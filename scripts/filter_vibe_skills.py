#!/usr/bin/env python3
"""
Step 2: Filter vibe-related skills from catalog for deep evaluation.
Reads docs/skill-catalog-index.json, selects relevant skills, outputs filtered list.
"""

import json
import sys
from pathlib import Path

CATALOG_PATH = Path(__file__).parent.parent / "docs" / "skill-catalog-index.json"
OUTPUT_PATH = Path(__file__).parent.parent / "docs" / "vibe-filtered-skills.json"

VIBE_KEYWORDS = [
    "vibe", "coding", "code", "environment", "agent", "orchestrator",
    "mcp", "n8n", "dev", "debug", "engineering", "bridge", "dot"
]

EXCLUDE_KEYWORDS = [
    "prospecting", "facebook", "poster", "demo"
]

def score_relevance(name: str, summary: str, family: str) -> int:
    """Score 0-100 for vibe coder environment relevance."""
    text = f"{name} {summary} {family}".lower()
    score = 0
    for kw in VIBE_KEYWORDS:
        if kw in text:
            score += 10
    for kw in EXCLUDE_KEYWORDS:
        if kw in text:
            score -= 20
    # Boost code-plugin family
    if family == "code-plugin":
        score += 15
    # Boost high downloads
    return max(0, min(100, score))

def main():
    with open(CATALOG_PATH) as f:
        catalog = json.load(f)

    filtered = []

    # Process community plugins
    for key, plugin in catalog.get("communityPluginsFromSearch", {}).items():
        relevance = score_relevance(key, plugin.get("summary", ""), plugin.get("family", ""))
        if relevance > 20:  # threshold
            filtered.append({
                "key": key,
                "displayName": plugin.get("displayName"),
                "family": plugin.get("family"),
                "channel": plugin.get("channel"),
                "summary": plugin.get("summary"),
                "latestVersion": plugin.get("latestVersion"),
                "runtimeId": plugin.get("runtimeId"),
                "downloads": plugin.get("downloads", 0),
                "verificationTier": plugin.get("verificationTier"),
                "relevanceScore": relevance
            })

    # Sort by relevance desc, then downloads desc
    filtered.sort(key=lambda x: (-x["relevanceScore"], -x["downloads"]))

    result = {
        "filteredAt": "2026-10-03T05:55:00-04:00",
        "totalCandidates": len(catalog.get("communityPluginsFromSearch", {})),
        "filteredCount": len(filtered),
        "skills": filtered
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Filtered {len(filtered)} skills from {result['totalCandidates']} candidates")
    for s in filtered:
        print(f"  {s['key']}: relevance={s['relevanceScore']}, downloads={s['downloads']}, tier={s['verificationTier']}")

    return 0

if __name__ == "__main__":
    sys.exit(main())