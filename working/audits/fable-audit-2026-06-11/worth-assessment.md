# Worth Assessment — The Weirwood Network

> Written 2026-06-12 by a read-only Fable subagent, on Matt's instruction: "your unsentimental take
> on what this project is actually worth. No flattery, no hedging... a take that flatters me is
> worthless." Sources: synthesis.md, history-audit.md, graph-deep-dive.md (this folder),
> reference/architecture.md, the scripts/ and .claude/agents/ listings, and general knowledge of the
> mid-2026 LLM/KG landscape. A prior partial draft of this file was discarded unread per instruction.

---

## 1. The agnostic benefits — strip away ASOIAF

Remove every dragon and the project decomposes into two piles: a **methodology** that transfers
nearly intact, and a **corpus artifact** that transfers almost not at all. The honest finding is
that the methodology is the more valuable pile, and it is currently in the worse shape for reuse.

### The playbook (transfers, but only as patterns + a worked example)

These are the rules that demonstrably changed outcomes, each with receipts in history-audit §C/§D:

- **Python-before-agent.** Instituted S24 after a 2–3× agent-cost overrun; decisive at least six
  times. ~7,000 of ~8,300 nodes, all indexes, the alias resolver, and the 2,834-edge spine were
  produced deterministically for ~$0, against a projected ~$1,200 agent path for the nodes alone.
  The corollary that kept proving out: *every time a pass was re-examined, more of it turned out to
  be deterministic.* This is the single most transferable lesson, and it cuts against the default
  instinct of every LLM-tooling vendor in 2026.
- **Smoke-before-spend with measured NO-GO gates — two distinct mechanisms, both real.** Pre-spend
  gating: ~$11 of smokes held the ~$270–290 extra-tables bulk, which never ran. Post-hoc audit
  gating: Events-Haiku's ~$50 bulk *did* run — operationally flawless, ~85–90% on hand-read
  smokes — and was killed afterward by a 48%-vs-70% cross-model audit; the discipline there was
  deprecating sunk output, not avoiding the spend. And the avoided-spend ledger's ~$4,400-vs-~$800
  contrast needs two corrections: ~$2,000 of the "avoided" was a projected fleet budget that was
  never going to be spent, and the ~$800 counts tracked API spend only, not the untracked
  Max-subscription time that did most of the work (see §3).
- **Vocab lockdown + zero-freeform schema.** The S54 finding is the generalizable one: Haiku at
  ~80% semantic failure pre-lockdown, ~3–4% violations post-lockdown. The durable fix for cheap
  models is not better prompts — it is removing every freestyle surface (locked edge vocabulary,
  qualifier enums, deleted `notes` field) and validating mechanically with drift-halt exit codes.
- **Provenance in every row** (`evidence_kind`, `typed_by`, `prompt_sha`, `run_id`, supersede stamps)
  and **in-data deprecation, never deletion**. This is what made the comention dead end recoverable
  as Plate-4 input and made the S64 dual-run incident diagnosable at all.
- **Cross-model audit + fresh-eyes review.** ~7 instances where a fresh context corrected the
  orchestrator's own conclusion (S71 false alarm, S81 miscited smoke, S82 cleanroom). The insight:
  the precision floor came from adversarial process, not from any model being good.
- **Operational learnings for unattended bulk runs** — fail-fast, resume, rate-wall detection,
  single-coordinator loops, key-based (not count-based) health checks. Learned expensively: ≥6
  incidents across three eras before the pattern stuck.

### Machinery: agnostic vs ASOIAF-specific

Genuinely corpus-agnostic *patterns*: the mechanical schema validator + halt-code design, the
edge-direction normalizer, the alias-resolver construction, index builders, the `run-forever`
supervision wrappers, the drift-audit harness, reification-with-role-edges, the no-silent-drop
pipeline shape. ASOIAF-specific: the 163-type vocabulary itself, POV canonicalization, spoiler
gating, the entity hierarchy, and the wiki infobox field map.

But be honest about packaging: the 146 scripts are not a library. They hardcode this repo's paths
and schemas, and the listing is littered with one-offs (`classify-ramsay-snow.py`,
`temp-classify-glovers.py`, seven near-duplicate `stage4-haiku-classify*` variants). Nobody reuses
this code; they reuse the *design* after reading it. As shipped, the playbook exists only as
inference over 18 worklog archives — it has never been written down domain-agnostically.

