# Progress

Tracks the state of in-progress work across agent invocations and sessions. When an agent finishes a batch, is interrupted, or surfaces something interesting, it logs in the appropriate file here. The next agent (or session) reads to pick up where things left off.

## Files

| File | What it tracks |
|------|---------------|
| `pass1-agot.md` | Pass 1 mechanical extraction wave log for AGOT |
| `handoffs.md` | Work that needs human action or agent pickup |
| `scratch-notes.md` | Observations worth keeping but not yet triaged |

When new books or passes start, create new files: `pass1-acok.md`, `pass2-wiki.md`, etc.
