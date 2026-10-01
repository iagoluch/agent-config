---
id: 1
title: "Static pre-built frontend bundle + browser HTTP cache can masquerade as a code bug during live verification"
status: actioned
type: open-source
skill: [webapp-testing, browser-testing-with-devtools, debugging-and-error-recovery]
proposes_skill: []
target_file: []
siblings_checked: "none — no skill-families.md registry exists yet in this workspace"
area: "browser-based live verification of a rebuilt frontend"
date: 2026-09-24
session_context: "Verifying two authorized bug fixes (a Setup confirmation dialog and a Pausas Desativar/Remover confirmation) in a React SPA served as a static pre-built bundle (no HMR/dev-server) via FastAPI's SpaStaticFiles. After confirming via grep that the rebuilt bundle contained the fix's source text, live browser testing kept showing the OLD pre-fix behavior, which was initially treated as evidence the fix had not actually taken effect."
resolved: 2026-09-29
resolution: "Staged for browser-verification-extras at skill-updates/2026-09-29/browser-verification-extras (weekly review); rota companion escolhida pelo usuário para webapp-testing, browser-testing-with-devtools e debugging-and-error-recovery (cópias de pacote, voláteis)"
reference:
---

**Issue:** Two independent factors compounded into what looked like a code bug but was not: (1) a browser tab that had already loaded `index.html` before a rebuild keeps executing the old JS bundle from its own HTTP cache/memory even after `npm run build` produces a new hashed bundle on disk — a plain navigate or reload does not force a re-fetch of `index.html`, only a true hard reload (`location.reload(true)`) or a fresh tab does; and (2) test clicks were issued using pixel coordinates carried over from an earlier screenshot, before a contextual warning banner had pushed the action-button row down, so clicks intended for one button silently landed on an adjacent disabled button, producing "nothing happened" that was misread as further evidence of a bug. Confirming the bundle's source text was present (via grep on the built file) was necessary but not sufficient to prove the *browser* was running that bundle. Significant investigation time was spent chasing a phantom code bug before both factors were identified together.

**Suggested improvement:** When verifying a fix against an app served as a static pre-built bundle (no hot-reload dev server): after any rebuild, always force a true hard reload or open a fresh tab before drawing any conclusion from browser behavior — do not trust that a normal navigate/reload picked up the new bundle. Separately, before any coordinate-based click, take a screenshot immediately beforehand (never reuse coordinates from an earlier screenshot) — an unexpected banner, error message, or contextual UI element that changes vertical layout can silently misdirect a click to the wrong control, which then looks exactly like an unresponsive button or a missing feature. When live-testing behavior contradicts static evidence (e.g., grep confirming the fix is in the built file), treat cache/staleness of the *test harness itself* (browser tab, click coordinates) as a leading hypothesis before concluding the fix is broken.

**Principle:** Static evidence that a fix landed in a build artifact (grep on the bundle, a passing unit test) does not prove a live browser session is executing that artifact. Any live verification loop against a non-hot-reloading server needs its own cache-invalidation discipline (hard reload / fresh tab per rebuild) and its own layout-drift discipline (fresh screenshot immediately before each coordinate-based interaction) — treating these as leading hypotheses saves significant time versus re-investigating the application code first when live behavior seems to contradict a verified fix.
