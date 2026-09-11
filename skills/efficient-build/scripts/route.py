#!/usr/bin/env python3
"""Map complexity flags + uncertainty/risk to an efficient-build route."""

from __future__ import annotations

import argparse
import json
import sys

FLAG_POINTS = {
    "schema": 2,
    "auth": 2,
    "concurrency": 2,
    "unfamiliar": 2,
    "destructive": 2,
    "many_files": 1,
    "public_api": 1,
    "multiple_architectures": 1,
    "ambiguous": 1,
    "performance": 1,
    "inconsistent": 1,
    "hard_to_test": 1,
}

TIERS = ("grok-only", "grok+review", "sol-plan", "fable-plan")

AGENTS = {
    "grok-only": {
        "architect": "parent-grok",
        "reviewer": None,
        "route": "grok implement",
    },
    "grok+review": {
        "architect": "parent-grok",
        "reviewer": "frontier-reviewer",
        "route": "grok plan+implement → sol review",
    },
    "sol-plan": {
        "architect": "frontier-architect",
        "reviewer": "frontier-reviewer",
        "route": "sol plan → grok implement → sol review",
    },
    "fable-plan": {
        "architect": "frontier-escalation",
        "reviewer": "frontier-reviewer",
        "route": "fable plan → grok implement → sol review",
    },
}


def complexity_from_flags(flags: list[str]) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    seen: set[str] = set()
    for raw in flags:
        flag = raw.strip().lower().replace("-", "_")
        if not flag or flag in seen:
            continue
        seen.add(flag)
        pts = FLAG_POINTS.get(flag)
        if pts is None:
            raise SystemExit(
                f"unknown flag {raw!r}; expected one of: {', '.join(FLAG_POINTS)}"
            )
        score += pts
        reasons.append(f"{flag} +{pts}")
    return score, reasons


def base_tier(complexity: int) -> str:
    if complexity <= 2:
        return "grok-only"
    if complexity <= 5:
        return "grok+review"
    if complexity <= 8:
        return "sol-plan"
    return "fable-plan"


def bump(tier: str, steps: int) -> str:
    idx = min(len(TIERS) - 1, TIERS.index(tier) + steps)
    return TIERS[idx]


def route(complexity: int, uncertainty: int, risk: int) -> tuple[str, list[str]]:
    notes: list[str] = []
    tier = base_tier(complexity)
    notes.append(f"base from complexity {complexity} → {tier}")

    if uncertainty >= 9 and risk >= 8:
        if tier != "fable-plan":
            notes.append("force fable-plan (uncertainty≥9 and risk≥8)")
        return "fable-plan", notes
    if uncertainty >= 8 and risk >= 8 and complexity >= 6:
        if tier != "fable-plan":
            notes.append(
                "force fable-plan (uncertainty≥8, risk≥8, complexity≥6)"
            )
        return "fable-plan", notes

    if uncertainty >= 8 or risk >= 8:
        bumped = bump(tier, 1)
        if bumped != tier:
            why = []
            if uncertainty >= 8:
                why.append(f"uncertainty={uncertainty}")
            if risk >= 8:
                why.append(f"risk={risk}")
            notes.append(f"bump one tier ({', '.join(why)}) → {bumped}")
        return bumped, notes

    return tier, notes


def parse_flags(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [part for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--uncertainty", type=int, required=True, metavar="1-10")
    parser.add_argument("--risk", type=int, required=True, metavar="1-10")
    parser.add_argument(
        "--flags",
        default="",
        help="comma-separated flags (see router.md)",
    )
    parser.add_argument(
        "--complexity",
        type=int,
        help="override summed flag score",
    )
    parser.add_argument(
        "--force-tier",
        choices=TIERS,
        help="user override; skips scoring",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    for label, value in (("uncertainty", args.uncertainty), ("risk", args.risk)):
        if not 1 <= value <= 10:
            raise SystemExit(f"{label} must be 1–10, got {value}")

    flags = parse_flags(args.flags)
    flag_score, reasons = complexity_from_flags(flags)
    complexity = args.complexity if args.complexity is not None else flag_score
    if complexity < 0:
        raise SystemExit("complexity must be >= 0")

    if args.force_tier:
        tier = args.force_tier
        notes = [f"forced by user → {tier}"]
    else:
        tier, notes = route(complexity, args.uncertainty, args.risk)

    payload = {
        "complexity_score": complexity,
        "uncertainty": args.uncertainty,
        "risk": args.risk,
        "flags": flags,
        "reasons": reasons,
        "notes": notes,
        "tier": tier,
        **AGENTS[tier],
    }

    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    print(f"complexity_score: {payload['complexity_score']}")
    print(f"uncertainty: {payload['uncertainty']}")
    print(f"risk: {payload['risk']}")
    print("reasons:")
    if reasons:
        for line in reasons:
            print(f"- {line}")
    else:
        print("- (no flags)")
    print("notes:")
    for line in notes:
        print(f"- {line}")
    print(f"tier: {tier}")
    print(f"route: {payload['route']}")
    print(f"architect_agent: {payload['architect']}")
    print(f"reviewer_agent: {payload['reviewer'] or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
