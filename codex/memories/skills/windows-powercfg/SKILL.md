---
name: windows-powercfg
description: Configure or verify a Windows power plan, Ultimate Performance, or requests to keep the screen/notebook active.
argument-hint: "[activate-ultimate|disable-timeouts|verify]"
disable-model-invocation: true
allowed-tools: [Bash]
---

# Windows powercfg

## When to use

Use for a request to activate “Desempenho Máximo”/Ultimate Performance, disable screen/sleep/hibernate/disk timers, or verify those settings. Do not use this to change lid-close behavior without explicit confirmation.

## Inputs / context

1. Confirm whether the request is plan activation, timeout changes, or verification.
2. Read the active scheme and available schemes: `powercfg /getactivescheme; powercfg /list`.
3. Treat returned GUIDs and the current active plan as host-specific observations.

## Procedure

1. For Ultimate Performance when absent, run `powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61`, capture the returned GUID, then run `powercfg /setactive <GUID>`.
2. For “always active” requests, set each automatic timeout for both AC and DC to never:
   - `powercfg /change monitor-timeout-ac 0` and `powercfg /change monitor-timeout-dc 0`
   - `powercfg /change standby-timeout-ac 0` and `powercfg /change standby-timeout-dc 0`
   - `powercfg /change hibernate-timeout-ac 0` and `powercfg /change hibernate-timeout-dc 0`
   - `powercfg /change disk-timeout-ac 0` and `powercfg /change disk-timeout-dc 0`
3. Do not change the lid-close action unless the user separately authorizes it.

## Efficiency plan

- Run the discovery commands once before modifying and once after modifying.
- For timeout validation, query all four aliases in a single command chain. Stop after the selected setting is confirmed; do not alter unrelated power policies.

## Pitfalls and fixes

- Missing Ultimate Performance: duplicate the native template rather than treating it as an error.
- “Always active” does not override manual shutdown/restart/sleep/hibernate or lid-close policy. State these limits.
- Lid-close changes can create thermal risk when the laptop is in a bag; require confirmation.

## Verification checklist

- `powercfg /getactivescheme` and `powercfg /list` show the intended active `*` scheme when a plan was changed.
- `powercfg /query SCHEME_CURRENT SUB_VIDEO VIDEOIDLE`, `SUB_SLEEP STANDBYIDLE`, `SUB_SLEEP HIBERNATEIDLE`, and `SUB_DISK DISKIDLE` show AC/DC `0x00000000` when timeouts were disabled.
- Report the exact verified settings and manual/lid-close exceptions.
