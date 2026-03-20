---
name: orient
version: 1.0.0
description: |
  Read the project handoff document and deliver a spoken briefing.
  Run this at the start of any new session to reload context without
  crawling the codebase. Pairs with /log (capture) and /brief (synthesize).
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
---

# /orient

Read `.claude/HANDOFF.md` and deliver a spoken briefing. Get fully oriented in under 2 minutes. No codebase crawling required.

## Steps

### 1. Find the project root

```bash
git rev-parse --show-toplevel 2>/dev/null || pwd
```

### 2. Read context

Try in order:
1. `{PROJECT_ROOT}/.claude/HANDOFF.md` — preferred
2. `{PROJECT_ROOT}/.claude/journal.md` — fallback if no HANDOFF exists
3. If neither exists: tell the user "No project context found. Use /log to start capturing decisions and /brief to generate a handoff document."

### 3. Deliver the briefing

Speak directly. No headers. No bullet lists. Conversational but dense. Cover:

1. **What this is** — one sentence on the product and the user it serves
2. **Where things stand** — what's built, what's not, what's next
3. **The load-bearing decisions** — say each one plainly. These are the things that would cause problems if violated.
4. **The active warnings** — the landmines. Say them clearly.
5. **Where to start** — tell me the 2-3 files I should open first if I'm about to write code

End with: "What are we working on today?"

## Tone

Sound like a senior engineer on the project who just walked back from a two-week vacation and is getting a new contractor up to speed. Confident. Specific. No fluff.

**Example opening:**
> "This is ShowStack, a React Native app for Whatnot sellers. It replaces a Google Sheets workflow for creating bulk listing CSVs. The core user is a high-volume seller doing 50-200 items per show who currently preps listings the night before by hand.
>
> Phase 1 source files are written — fee calculator, CSV generator, listing library, all four screens — but the Expo scaffold hasn't been run yet and Supabase image upload isn't wired. The CSV can't be trusted until we validate enum strings against a real Whatnot test import, which hasn't happened.
>
> The load-bearing decisions you need to know: price is never AI-inferred under any circumstances. Subcategory is required — don't make it optional. The CSV column order is fixed and must match Whatnot's import spec exactly.
>
> Start reading in csv-generator.ts, then whatnot-enums.ts. The spec files in /spec explain the fee math and the column contract.
>
> What are we working on today?"

## If HANDOFF.md is stale or missing

If HANDOFF.md exists but is more than 7 days old (check the "Last updated" line), note it:
> "Note: this handoff is from {date} — {N} days ago. Consider running /brief to refresh it before we go deep."

If only journal.md exists (no HANDOFF.md), synthesize the briefing directly from journal entries and note:
> "No HANDOFF.md found — working from the raw journal. Run /brief to generate a proper handoff document."
