---
name: "Ned orders Daenerys's assassination cancelled"
type: event.assassination
slug: ned-orders-daenerys-s-assassination-cancelled
aliases: ["Ned cancels Daenerys's assassination", "Ned calls off the assassins", "Ned orders the assassination cancelled", "Robert's change of heart about Daenerys", "Ned tries to call off the killers", "Eddard countermands the order to kill Daenerys", "let her live"]
confidence: tier-1
era: roberts-reign
pass_origin: s119-essos-root-track
node_version: 2
evidence_chapters:
  - AGOT Eddard XIII
occurred:
  ac_year: 298
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-present
  date_confidence: tier-2
---

## Identity

On his deathbed after the boar's goring, [King Robert Baratheon](robert-baratheon) repents the [order he gave to kill Daenerys Targaryen](robert-orders-daenerys-assassination) — "The girl. Daenerys. Let her live ... don't let them kill her." Acting on the dying king's reversal, [Eddard Stark](eddard-stark) commands [Varys](varys) to undo the arrangements at once: "Robert had a change of heart concerning Daenerys Targaryen. Whatever arrangements you made, I want unmade. At once." Varys warns it may already be too late — "I fear those birds have flown." The countermand is the direct unmaking of Robert's original order, and it is the in-world reason the wine-merchant attempt at Vaes Dothrak proved the last sanctioned attempt for a time. It comes too late to matter to the Essos thread: by then Drogo has already sworn his westward vow and the dragons are nearly born.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`. [Eddard Stark](eddard-stark) is the orderer of the cancellation (COMMANDS_IN, Tier-1); [Varys](varys) is the agent tasked with unmaking it (AGENT_IN, Tier-1); [Daenerys](daenerys-targaryen) is the subject (VICTIM_IN, Tier-1). This cancellation is the negation of [Robert's assassination order](robert-orders-daenerys-assassination) — but fresh-verify (S119) declined a CAUSES edge from the order: the order is the *object* being cancelled, not the cause. The true cause is Robert's deathbed change of heart (unmodeled), so this node carries no causal upstream by design. Node repaired S119 essos-root track [was a bare Plate-3 skeleton].)

## Quotes

> "The girl," the king said. "Daenerys. Let her live. If you can, if it … not too late … talk to them … Varys, Littlefinger … don't let them kill her."

— Robert Baratheon, AGOT Eddard XIII (`sources/chapters/agot/agot-eddard-13.md:89`)

> "Robert had a change of heart concerning Daenerys Targaryen. Whatever arrangements you made, I want unmade. At once." ... "Alas," said Varys. "At once may be too late. I fear those birds have flown."

— Eddard Stark and Varys, AGOT Eddard XIII (`sources/chapters/agot/agot-eddard-13.md:153`)
