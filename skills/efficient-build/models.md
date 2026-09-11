# Model pins

Unquoted IDs. Cursor's agent loader treats quotes as part of the name and silently falls back to the parent model.

| Role | Agent file | `model` |
| --- | --- | --- |
| Worker / parent | (chat picker) | Cursor Grok 4.6 High |
| Default architect | `~/.cursor/agents/frontier-architect.md` | `gpt-5.6-sol[effort=high]` |
| Escalation architect | `~/.cursor/agents/frontier-escalation.md` | `claude-fable-5-1[effort=high]` |
| Reviewer | `~/.cursor/agents/frontier-reviewer.md` | `gpt-5.6-sol[effort=high]` |

If a pin is rejected (plan, admin, or Fable data-retention opt-in), the orchestrator downgrades **one rung** and says so: Fable → Sol → Grok.

Fable 5.1 may require Anthropic data-retention approval when Privacy Mode is on. Sol is then the frontier specialist.

Do not pass Task `model` when invoking these named agents. Their frontmatter is the pin.

Emergency Sol-only fallback (named agent missing): Task `generalPurpose` with `model: gpt-5.6-sol-high` and the **closed-world packet prompt**. There is no equivalent Fable slug on the Task allow-list — missing `frontier-escalation` means Sol, not a guessed Fable ID.

Cursor subagents cannot strip read tools. Blindness is enforced by the packet + `CLOSED WORLD. Do not use tools.` — not by `readonly: true` (that only blocks writes).
