---
session: 120
date: 2026-06-21
model: Opus 4.8 (orchestrator) + Sonnet 4.6 subagents (3 build research/verify + 4 advisory board + 1 fresh critic + 1 harvest)
type: build + design-review
---

# Session 120 — ESSOS E3/E5 build, then a container/process advisory review

## Arc 1 — Build (execution)
Resumed the ESSOS container from the S119 handoff (E4+E1+E2 done). Built the two remaining high-value junctures via the arc-mint machine:
- **E3** (Daznak's Pit → Drogon flees → Dany lost on the Dothraki sea) — 3 new event.incident nodes + 8 edges (3 causal Tier-2 + 2 role + 3 SUB_BEAT_OF). Fresh research+verify subagent adjudicated `wedding ENABLES drogon-returns` (not CAUSES — preserves Drogon's autonomous agency).
- **E5** (Doran pact-reveal → Quentyn's death) — 2 new nodes + 6 edges, modeled as **two clean segments** (the reveal is exposition posterior to the already-underway quest; chronology forbids a causal link). Corrected the common fan misattribution: **Rhaegal** (not Viserion) burns Quentyn.
- All 14 edges passed the citation checker (0 line drift; every ref re-pinned pre-mint).
- **Harvest-consume pass:** 53 rows → 37 attached, 15 dedup, 1 parked. Queue 0 open.

The ESSOS high-value spine (E1–E5) is now complete. Full build facts in the worklog S120 entry + `working/session-results/2026-06-21-essos-e3-research.md` / `…-e5-research.md` / `…-harvest-pass-s120.md`.

## Arc 2 — Advisory review (design)
Matt asked for (a) a rec on next and (b) a fresh-eyes audit of how the two major containers (Essos, WO5K) and the narrative-arc hierarchy are organized — confirm on-track / catch drift.

**4-lens advisory board** (structure · causal-semantics · process · taxonomy) → unanimous **on-track, yes-with-caveats**. Crown jewel praised by all: the **sequence-only-trap discipline**. Full findings: `working/session-results/2026-06-21-container-advisory-board.md`. Headline caveats: the **ENABLES traversal gap** (`--causal-chain` skips ENABLES → the spine reads as disconnected segments), **two missing containers** (NORTH/Wall, AEGON), the WO5K↔Essos **seam** (Robert's-order), and small process hardening.

**Fresh-critic pass** on the resulting next-session plan + continue prompt → confirmed sequencing, and found 3 concrete graph bugs by reading the live graph: `arrest-of-eddard-stark` mis-typed `event.battle`; the `petyr-baelish BETRAYS eddard-stark` dyad exists with a **broken evidence quote** (cites Ned reading the will, not the betrayal); `sansa-stark BETRAYS eddard-stark` exists as an unmodeled upstream cause of the arrest.

**Teaching artifact:** wrote `graph-concepts-explainer.md` (gitignored, Matt's reference) — nodes/edges/directed graphs, walking/traversal/upstream/inverse-causal, the four causal edge types, causal chains (Essos worked example), the sequence-trap, the ENABLES gap, convergence/divergence (many-to-one join hubs), reification, the decomposition-doc trick.

## Decisions reached (see worklog Active Decisions)
- **Granularity policy:** a node may be `SUB_BEAT_OF X` AND causal-into-X **only when it is chronologically prior to + a prerequisite for X**, never when constitutive of X. `ned-confesses-to-treason` (SUB_BEAT_OF + TRIGGERS execution) is the legit case; `littlefinger-betrays-ned` will be SUB_BEAT_OF-only. This is the mirror of the sequence-trap (don't under-draw causation; don't fake convergence with constitutive beats).
- **`containers:` frontmatter field** (array) adopted in principle (Matt leans yes) — a tag, NOT an umbrella parent (no chain-as-arc violation); `--container` documented as bag-retrieval, not "the arc"; null/omit for untagged standalones, never `[]`.
- **Two verify gate-levels named:** L1 verified-at-mint (ok for ENABLES/role/simple), L2 independent fresh-verify (required for cross-book/contested CAUSES).
- **`littlefinger-betrays-ned` is a confirmed gap → mint next session** (marquee betrayal; quotes verified: `agot-eddard-14:125` payoff + `agot-eddard-05:173` setup). Cersei's "game of thrones, you win or you die" correctly attributed to Cersei (`agot-eddard-12:169`), NOT Littlefinger.
- **Book-cite overlays done this session:** Cersei's title-drop quote (`agot-eddard-12:169`) + Varys's "innocents who suffer" speech (`agot-eddard-15:155`) — both were wiki-cited only; added navigable book cites (kept the wiki refs — overlay is additive, both retained).

## Next
3-step plan in the live continue prompt: (1) hardening pass, (2) container-split advisory fan-out, (3) WO5K remainder build. See `progress/continue-prompts/2026-06-21-essos-container-decomposition.md`.
