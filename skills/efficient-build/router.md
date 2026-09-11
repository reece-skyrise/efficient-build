# Router

Frontier reasoning is triggered by **uncertainty** and **risk**, not task size.

## Flags → complexity

Start at 0. Sum matching flags. Pass them to `scripts/route.py`.

| Flag | Pts | Use when |
| --- | ---: | --- |
| `schema` | 2 | Schema change or migration |
| `auth` | 2 | Auth, permissions, security boundary |
| `concurrency` | 2 | Races, distributed, locks, queues |
| `unfamiliar` | 2 | Subsystem you have not mapped this session |
| `destructive` | 2 | Prod infra, data loss, irreversible ops |
| `many_files` | 1 | More than 5 meaningful files |
| `public_api` | 1 | Public / shared interface changes |
| `multiple_architectures` | 1 | Several plausible designs |
| `ambiguous` | 1 | Requirements underspecified |
| `performance` | 1 | Material perf implications |
| `inconsistent` | 1 | Existing impl already disagrees with itself |
| `hard_to_test` | 1 | Behaviour is difficult to validate |

## Uncertainty and risk (1–10)

**Uncertainty** — how hard is it to know the *correct* change?

**Risk** — how bad if we are wrong?

| | C (size) | U | R |
| --- | ---: | ---: | ---: |
| CSS / copy tweak | 1 | 1 | 1 |
| Typical CRUD endpoint | 3 | 2 | 2 |
| DB migration, well-known pipeline | 4 | 3 | 7 |
| Rare race condition, tiny diff | 2 | 9 | 8 |
| Auth rewrite | 7 | 7 | 9 |

A large, obvious change can stay off Fable. A tiny, high-entropy change should escalate.

## Tiers

Computed by `scripts/route.py`:

| Tier | Architect | Implement | Review |
| --- | --- | --- | --- |
| `grok-only` | Grok (you) | Grok | none |
| `grok+review` | Grok (you) | Grok | `frontier-reviewer` (Sol) |
| `sol-plan` | `frontier-architect` (Sol) | Grok | `frontier-reviewer` (Sol) |
| `fable-plan` | `frontier-escalation` (Fable) | Grok | `frontier-reviewer` (Sol) |

Reviewer is **Sol**, not the architect. Diversity is cheaper than Fable reviewing Fable, and catches self-agreement.

Bump one tier (cap `fable-plan`) if `uncertainty >= 8` or `risk >= 8`.

Force `fable-plan` if `(uncertainty >= 9 and risk >= 8)` or `(uncertainty >= 8 and risk >= 8 and complexity >= 6)`.

Base from complexity only: 0–2 `grok-only`, 3–5 `grok+review`, 6–8 `sol-plan`, 9+ `fable-plan`.
