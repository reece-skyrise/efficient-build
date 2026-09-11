# efficient-build

A Cursor workflow that spends Grok on gathering and implementation, and Sol / Fable only on decisions.

Grok (parent) explores, compiles a Task Capsule, implements, and tests. Sol High plans most non-trivial work and reviews the raw diff. Fable High plans only high-uncertainty / high-risk work. Frontier agents are **closed-world**: they never read the repo; Grok passes a self-contained packet.

## Install

From this repo:

```bash
./install.sh
```

That symlinks:

- `skills/efficient-build` → `~/.cursor/skills/efficient-build`
- `agents/*.md` → `~/.cursor/agents/`

## Invoke

In Agent chat, model **Grok 4.6 High**:

```
/efficient-build

<the task>
```

Keep it on for a session with Option+Enter (Mac) / Alt+Enter (Windows) after selecting the skill.

User overrides: `grok only`, `skip review`, `use fable`.