### Who would actually pay / reuse / learn

- **A team building a legal/medical/compliance/lore KG with LLM extraction**: high value from the
  lockdown + NO-GO + provenance stack — these are exactly the failure modes such teams hit — but
  only via a written-up playbook or a consulting conversation, not via this repo as-is.
- **A solo dev replicating the method on their own corpus**: the best-fit audience. The repo proves
  the whole thing is doable by one person on a Max subscription plus ~$800 of tracked API spend.
- **A researcher / cost analyst**: the spend ledger is legitimately rare empirical data — per-pass
  dollar costs, 2–7× estimate errors, model bake-off results, precision-vs-cost tradeoffs for
  Opus/Sonnet/Haiku on a real extraction workload in 2026. Most such numbers never get published.
- **Nobody** pays for the ASOIAF graph itself (see §3).

## 2. The real worth

### Commodity vs distinctive, calibrated to mid-2026

Be clear-eyed: **LLM-extraction-to-KG is a crowded, largely commoditized space.** GraphRAG and its
descendants, Neo4j's LLM graph builders, LlamaIndex/LangChain KG construction, instructor-style
schema-constrained extraction, LLM-as-judge evaluation — all off the shelf. Entity resolution is a
decades-old field. "We extracted a knowledge graph from books with Claude" is, in 2026, a weekend
blog post. None of that is novel here, and pretending otherwise would be the flattery Matt banned.

What is actually distinctive, in descending order of confidence:

1. **The evidence standard, enforced mechanically.** 3,782 of 4,760 edges carry a verbatim quote
   mechanically re-located to an exact `file:line` with a `locate_status=verbatim` check; 948
   edges (897 of them book-derived reified ones) cite chapter-level only; 32 lack quotes. Human
   verification of the locator is thin — a spot-check of 5 rows, 5/5 exact. Citation-grounding is
   common as an *aspiration*; "a wrong cited edge is graph pollution" held as a *gate* — through
   NO-GO decisions that left budgeted money unspent — is genuinely rare. Most comparable projects,
   hobby and professional, ship the plausible-looking swamp.
2. **The measured-discipline record.** Not the rules themselves (any ML-ops blog lists them) but
   the documented 91-session history of the rules being violated, the incidents that resulted, and
   the structural fixes — including ~$250 of honestly-accounted dead end. As a process artifact it
   is more complete than most industrial postmortem cultures produce.
3. **Self-correction at audit cost.** The process caught its own worst sequencing failure — the
   unmerged infobox layer (§3) — for roughly the cost of one audit session, and produced an
   owner-accepted correction. A record that surfaces its own errors cheaply is itself evidence the
   process record has value; errors of this class are usually found by users, or never.
4. **The cost profile.** Deterministic-first inverted the usual economics: the tracked API spend
   bought only what genuinely required judgment, and the audit trail proves which steps those
   were — though the headline dollar figure omits the subscription time that powered the rest
   (see §3).
5. **Reification with provenance** (event hubs, role edges, head rule, SUB_BEAT_OF) is solid
   engineering but standard KG modeling — distinctive only in that a solo+agents project did it at
   all, with a validated 2-hop traversal.

### Who it matters to

- **Matt**: the real return so far is a now-portable skill in running agent fleets safely on a
  budget — demonstrably improved between the S33 chain explosion and the audited Plate-5 ship.
- **Agents traversing it**: a dense, trustworthy affect/interaction graph over ~1,200 entities —
  and a wall at the other 85% of nodes until the infobox merge lands. Today it serves its stated
  primary user only partially.
- **ASOIAF fans**: approximately nothing yet. AWOIAF exists, is bigger, and is one search away.
- **A hiring manager**: a strong agent-orchestration/LLM-ops portfolio piece *if narrated* — the
  repo as-is is unreadable to an outsider (doc rot, 146 scripts, 18 archives). The audit folder
  this file sits in is currently the best entry point that exists.
- **A method replicator**: the highest-leverage audience, currently unserved by any writeup.

### The strongest single honest claim

