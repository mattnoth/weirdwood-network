# SESSION 216 — Theories staging review: validate the R+L=J cluster, settle the schema, then next builds

> **This is Session 216.** Stamp your worklog entry `### Session 216` at endsession.
> (Renumbered from 215 at S215 endsession — the harvest-drain session took S215; theories is the next session.)
> **Recommended model:** **Fable orchestrator** (schema/integration adjudication with Matt) +
> Sonnet proposers + Haiku fresh-verifiers for any new builds.
> **PRE-REQ:** S214 committed+pushed. If git log disagrees with worklog.md S214, STOP and reconcile.

## State (end of S214)

Wave-1 pipeline is COMPLETE: all 15 ASX videos extracted (21 theory headers / 792 beats),
re-grounded to **406 byte-verified verbatim chapter:line cites**. Artifacts:
`working/theories/{extractions,regrounding,regrounding-agent}/` + scripts
`theories-vtt-clean.py` / `theories-reground.py` / `theories-reground-repair.py`.

The **R+L=J cluster is STAGED at the mint gate** in `working/theories/rlj-cluster/`:
- `nodes/r-plus-l-equals-j.node.md` (new; tier-3, status show-confirmed)
- `enrich/knight-of-the-laughing-tree-theories.node.md` (stub rewrite; tier-3, open)
- `candidates.json` — 13 edges (12 SUPPORTS / 1 CONTRADICTS), quotecheck 13/13, dry-run green
- `ADJUDICATION-s214.md` — fresh-verify 12C/2A/0R + orchestrator adjudications
  (T8→premise prose · T9 requoted · T6 tier-3→tier-4)

**Matt's S214 decision: ALL theory nodes stay on STAGING. No mint without a validation
review.** (Worklog Active Decision, S214.)

## The work

1. **Staging review with Matt** — walk the R+L=J cluster artifacts; ratify or amend the
   S214 conventions (worklog Active Decision S214): node-per-canonical-theory ·
   evidence-node→theory SUPPORTS/CONTRADICTS w/ byte-verified quotes · edge-tier
   variance · claim-in-frontmatter · CITED_BY deferral · domain-labelled ungrounded
   sections. Open questions queued for him: (a) CITED_BY / out-of-world source node
   type, (b) umbrella-stub linkage, (c) whether/how the chat ever exposes theories,
   (d) KotLT display name.
2. **Validation/testing Matt asked for** — candidates (pick with him): fresh Sonnet
   pressure-test agent over the staged node prose (theory-stated-as-fact leak check);
   verify_node_quotes-style check against the staged files; a query-layer dry probe
   (what would neighbors/dossier surfaces look like if minted — bundle impact);
   architecture.md sync draft for the new frontmatter fields.
3. **Next theory builds (same machine, still staged)** — grounded substrate is ready
   for: eldritch-apocalypse (S110 seed + Euron video, 12 det matches), GNC,
   grand-maester-conspiracy, bolt-on, A+J=T, jojen-paste, hooded-man (+
   winterfell-murders sub-theory), coldhands, patchface, azor-ahai enrichment
   (2 videos incl. held-out Rhaegar-as-AA beats), bastard-letter enrichment,
   bloodraven cluster (5 headers). Per-cluster: proposer → fresh-verify → adjudicate
   → quotecheck → dry-run → STAGE (not mint).

## Residue (small, non-blocking)

- ~36 byte-fail rows across regrounding-agent files (excluded from anything mintable);
  a consolidated Haiku redo could rescue some.
- Coldhands residue file missing its last 2 beats (agent died at the spend wall).
- `mint_enrichment.py` validation mode writes new-node files into the real graph
  (S214 incident — reverted); add `--nodes-root` before the next dry-run.

## Vocabulary (paste into subagent prompts — they don't load CLAUDE.md)

Pass = big numbered corpus sweep; Track = named chunk of work; step (lowercase) =
ordered piece inside a Track; Tier = confidence rating 1–5 ONLY.
Harvest rule: while in chapter text for ANY reason, drop `chapter:line / kind / note`
pointers to notable off-task finds into the agent's own harvest file; POINT, don't extract.

## DO NOT

- Do NOT mint/deploy ANY theory node or edge — staging only (Matt S214, standing).
- Do NOT let theory claims into tier-1/2 or into node prose stated as fact.
- Do NOT touch the chat's no-theories guardrail.
- Do NOT re-pull ASX transcripts (all 15 clean on disk).
- Do NOT run /endsession without permission.
