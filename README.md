# project-journal

Three Claude Code skills for keeping context alive across sessions.

The problem: load-bearing decisions get made in conversation and disappear by the next session. Crawling the codebase to reconstruct context wastes 20 minutes and still misses the *why*. This solves it.

---

## The three skills

### `/log` — capture in the moment

```
/log decision "Price is never AI-inferred — non-negotiable"
/log warning "CSV enum strings not yet validated against live import"
/log state "Phase 1 source files written, scaffold not yet run"
/log discovery "Whatnot requires integer prices — no cents in CSV"
/log todo "Add camera permissions request before image picker"
/log "Just a note"
```

Appends a timestamped entry to `.claude/journal.md` in your project root. One confirmation line. That's it. Low friction is the whole point — if it takes more than 5 seconds you won't do it.

**Entry types:** `decision`, `warning`, `discovery`, `state`, `todo`, `note`

---

### `/brief` — synthesize at the end of a session

```
/brief
```

Reads the journal + key project files. Writes `.claude/HANDOFF.md` — a dense, honest briefing document covering:

- What this is (real user, real pain)
- Current state (what's built, what's not)
- Load-bearing decisions
- Active warnings / landmines
- Discoveries
- Where to start reading the code
- Recent log entries

Run this at the end of any significant session, or any time the project state changes meaningfully.

---

### `/orient` — reload at the start of a session

```
/orient
```

Reads `HANDOFF.md` and delivers a spoken briefing. Gets you (and Claude) fully oriented in under 2 minutes without crawling the codebase.

If `HANDOFF.md` is stale (>7 days), it says so. If only a raw journal exists, it briefs from that and suggests running `/brief`.

---

## How it fits together

```
During session:   /log decision "..."    ← capture as it happens
End of session:   /brief                 ← synthesize to HANDOFF.md
Start of session: /orient                ← reload, pick up where you left off
```

The journal (`.claude/journal.md`) is append-only. Never edited. Source of truth.
The handoff (`.claude/HANDOFF.md`) is synthesized. Overwritten by each `/brief` run.

Both files live in `.claude/` in your project root — commit them to git if you want teammates to benefit.

---

## Pair with code-review-graph

project-journal handles the *why*. [code-review-graph](https://github.com/tirth8205/code-review-graph) handles the *where*.

```
project-journal   → decisions, warnings, state, discoveries  (human knowledge)
code-review-graph → blast radius, callers, dependencies       (structural knowledge)
```

Install both, then add to your global `~/.claude/CLAUDE.md`:

```
Before reading files for any non-trivial task, call get_review_context_tool.
At session start, read .claude/HANDOFF.md if it exists (/orient).
```

Now every Claude session starts oriented and reads only what matters.

---

## Requirements

- [Claude Code](https://docs.anthropic.com/claude/claude-code)
- [gstack](https://github.com/garrytan/gstack)

---

## Install

```bash
git clone https://github.com/yourusername/project-journal
cd project-journal
bash install.sh
```

Or without git:

```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/project-journal/main/install.sh | bash
```

Restart Claude Code if it's running. Skills are available immediately.

---

## The philosophy

The goal is not to document everything. It is to capture the things that would cause a new developer — or Claude three weeks from now — to make a wrong call without knowing why.

A decision worth logging takes 10 seconds to write. A wrong call made without context can take hours to unwind.

Log the load-bearing stuff. Brief at the end. Orient at the start. Everything else is in the code.