**One person, in 91 agent-orchestrated sessions and ~$800 of tracked spend (atop an untracked Max
subscription), built an 8,300-node graph where 3,782 of 4,760 edges carry a verbatim book quote
mechanically re-located to exact file:line (948 reified edges cite chapter-level) — a citation
discipline I know of no comparable hobby-scale LLM-extracted graph matching — plus the audited
spend ledger proving which pipeline steps needed a model at all.**

## 3. The weaknesses

### Overbuilt, specifically

- **28 agent definitions for a solo project**, of which a handful (mechanical-extractor,
  script-builder, wiki-ingester, a couple of auditors) ever did real work. `chekhovs-gun-tracker`,
  `perception-mapper`, `theory-evidence-scorer` et al. are aspirational stubs.
- **The fleet apparatus**: three planning docs in `working/agent-fleet-specs/`, a 27-agent roster,
  a "$1,250–2,310" budget — never executed. The mission protocol shipped, was used ~3 times, and
  has been dormant since S48. This is design-as-recreation, and it cost sessions.
- **Process overhead per session**: /endsession checklists, worklog + 5-entry archive rotation,
  session-detail files, continue prompts, memory hygiene. Some of it earns its keep (rule #9 was
  invoked productively ≥4 times); much of it is self-administration. The tell: at 91 sessions a
  dedicated audit was needed to discover the project's own documentation was wrong about its state.
  A process that requires a $-priced audit to stay honest does not scale past one owner.
- **Script sprawl**: 146 scripts, heavy one-off and near-duplicate mass, no packaging, no
  separation of reusable machinery from run-specific glue.

### What a hostile skeptic says, and where they're right

- *"Everything here was built, judged, and graded by one model family."* Correct, and this belongs
  at the top. The build ran on Claude variants; the "cross-model audit" was Sonnet judging Haiku —
  same family, correlated blind spots; the prior audits and this assessment are Claude too. Every
  precision number in this document is self-reported by the pipeline being graded; independent
  human verification is about five rows. A systematic extraction error shared across the family
  would be invisible to every check the project has run. No mitigation exists in the repo today.
- *"The ~$800 is not the cost."* The dominant real input was 91 sessions of untracked
  Max-subscription LLM time — orchestration, audits, and extraction passes that never touched the
  metered API. The ledger captures tracked API spend only, so the ~$800-vs-~$4,400 contrast
  overstates the efficiency twice over: the denominator omits the largest cost, and ~$2,000 of the
  "avoided" figure was a projected fleet budget that was never going to be spent anyway. The
  honest framing is "~$800 of marginal API spend on top of a subscription doing the heavy lifting."
- *"78% strict precision is a D+ if you treat it as a database."* Correct as stated. The defense —
  affect edges run hot but `asserted_relation` preserves nuance, and the tiers signal trust — is
  real but partial. For lookup-grade facts the graph is not yet a database; it's a cited candidate
  store.
- *"4,760 edges in two months; a wiki dump has millions."* Worse than that: the audit found 20,614
  deterministic, already-typed infobox relationship rows sitting parsed on disk **since April**
  while ~$250 and five weeks went to LLM prose-edge extraction that was then deprecated. The
  deprecation was right; the sequencing failure was the project's largest process error, and 85%
  of nodes are isolated today because a free merge was never scheduled. The partial credit: the
  project's own audit found it, at one session's cost (§2).
- *"Nobody has used it for the destination feature."* True and damning-adjacent. Zero dialog
  sessions, zero agent-traversal users, including Matt. The core thesis — that this graph makes an
  agent meaningfully better at ASOIAF conversation than base-model knowledge plus wiki RAG — is
  **unvalidated**, and it is not obviously true: ASOIAF is saturated in every frontier model's
  weights. The worst-case reading is that the graph's marginal utility over "just ask Claude" is
  small, and no test has yet been run that could falsify that.
- *"Theories and prophecies — the soul of an ASOIAF graph — are absent."* 45 theory nodes with one
  (probably misresolved) edge; 2 prophecy nodes, zero edges. The most differentiated content the
  project could offer (the thing AWOIAF does *badly* and base models hedge on) is the least built.
