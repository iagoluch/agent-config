---
name: ""
metadata:
  node_type: memory
  id: verify-subagent-factual-claims
  title: "Verify a subagent's \"dead code\" / factual claims before auto-applying a fix based on them"
  status: open
  skill: "(cross-cutting, no specific skill)"
  session_context: "Auditoria completa 23/09/2026, Gestor de Peças (goal de longo prazo)"
  date: 2026-09-23
  originSessionId: 4f869c5b-eb66-473e-98db-73bf6598e807
  modified: 2026-09-23T04:37:50.256Z
---

## Observation

A background audit subagent (backend/domain audit) reported finding #10 as
"dead code": `_JanelaPrefetch.agora` stored as `self._agora`, claimed
"never read anywhere." Before applying the proposed fix (which the agent
judged "safe, zero-behavior-change"), I independently grepped the codebase
and found `self._agora` IS read at two call sites in
`mes/services/management.py` (lines 953, 1021) as a fallback "now" for
still-open records. The claim was wrong.

Had I trusted the subagent's claim and applied the fix, it would have
silently changed OEE/analytics-adjacent behavior (switching from an
injectable clock reference used as a fallback to genuinely dead code
removal that wasn't actually dead) — directly violating a hard user
constraint on this task ("nunca altere a lógica existente").

## Why this generalizes

Subagent reports (especially "dead code" / "unused" / "safe to remove"
claims) are software-engineering *hypotheses*, not verified facts, even
when phrased with confidence. This is exactly the class of claim that is
cheap to verify (one grep) and expensive to get wrong (silent behavior
change, possibly in analytics/OEE-affecting code). This applies to any
project, not just this one, and to any subagent-delegated audit/refactor
task — not specific to this skill.

## Suggested rule

Before auto-applying ANY fix a subagent proposes as "safe / zero-behavior
-change / dead code", independently verify the specific factual claim
underlying that judgment (grep for all usages, not just the ones the
subagent cited) — do not propagate the subagent's confidence without
re-deriving it. If verification contradicts the claim, reclassify the
finding as needing explicit user confirmation rather than silently
correcting and moving on.
