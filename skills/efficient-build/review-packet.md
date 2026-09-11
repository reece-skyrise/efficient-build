# Review packet

You (Grok) produce this after implementation. The reviewer is **blind** — it will not run `git` or open files.

Independence: include the **verbatim diff**, not a narrative of what you think you changed. Do not write “this correctly implements X”.

Budget: keep it tight. Omit lockfiles, generated assets, formatting-only noise. If the diff is large, include `--stat` plus full hunks for the planned/behavior files, not a summary.

```
TASK CAPSULE
<frozen capsule>

PLAN
<approved plan>

DIFF STAT
<verbatim git diff --stat>

DIFF
<verbatim git diff hunks — worker-produced, not paraphrased>

VALIDATION
- command → pass/fail
- relevant assertion names only; no full logs
```

Re-review packet: capsule + plan + previous findings + **repair delta only** + new validation. Same closed-world rule.