- *"Elaborate yak-shaving."* The meta-layer (worklogs, audits, audits-of-audits, this assessment)
  plausibly exceeds the object-level product in word count. The rebuttal — the meta-layer *is* the
  transferable product — is true only if it gets extracted; today it's shavings.

### What would have to be true for this to matter beyond a portfolio

1. **The dialog/traversal layer ships and beats baseline** — a measured comparison against
   vanilla Claude + AWOIAF retrieval on a fixed question set. This is the falsifiable claim the
   whole project rests on, and it is one session of evaluation away after the infobox merge.
2. **The playbook gets written domain-agnostically** — a standalone document (or repo) of the
   lockdown/NO-GO/provenance stack with the cost data. That artifact would outvalue the graph.
3. **N≥2 domains** — the method replicated once on a corpus that is *not* in model weights (private
   docs, niche legal/technical corpus), where extraction actually adds information. ASOIAF was a
   fine training ground and a weak proof.

### Market value

I don't know, and anyone quoting a number is guessing. Conditionals: as a salable product, ~$0
today and probably forever — and the problem is sharper than "fan market won't pay." The graph
embeds 4,728 verbatim book quotes and the repo carries full chapter texts of five novels: any
*published* form, free or paid, is a copyright problem before it is a market problem. The evidence
standard that makes the graph trustworthy is the same thing that makes it unpublishable as-is;
a public release would need quote truncation/snippet-izing and exclusion of the chapter corpus.
As career capital for agent-orchestration work, meaningful but only after a narration pass. As a
methods writeup with the spend ledger attached, the most plausibly valuable artifact — and it
doesn't exist yet (the writeup needs no quotes; it is the one form with no copyright exposure).

## Verdict

The Weirwood Network is a real, validated, honestly-accounted engineering artifact whose graph is
worth little and whose process record is worth a lot — currently trapped in a form only its author
can read, attached to a destination feature nobody has tried. ~$800 of tracked API spend — riding
on a much larger untracked subscription cost — bought a defensible evidence standard, a hard-won
operations playbook for cheap-model bulk extraction, and proof that one person can do this; it did
not yet buy evidence that anyone needed the result, and every quality number it rests on was graded
by the same model family that produced it. The next ~$0 of work (the
infobox merge, then a baseline-comparison dialog test, then the domain-agnostic writeup) determines
whether this was an exceptional apprenticeship or an actual contribution. Both would have been
acceptable outcomes; only one should be claimed.

---

## Changelog

- **v2, 2026-06-12** — hostile-critic review applied (verdict: ACCEPT-WITH-FIXES). Changes:
  1. Headline claim corrected — "every book-derived edge … verified at an exact file and line"
     was false (3,782/4,760 at file:line; 948 chapter-level, 897 of them book-derived reified;
     32 quoteless). Replaced in §2 "strongest claim" and in §2 distinctive item 1.
  2. "Essentially no comparable LLM-extracted graph meets this standard" hedged to an
     "I know of none" claim — the original was unfalsifiable as written.
  3. Added top-tier weakness: single-model-family risk — build, judge (Sonnet auditing Haiku),
     audits, and this assessment are all Claude variants; all precision numbers are self-reported
     by the pipeline being graded (human verification ≈5 rows).
  4. Added weakness: the ~$800 excludes the dominant real cost (91 sessions of untracked
     Max-subscription time); $800-vs-$4,400 framing corrected wherever it appeared, noting
     ~$2,000 of "avoided" was a projected budget that was never real.
  5. Copyright weakness strengthened: 4,728 verbatim quotes + full chapter texts make any
     published form a copyright problem, not merely a $0 fan market.
  6. Smoke-before-spend conflation fixed: the $11-smokes-held-$270-bulk credit belongs to the
     extra-tables NO-GO; Events-Haiku's ~$50 bulk ran and was killed post-hoc by cross-model
     audit. Each mechanism now credited separately.
  7. Added undersold strength (§2 item 3): the process caught its own sequencing failure
     (unmerged infobox layer) for ~one audit session's cost, with an owner-accepted correction.
     Performative flourishes trimmed ("single most embarrassing fact", "obsessive owner").
  8. Scripts count corrected 148 → 146 (three occurrences).
- Rejected critic findings: none.
- **v1, 2026-06-12** — original draft.
