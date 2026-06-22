# Dyad Queue — relationship-enrichment candidates (NOT causal arcs)

> **Purpose (S121, 2026-06-21).** A holding queue for *relationship dyads* that surfaced during container
> decomposition but are the **wrong shape for a causal arc**. These are character↔character (or
> character↔event) ties best modeled as one or two typed edges (+ maybe a `WITNESS_IN`), NOT as causal
> event-node chains. The advisory board (lens 2 + lens 4) flagged that E7/E8 would "always be deferred as
> Essos junctures" because they are dyads masquerading as junctures — so they were lifted out of the
> Essos juncture list (`working/essos-decomposition.md` §3) into this queue.
>
> **Distinction from the arc backlog:** the arc backlog (`working/major-arc-backlog.md`,
> `working/wo5k-decomposition.md`) holds *causal spines* built via the arc-mint machine. This queue holds
> *standalone relationship edges* built via a normal curator mint (research → verify quote → append edge),
> no causal walk involved. Consume on demand (e.g. during an enrichment pass), not in build priority order.
>
> **Vocabulary:** Pass = numbered corpus sweep · Track = named workstream · step = ordered piece · Tier =
> confidence 1–5 only.

## Queue

### D1. Varys ↔ Illyrio conspiracy dyad  (was Essos E7)
- **Belongs to the AEGON / Targaryen-restoration container, NOT Essos** (board lens 4). Park here until the
  AEGON container is opened; it is the AGOT seed of that thread.
- **Scene:** Arya witnesses Varys + Illyrio in the tunnels beneath the Red Keep (agot-arya-03:73–97):
  the princess is pregnant, the khal won't move until the son is born, Ned "troubles my sleep," delay.
- **Model (dyad, not arc):** `varys CONSPIRES_WITH illyrio-mopatis` (symmetric, Tier-2/3, `evidence_kind:
  book-curator`, cite agot-arya-03.md:~89) + `arya-stark WITNESS_IN <the meeting>`. The WITNESS_IN target
  needs a node; per the S117 edge-vs-node rule the meeting becomes its own `event.*` node ONLY if the
  *seeing* gets an outgoing causal edge (Arya→Ned→dismissal is weak + 4–5-decision-mediated → agency-
  collapse, so NOT a causal node). Default: mint a light `varys-and-illyrio-conspire-in-the-tunnels`
  conspiracy-meeting node only if the AEGON container needs an anchor; else the CONSPIRES_WITH dyad lives
  on the two character nodes and the WITNESS_IN waits for that anchor.
- **Harvest row (parked):** `working/harvest-queue.md` carries the Arya-witness pointer (agot-arya-03:73),
  parked until this node exists.
- **Open question for the AEGON fan-out:** conspiracy-meeting event node vs character-dyad-only? — **RESOLVED
  S127 (AEGON decomp dip): DYAD-ONLY, do NOT mint the tunnel-meeting node.** Juncture A1's reveal node
  (`aegon-revealed-to-the-golden-company`) gives the spine its anchor, so the conspiracy attaches as the
  `varys CONSPIRES_WITH illyrio-mopatis` dyad on the character nodes; `arya-stark WITNESS_IN` stays parked
  (Arya's seeing has no clean outgoing causal edge → agency-collapse → never earns a node). Full justification:
  `working/aegon-decomposition.md` §6.

### D2. Jorah informant channel dyad  (was Essos E8)
- **Pure information channel — causal load 0.** Jorah informs on Dany to the Small Council for a royal
  pardon; this is the *vehicle* by which Robert learns of the pregnancy. Its causal consequence is already
  captured by `robert-orders-daenerys-assassination` (E4, built S119) — no event mint needed.
- **Model (dyad):** `jorah-mormont SPIES_ON daenerys-targaryen` + `jorah-mormont INFORMS varys` (Tier-3).
  Cite: Illyrio's letter conduit (agot-daenerys-07:41) + Jorah's pardon motive (re-verify exact lines at
  mint). Both edge types are live in the locked vocab (Knowledge & Information section).
- **No node, no causal edge.** Background condition only.

## Carried harvest WITNESS_IN candidates (S120, text-anchored, not yet minted)
These are clean role-edge candidates from the S120 Essos harvest pass — small curator mints (verify the
line, append the edge), no causal walk:
- `jorah-mormont WITNESS_IN drogo-blood-magic-ritual` — agot-daenerys-08:225
- `strong-belwas WITNESS_IN drogon-returns-to-daznak-pit` — adwd-daenerys-09:233
- `barristan-selmy WITNESS_IN drogon-returns-to-daznak-pit` — adwd-daenerys-09:233
- `reznak-mo-reznak WITNESS_IN drogon-returns-to-daznak-pit` — adwd-daenerys-09:233
- `mossador SIBLING_OF missandei` — adwd-daenerys-02:35 (kinship dyad)
