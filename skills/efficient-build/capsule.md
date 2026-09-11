# Task Capsule

Decision-complete context. Not a lossless dump of exploration.

The recipient **cannot open the repository**. Every claim they must rely on has to be in this packet.

Budget: **~1–3k tokens**. Name `path:symbol` / `file:line` **and paste the few lines that are the evidence**. A bare path is a dangling pointer.

```
TASK
<one sentence>

ACCEPTANCE CRITERIA
- <observable, testable>

CURRENT ARCHITECTURE
- <how the relevant request/data currently flows>
- <existing types / modules that own this>

RELEVANT FILES
- path — why

INVARIANTS
- <must not break>
- <API / transactional / compatibility constraints>

KNOWN PROJECT CONVENTIONS
- <only those that bind this change>

OBSERVATIONS / EVIDENCE
- path:line — factual
- tests covering A/B but not C

UNCERTAINTIES
- <decisions the architect must own — options, not your chosen plan>
```

Omit empty sections. Do not include: search traces, rejected files, conversation recap, "I looked at…".

Do not smuggle a preferred design into CURRENT ARCHITECTURE or OBSERVATIONS. Evidence is fact; the approach is theirs.

The frontier model needs constraints, evidence, and decision points. It does not need 90% of what Explore saw, and it must not be sent to fetch the rest.
