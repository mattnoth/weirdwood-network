---
name: "Euron hunts Aeron Damphair"
type: event.incident
slug: euron-hunts-aeron-damphair
aliases: ["Euron hunts Aeron", "Euron hunts the Damphair", "Ironmaker searches for the Damphair", "the search for Aeron Damphair", "Euron's hunt for Aeron"]
confidence: tier-2
era: war-of-the-five-kings
pass_origin: s116-enrichment
node_version: 1
evidence_chapters:
  - ADWD The Wayward Bride
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: cross-book-recall
  date_confidence: tier-2
---

## Identity

After [Aeron Damphair](aeron-greyjoy) [vanishes vowing to raise the ironborn smallfolk](aeron-vows-to-raise-the-ironborn-smallfolk) against the godless king, [Euron Greyjoy](euron-greyjoy) sets [Erik Ironmaker](erik-ironmaker) to search the isles for the missing priest — Euron's response to the one rival who refused to submit and whose prophet's voice can turn the common folk against him. [Tristifer Botley](tristifer-botley) believes the search is a sham: that Euron has already had Aeron's throat cut and stages the hunt only to mask the kinslaying, since "Euron is afraid to be seen as a kinslayer." **The published books leave Aeron's fate unresolved** — he is missing and hunted, neither confirmed dead nor found (so no `death-of-aeron` node is minted; the murder is an in-world rumor, not canon). Downstream — Aeron's eventual capture by Euron — is a TWOW beat not in the corpus, left dark.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S116 enrichment pass. CAUSED by [Aeron's resistance vow + disappearance](aeron-vows-to-raise-the-ironborn-smallfolk) (his threat to raise the smallfolk drives Euron to hunt him — CAUSES, Tier-2). [Euron Greyjoy](euron-greyjoy) orders the search (COMMANDS_IN, Tier-1); [Erik Ironmaker](erik-ironmaker) conducts it (AGENT_IN, Tier-1); [Aeron Greyjoy](aeron-greyjoy) is the hunted (VICTIM_IN, Tier-1). The rumor that the hunt masks a murder is recorded in `## Quotes`, not modeled as a `SUSPECTED_OF` edge — there is no confirmed death to point it at.)

## Quotes

> "I think the Damphair's dead. I think the Crow's Eye slit his throat for him. Ironmaker's search is just to make us believe the priest escaped. Euron is afraid to be seen as a kinslayer."

— Tristifer Botley to Asha (an unconfirmed suspicion; Aeron's fate is unresolved in the published books), ADWD The Wayward Bride (`sources/chapters/adwd/adwd-the-wayward-bride-01.md:183`)
