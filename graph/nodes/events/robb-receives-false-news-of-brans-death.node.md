---
name: "Robb receives false news of Bran and Rickon's deaths"
type: event.incident
slug: robb-receives-false-news-of-brans-death
aliases: ["the Greatjon brings Robb news of Winterfell", "false news of Bran and Rickon's deaths", "Robb learns his brothers are dead", "news of Winterfell reaches the Crag"]
confidence: tier-1
era: war-of-the-five-kings
containers: [wo5k]
pass_origin: s123-wo5k-q5
node_version: 1
evidence_chapters:
  - ASOS Catelyn II
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-recounted
  date_confidence: tier-2
---

## Identity

While [Robb Stark](robb-stark) was recovering at the [Crag](crag) from a festering arrow wound taken in [the storming](storming-of-the-crag), the [Greatjon Umber](greatjon-umber) brought him word that [Winterfell](winterfell) had fallen and that his brothers [Bran](bran-stark) and [Rickon](rickon-stark) were dead — slain by [Theon Greyjoy](theon-greyjoy), who had [taken the castle](capture-of-winterfell) and displayed two tarred heads above its gates as proof. The report was **false**: the heads belonged to two miller's boys Theon had killed and passed off as the Stark heirs; Bran and Rickon had escaped. But Robb believed it, and the grief drove him into the arms of [Jeyne Westerling](jeyne-westerling), who nursed and comforted him. He [wed her the next day](robb-weds-jeyne-westerling), holding it "the only honorable thing to do" — and in doing so broke his betrothal-pact with [House Frey](house-frey), the breach that would ripen into the [Red Wedding](red-wedding).

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S123 WO5K-remainder track / Q5. Caused by [Theon's capture of Winterfell](capture-of-winterfell) and its faked deaths (capture-of-winterfell CAUSES, Tier-2). The grief MOTIVATES [Robb Stark](robb-stark) (Tier-2) and TRIGGERS [Robb's marriage to Jeyne](robb-weds-jeyne-westerling) (Tier-2), which separately is ENABLED by [the storming of the Crag](storming-of-the-crag) putting the wounded Robb in Jeyne's care. The wedding in turn TRIGGERS the [Red Wedding conspiracy](red-wedding-conspiracy) (already wired). The falseness of the news is itself the hinge of dramatic irony: Robb breaks the alliance that kills him over brothers who are alive.)

## Quotes

> "The Crag was weakly garrisoned, so we took it by storm one night. ... I took an arrow in the arm just before Ser Rolph yielded us the castle. It seemed nothing at first, but it festered. Jeyne had me taken to her own bed, and she nursed me until the fever passed. And she was with me when the Greatjon brought me the news of . . . of Winterfell. Bran and Rickon." He seemed to have trouble saying his brothers' names. "That night, she . . . she comforted me, Mother."

— Robb Stark recounting the Crag to Catelyn, ASOS Catelyn II (`sources/chapters/asos/asos-catelyn-02.md:143`)

> Catelyn did not need to be told what sort of comfort Jeyne Westerling had offered her son. "And you wed her the next day."

— ASOS Catelyn II (`sources/chapters/asos/asos-catelyn-02.md:145`)

> He looked her in the eyes, proud and miserable all at once. "It was the only honorable thing to do. She's gentle and sweet, Mother, she will make me a good wife."

— Robb Stark, ASOS Catelyn II (`sources/chapters/asos/asos-catelyn-02.md:147`)
