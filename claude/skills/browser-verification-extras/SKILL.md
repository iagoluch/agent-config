---
name: browser-verification-extras
description: "Companion to webapp-testing and browser-testing-with-devtools. Use when live-verifying a fix in a browser against an app served as a static pre-built bundle (no HMR dev server), or when a coordinate-based click seems to do nothing, or when browser behaviour contradicts static evidence (grep on the built bundle, a passing test) that the fix landed."
---

# Browser Verification Extras

Delta rules for live browser verification. Load alongside `webapp-testing`
or `browser-testing-with-devtools`; they do not replace either.

## 1. After every rebuild, prove the browser runs the new bundle

A tab that loaded `index.html` before `npm run build` keeps executing the
old hashed bundle from memory and HTTP cache. A plain navigate or reload
does not re-fetch it.

- After each rebuild, open a fresh tab or force a hard reload
  (`location.reload(true)`, or navigate with cache disabled) before drawing
  any conclusion from what the page does.
- Confirm the running bundle, not just the file on disk: compare the
  `<script src>` hash in the live DOM with the file in the build output.
- A grep that finds the fix in the built file proves the artefact changed.
  It says nothing about which artefact the browser is executing.

## 2. Take a fresh screenshot immediately before each coordinate click

Contextual UI (a warning banner, a validation message, a toast) can shift the
layout between screenshots. A click reusing old coordinates then lands on
an adjacent control, often a disabled one, and looks exactly like an
unresponsive button.

- Never reuse coordinates from an earlier screenshot. Take a new one first,
  or click by element ref (`find` / `read_page`) instead of by pixels.
- After a click that "did nothing", screenshot again and check what is
  actually under that point before suspecting the application.

## 3. When live behaviour contradicts static evidence, suspect the harness first

If the build contains the fix but the browser shows the old behaviour, rank
these hypotheses before re-investigating application code:

1. stale bundle in the tab (rule 1);
2. layout drift under the click point (rule 2);
3. only then, a genuine defect in the fix.

Each harness check costs one action. Chasing a phantom code bug costs the
session.
