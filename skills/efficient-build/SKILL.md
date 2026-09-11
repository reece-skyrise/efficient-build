---
name: efficient-build
description: Cost-efficient coding workflow. Grok gathers and implements; Sol or Fable only decide. Invoke with /efficient-build.
disable-model-invocation: true
icon: rocket
color: purple
---

# Efficient build

You are the **worker and orchestrator**. Spend frontier tokens only on decisions.

Parent chat model should be **Grok 4.6 High**. If this session is already Sol, Fable, or Opus, say so in one line and continue — those tokens are already leaking.

User overrides win: `grok only`, `skip review`, `use fable`.

Read [router.md](router.md), [capsule.md](capsule.md), and [review-packet.md](review-packet.md) before the first specialist call. Model IDs: [models.md](models.md).

## Closed world (non-negotiable)

Sol and Fable are **blind**. They must not read the repo, search, grep, open files, run `git`, run tests, or use Explore/Browser/MCP. Every token they spend on gathering is a failure of this workflow.

You (Grok) do all token-churning work: codebase reads, search, diffs, tests, logs. You synthesise a **self-contained packet** and pass that. The API model’s entire world is the packet.

- If a decision depends on code, **paste the lines**. A `path:line` the specialist cannot open is useless.
- Never tell a specialist to “check the repo”, “read the file”, or “run git diff”.
- Prefix every specialist prompt with: `CLOSED WORLD. Do not use tools. The packet below is your entire context. If a fact is missing, output GAPS and stop.`
- If they return `GAPS`: you fetch those facts, update the packet, re-invoke **once**. Do not grant repo access.
- If they use tools anyway: ignore anything they fetched; keep only their decisions; do not send them back to explore.

Independence is preserved by passing **primary evidence** (verbatim snippets, raw diff hunks), not your commentary on that evidence.

## 1. Score, then route

After cheap exploration (not before), score **complexity / uncertainty / risk**.

Run:

```bash
python3 ~/.cursor/skills/efficient-build/scripts/route.py \
  --uncertainty N --risk N --flags flag,flag
```

Print the script output. That **route** is the contract for this run.

Do not ask the user to confirm unless the architect is Fable. Then one line: the score, the reasons, and that Fable will plan.

## 2. Compile a Task Capsule

Use Explore / search / file reads. Do not send frontier agents to explore.

Build the capsule from [capsule.md](capsule.md). Target **1–3k tokens**. Self-contained: the architect will not open any path you name.

Leave UNCERTAINTIES actually open. Do not smuggle your preferred design in as if it were current architecture. Freeze the capsule after this step; the architect may still overturn the implied approach.

Completion: every acceptance criterion is testable, every unresolved decision is listed, and the capsule does not contain exploration narration.

## 3. Plan

| Route | Who plans |
| --- | --- |
| `grok-only` / `grok+review` | You. Short plan. No specialist. |
| `sol-plan` | Task `frontier-architect` |
| `fable-plan` | Task `frontier-escalation` |

Specialist prompt: closed-world line + the **Task Capsule** as a briefing, not a verdict + the route line. No transcript. No “see also these files”. No tool use.

Do **not** set Task `model` — the agent's frontmatter pins it. Foreground only.

If the named subagent type is missing: Sol → `generalPurpose` with `model: gpt-5.6-sol-high` and the same closed-world + packet prompt. Fable → say the escalation agent was not loaded and **downgrade to Sol**; do not invent a Fable Task slug.

Treat the returned plan as the implementation contract, **including when it contradicts the capsule**. Specialists are hired to disagree. Do not round their pushback back into your first idea. If they call the approach wrong, timid, or basic, implement theirs unless it violates an invariant or an explicit user constraint. One line to the user when you accepted a better plan.

Do not re-plan unless a reviewer finds a **fundamental** architectural flaw — and if they do, that is a real re-plan, not a nit to absorb.

## 4. Implement

You implement. Do not spawn an implementer subagent.

Frontier agents are forbidden for: edits, ordinary debug, tests, format, lint, obvious local decisions.

Validate (targeted tests, then broader checks the repo already uses).

Completion: the plan's validation items have been run, or you recorded why a check cannot run.

## 5. Review

Skip on `grok-only`.

Otherwise you run `git diff` / tests yourself and Task `frontier-reviewer` with a [review packet](review-packet.md):

- closed-world line
- Task Capsule
- approved plan
- **raw** `git diff --stat` plus the verbatim hunks (not a prose summary of the change)
- concise validation results (commands + pass/fail, not full logs)

If `PASS`: stop.

If findings: apply **blocker** and **important** yourself; skip **minor** unless trivial. If they reject the *approach* (timid, wrong shape, local-maximum), that is a fundamental flaw — re-plan with the specialist, do not patch around it. Otherwise re-test and re-review with **only**: capsule, plan, previous findings, **repair delta**, new validation. Max two repair loops unless blockers remain.

## Hard rules

- API models never gather. Grok gathers; API models decide.
- The router is cheap. You never spend Fable tokens deciding whether to spend Fable tokens.
- Freeze capsule facts after the first architecture pass; the specialist may still overturn the approach.
- Do not flatten specialist pushback into your original idea.
- Re-review the **delta**, not the whole pipeline.
- Independent review needs the **raw diff**, not your interpretation of the diff — and Grok is the one who produced that diff.
