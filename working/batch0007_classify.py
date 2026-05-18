#!/usr/bin/env python3
"""
Batch 0007 prose-edge classifier — files 3-30.
Files 1-2 (lord-bracken-father-of-otho, lord-bracken-hand-of-the-king) already written.
"""
import json, os

BASE = "/Users/mnoth/source/asoiaf-chat"

def e(source, target, edge_type, snippet, section, bucket, confidence="tier-1", qualifier=None):
    row = {"decision": "emit_edge", "candidate_kind": "source_target",
           "source": source, "target": target, "edge_type": edge_type,
           "evidence_snippet": snippet, "evidence_section": section,
           "source_bucket": bucket, "confidence": confidence}
    if qualifier:
        row["qualifier"] = qualifier
    return json.dumps(row)

def r(source, target, reason, bucket):
    return json.dumps({"decision": "reject_just_mention", "candidate_kind": "source_target",
                       "source": source, "target": target, "reason": reason,
                       "source_bucket": bucket})

def write_file(bucket, slug, rows):
    dir_path = f"{BASE}/working/wiki/pass2-buckets/{bucket}/prose-edges"
    os.makedirs(dir_path, exist_ok=True)
    path = f"{dir_path}/{slug}.edges.jsonl"
    with open(path, "w") as f:
        f.write("\n".join(rows) + "\n")
    print(f"Written {len(rows)} rows: {slug}")

# ── File 3: lothar-bracken ──────────────────────────────────────────────────
BKT = "characters-house-bracken"
rows = [
    e("lothar-bracken","agnes-blackwood","OPPOSES",
      "Lothar's neighbour, Lady [LINK], led the rivermen in resisting Harwyn's ironborn, but Lord Lothar attacked her army from behind.",
      "## Origins", BKT),
    e("lothar-bracken","harwyn-hoare","PRISONER_OF",
      "but Harwyn crushed the rebellion, sacking and destroying Stone Hedge, and imprisoning Lothar in a [crow cage].",
      "## Origins", BKT),
    e("lothar-bracken","house-hoare","OPPOSES",
      "Harwyn claimed the riverlands for [LINK]. Six months later, Lothar rebelled against this new King of the Isles and Rivers.",
      "## Origins", BKT),
    e("lothar-bracken","king-of-the-trident","CLAIMS",
      "Some have theorized that Lothar hoped to become [LINK] once Harwyn defeated Arrec.",
      "## Origins", BKT, confidence="tier-3", qualifier="speculative — 'Some have theorized'"),
    e("lothar-bracken","stone-hedge","RULES",
      "Harwyn crushed the rebellion, sacking and destroying [LINK], imprisoning Lothar.",
      "## Origins", BKT, confidence="tier-2"),
    r("lothar-bracken","arrec-durrandon","contextual mention of former king under whose rule riverlands were; no direct lothar→arrec relationship",BKT),
    r("lothar-bracken","crow-cage","concept.custom; no applicable edge type for imprisonment in an object",BKT),
    r("lothar-bracken","ironborn","generic group reference, not a specific relationship",BKT),
    r("lothar-bracken","king-of-the-iron-islands","title contextually describing Harwyn; not a lothar→title edge",BKT),
    r("lothar-bracken","king-of-the-isles-and-the-rivers","OPPOSES doesn't go character→title; covered by OPPOSES house-hoare",BKT),
    r("lothar-bracken","riverlands","geographic region, contextual only",BKT),
    r("lothar-bracken","storm-king","title/role, contextual background only",BKT),
]
write_file(BKT, "lothar-bracken", rows)

# ── File 4: lyle-bracken ───────────────────────────────────────────────────
rows = [
    e("lyle-bracken","maegor-i-targaryen","OPPOSES",
      "He fought in the trial of seven in which seven of the Warrior's Sons faced King [LINK] and his six champions. Ser Lyle died during the fight.",
      "## Origins", BKT),
    e("lyle-bracken","sept-of-remembrance","LOCATED_AT",
      "He was a member of the King's Landing chapter of the Warrior's Sons, based in the [LINK].",
      "## Origins", BKT),
    r("lyle-bracken","trial-of-seven","concept.custom, not event.*; FIGHTS_IN requires event.* target",BKT),
]
write_file(BKT, "lyle-bracken", rows)

# ── File 5: mohor ──────────────────────────────────────────────────────────
rows = [
    e("mohor","catelyn-stark","ALLIES_WITH",
      "Mohor is one of three Bracken men-at-arms at the inn at the crossroads who assist Lady [LINK] in taking captive Tyrion Lannister.",
      "## Narrative Arc / ### A Game of Thrones", BKT, confidence="tier-2"),
    e("mohor","inn-at-the-crossroads","LOCATED_AT",
      "Mohor is one of three Bracken men-at-arms at the [LINK] who assist Lady Catelyn Stark.",
      "## Narrative Arc / ### A Game of Thrones", BKT),
    e("mohor","tyrion-lannister","CAPTURES",
      "who assist Lady Catelyn Stark in taking captive [LINK] and bringing him to the Vale of Arryn.",
      "## Narrative Arc / ### A Game of Thrones", BKT, confidence="tier-2"),
    e("mohor","lharys","ALLIES_WITH",
      "Along with [LINK] and Kurleket, Mohor is one of three Bracken men-at-arms at the inn at the crossroads.",
      "## Narrative Arc / ### A Game of Thrones", BKT),
    e("mohor","vale-mountain-clans","KILLED_BY",
      "He is slain during their first fight with members of the [LINK].",
      "## Narrative Arc / ### A Game of Thrones", BKT),
    r("mohor","kurleket","co-listed as fellow man-at-arms; ALLIES_WITH already captured via lharys edge",BKT),
    r("mohor","vale-of-arryn","geographic destination context; no residence relationship",BKT),
]
write_file(BKT, "mohor", rows)

# ── File 6: olyver-bracken ─────────────────────────────────────────────────
rows = [
    e("olyver-bracken","ice","EXECUTED_WITH",
      "the exception of Olyver, who was beheaded by Lord Stark with the [Valyrian steel] greatsword [LINK].",
      "## Origins", BKT),
    e("olyver-bracken","jaehaerys-i-targaryen","ALLIES_WITH",
      "Ser Olyver and his sworn brother of the Kingsguard, Ser Raymund Mallery, abandoned King Maegor in 48 AC when Prince [LINK] made his claim for the Iron Throne.",
      "## Origins", BKT),
    e("olyver-bracken","maegor-i-targaryen","OPPOSES",
      "Ser Olyver and his sworn brother of the Kingsguard, Ser Raymund Mallery, abandoned King [LINK] in 48 AC.",
      "## Origins", BKT),
    e("olyver-bracken","nights-watch-rebellion-of-50-ac","FIGHTS_IN",
      "in 50 AC, Olyver and Raymund [LINK] of former Faith Militant in the Watch, trying to make themselves lords of their castles.",
      "## Origins", BKT),
    e("olyver-bracken","raymund-mallery","ALLIES_WITH",
      "Ser Olyver and his sworn brother of the Kingsguard, Ser [LINK], abandoned King Maegor in 48 AC.",
      "## Origins", BKT),
    e("olyver-bracken","walton-stark-son-of-brandon","KILLED_BY",
      "with the exception of Olyver, who was beheaded by Lord [LINK] with the Valyrian steel greatsword Ice.",
      "## Origins", BKT),
    e("olyver-bracken","faith-militant","ALLIES_WITH",
      "in 50 AC, Olyver and Raymund led a rebellion of former [LINK] in the Watch.",
      "## Origins", BKT, confidence="tier-2",
      qualifier="led former Faith Militant members in rebellion"),
    e("olyver-bracken","lord-commander-of-the-nights-watch","SERVES",
      "The [LINK] gave Ser Olyver command of Rimegate and Ser Raymund command of Sable Hall.",
      "## Origins", BKT, confidence="tier-2"),
    r("olyver-bracken","iron-throne","contextual — Jaehaerys's claim, not Olyver's",BKT),
    r("olyver-bracken","lord","generic concept/title reference",BKT),
    r("olyver-bracken","sable-hall","Sable Hall assigned to Raymund, not Olyver",BKT),
    r("olyver-bracken","valyrian-steel","material descriptor for Ice; no character→material edge type",BKT),
    r("olyver-bracken","wall","geographic context of Night's Watch posting",BKT),
]
write_file(BKT, "olyver-bracken", rows)

# ── File 7: otho-bracken ──────────────────────────────────────────────────
rows = [
    e("otho-bracken","quentyn-blackwood","KILLS",
      "After slaying Lord [LINK] in 206 AC in a tourney at King's Landing, Otho became known as 'the Brute of Bracken'.",
      "## Origins", BKT),
    e("otho-bracken","lord-bracken-father-of-otho","PARENT_OF",
      "the Great Spring Sickness, which made Otho his [LINK] new heir.",
      "## Origins", BKT, qualifier="child→parent direction; Otho is the child"),
    e("otho-bracken","tourney-at-ashford-meadow","FIGHTS_IN",
      "Otho participated in the [LINK] in 209 AC.",
      "## Origins", BKT),
    e("otho-bracken","house-blackwood","OPPOSES",
      "his brown tent beneath a red stallion erected far away from the tents of [LINK].",
      "## Origins", BKT, confidence="tier-2",
      qualifier="long-standing Bracken-Blackwood feud implied"),
    e("otho-bracken","kings-landing","LOCATED_AT",
      "After slaying Lord Quentyn Blackwood in 206 AC in a tourney at [LINK], Otho became known as 'the Brute of Bracken'.",
      "## Origins", BKT),
    r("otho-bracken","209-ac","year page, not a graph node",BKT),
    r("otho-bracken","aerion-targaryen","Steffon betrayed Duncan to Aerion, not Otho; indirect",BKT),
    r("otho-bracken","blackfyre","speculative future allegiance predicted by others, never confirmed",BKT),
    r("otho-bracken","duncan-the-tall","narrative interaction — Duncan approached Otho but Otho refused; no structural edge",BKT),
    r("otho-bracken","faith-of-the-seven","quote attribution context only",BKT),
    r("otho-bracken","gormon-peake","overheard discussing Otho; no direct relationship",BKT),
    r("otho-bracken","great-spring-sickness","Otho's brother died, not Otho; establishes heir status only",BKT),
    r("otho-bracken","hedge-knight","Otho didn't know Duncan was a hedge knight — contextual rejection",BKT),
    r("otho-bracken","house-frey","speculation about future allegiance; no confirmed relationship",BKT),
    r("otho-bracken","house-lothston","speculation about future allegiance; no confirmed relationship",BKT),
    r("otho-bracken","knight","generic concept, not a specific character",BKT),
    r("otho-bracken","pearse-caron","tilted with Otho in training; too minor for structural edge",BKT),
    r("otho-bracken","sefton-staunton","predicted 'Blackwoods will never stomach Brute of Bracken'; no direct relationship",BKT),
    r("otho-bracken","septon","generic role reference",BKT),
    r("otho-bracken","steffon-fossoway","tried to recruit Otho for Duncan's trial of seven, failed; no resulting alliance",BKT),
    r("otho-bracken","tommard-heddle","discussed Otho with Gormon Peake; no direct otho relationship",BKT),
    r("otho-bracken","tourney","generic concept; specific tourney already captured",BKT),
    r("otho-bracken","trial-of-seven","concept.custom not event.*; Otho refused to participate",BKT),
    r("otho-bracken","wedding-tourney-at-whitewalls","rumored Otho might come but did not",BKT),
    r("otho-bracken","whitewalls","location context of tourney Otho didn't attend",BKT),
    r("otho-bracken","duncan-the-tall","Quotes section — just quote attribution",BKT),
]
write_file(BKT, "otho-bracken", rows)

# ── File 8: raylon-rivers ──────────────────────────────────────────────────
rows = [
    e("raylon-rivers","amos-bracken","SIBLING_OF",
      "Ser [LINK] was slain during the Battle of the Burning Mill, after which his half-brother Raylon led survivors back.",
      "## Origins", BKT, qualifier="half-sibling"),
    e("raylon-rivers","battle-of-the-burning-mill","FIGHTS_IN",
      "Ser Amos Bracken was slain during the [LINK], after which his half-brother Raylon led survivors back toward Stone Hedge.",
      "## Origins", BKT),
    e("raylon-rivers","daemon-targaryen","OPPOSES",
      "Prince [LINK] had taken Stone Hedge and Lord Humfrey Bracken in the meantime.",
      "## Origins", BKT, confidence="tier-2",
      qualifier="House Bracken declared for Greens; Daemon was Black"),
    e("raylon-rivers","taking-of-stone-hedge","FIGHTS_IN",
      "Prince Daemon Targaryen had [LINK] and Lord Humfrey Bracken in the meantime.",
      "## Origins", BKT),
    r("raylon-rivers","dance-of-the-dragons","war context already covered by specific battle edges",BKT),
    r("raylon-rivers","stone-hedge","travel destination during retreat; no established residence relationship",BKT),
]
write_file(BKT, "raylon-rivers", rows)

# ── File 9: benjicot-branch ───────────────────────────────────────────────
BKT = "characters-house-branch"
rows = [
    e("benjicot-branch","stannis-baratheon","SERVES",
      "Benjicot is one of the men of the wolfswood that Lady Sybelle Glover sends with King [LINK] as hunters and scouts.",
      "## Narrative Arc / ### A Dance with Dragons", BKT),
    e("benjicot-branch","sybelle-glover","SERVES",
      "Benjicot is one of the men of the wolfswood that Lady [LINK] sends with King Stannis Baratheon as hunters and scouts.",
      "## Narrative Arc / ### A Dance with Dragons", BKT),
    e("benjicot-branch","crofters-village","LOCATED_AT",
      "a blizzard strands the army at a [LINK] for weeks.",
      "## Narrative Arc / ### A Dance with Dragons", BKT),
    e("benjicot-branch","winterfell","LOCATED_AT",
      "to lead his army to [LINK]. He kills a scrawny hart that is made into venison stew for Stannis's table.",
      "## Narrative Arc / ### A Dance with Dragons", BKT, confidence="tier-2",
      qualifier="destination of march; army stranded en route"),
]
write_file(BKT, "benjicot-branch", rows)

# ── File 10: andros-brax ─────────────────────────────────────────────────
BKT = "characters-house-brax"
rows = [
    e("andros-brax","battle-of-the-camps","FIGHTS_IN",
      "When Ser Brynden Tully leads a surprise attack in the [LINK], Lord Brax tries to cross the Tumblestone on rafts.",
      "## Narrative Arc / ### A Game of Thrones", BKT),
    e("andros-brax","brynden-tully","KILLED_BY",
      "They came under attack by a force led by Ser [LINK]; Andros drowned under the weight of his armor.",
      "## Narrative Arc / ### A Game of Thrones", BKT, confidence="tier-2",
      qualifier="Brynden's attack caused Andros to drown"),
    e("andros-brax","jaime-lannister","SERVES",
      "During Ser [LINK]'s siege of Riverrun, Andros commands the western camp.",
      "## Narrative Arc / ### A Game of Thrones", BKT),
    e("andros-brax","catelyn-stark","ALLIES_WITH",
      "visited Riverrun in hopes of making an offer for the hand of [LINK] or Lysa Tully for one of his sons.",
      "## Origins", BKT, confidence="tier-3",
      qualifier="sought marriage alliance with Tullys; proposal never consummated"),
    r("andros-brax","lysa-arryn","same as catelyn — marriage proposal not consummated; covered by catelyn edge at tier-3",BKT),
    r("andros-brax","red-fork","geographic feature, crossing context",BKT),
    r("andros-brax","trident","geographic feature",BKT),
    r("andros-brax","tumblestone","geographic feature where Andros drowned; DIED_AT requires place node, tumblestone is place.location but drowning mechanism not an edge",BKT),
]
write_file(BKT, "andros-brax", rows)

# ── File 11: flement-brax ────────────────────────────────────────────────
rows = [
    # Appearances (reject all material/creature refs)
    r("flement-brax","amethyst","armor decoration; no character→material edge type",BKT),
    r("flement-brax","horse","helmet design; descriptive",BKT),
    r("flement-brax","silver","armor material; no character→material edge",BKT),
    r("flement-brax","unicorn","house sigil on shield; descriptive",BKT),
    # ACOK
    e("flement-brax","battle-of-the-fords","FIGHTS_IN",
      "Ser Flement is among Lord Tywin's army as it attempts to cross the Red Fork of the Trident, leading to the [LINK].",
      "## Narrative Arc / ### A Clash of Kings", BKT),
    e("flement-brax","tywin-lannister","SERVES",
      "Ser Flement is among Lord [LINK]'s army as it attempts to cross the Red Fork of the Trident.",
      "## Narrative Arc / ### A Clash of Kings", BKT),
    r("flement-brax","house-lannister","organizational membership covered by SERVES tywin-lannister",BKT),
    r("flement-brax","house-mallister","House Mallister repulsed Flement's crossing; OPPOSES too strong for single tactical repulse",BKT),
    r("flement-brax","red-fork","geographic feature",BKT),
    r("flement-brax","riverrun","siege location context",BKT),
    r("flement-brax","scorpion-weapon","military equipment context, not a relationship",BKT),
    r("flement-brax","trident","geographic feature",BKT),
    # AFFC
    e("flement-brax","harrenhal","LOCATED_AT",
      "While at [LINK], Flement engages in a training fight with Ser Lyle Crakehall in the yard.",
      "## Narrative Arc / ### A Feast for Crows", BKT),
    e("flement-brax","hayford","LOCATED_AT",
      "He joins Jaime and others for supper at [LINK] on the first night of their ride.",
      "## Narrative Arc / ### A Feast for Crows", BKT),
    e("flement-brax","jaime-lannister","SERVES",
      "Ser Flement leads two hundred heavy horse that are part of Ser [LINK]'s force to take Riverrun.",
      "## Narrative Arc / ### A Feast for Crows", BKT),
    e("flement-brax","siege-of-riverrun","FIGHTS_IN",
      "Ser Flement leads two hundred heavy horse that are part of Ser Jaime Lannister's force to [LINK].",
      "## Narrative Arc / ### A Feast for Crows", BKT),
    r("flement-brax","lyle-crakehall","training sparring match; no structural edge",BKT),
    r("flement-brax","wine","incidental spill context; no relationship",BKT),
    # AGOT
    e("flement-brax","addam-marbrand","SERVES",
      "Flement rides under the command of Ser [LINK] in the right flank during the battle on the Green Fork.",
      "## Narrative Arc / ### A Game of Thrones", BKT),
    e("flement-brax","battle-of-the-camps","FIGHTS_IN",
      "News arrives at Lord Tywin's camp of the defeat of the Lannister forces in the [LINK]. The messenger was part of Lord Andros Brax's camp.",
      "## Narrative Arc / ### A Game of Thrones", BKT, confidence="tier-2"),
    e("flement-brax","battle-on-the-green-fork","FIGHTS_IN",
      "Flement rides under the command of Ser Addam Marbrand in the right flank during the [LINK].",
      "## Narrative Arc / ### A Game of Thrones", BKT),
    e("flement-brax","tytos-brax","SIBLING_OF",
      "Flement's older brother, [LINK], becomes the new Lord of Hornvale.",
      "## Narrative Arc / ### A Game of Thrones", BKT),
    e("flement-brax","inn-at-the-crossroads","LOCATED_AT",
      "Flement tells Tyrion that Lord Tywin has taken the [LINK] for his quarters, leading Tyrion there.",
      "## Narrative Arc / ### A Game of Thrones", BKT),
    r("flement-brax","brynden-tully","attacked Andros's force; Flement was in north camp, not direct combatant",BKT),
    r("flement-brax","hand-of-the-king","contextual about Tyrion's appointment; not flement's relationship",BKT),
    r("flement-brax","house-lannister","duplicate of SERVES edge above",BKT),
    r("flement-brax","kings-landing","contextual mention of Hand position location",BKT),
    r("flement-brax","lord-of-hornvale","title held by Tytos; not Flement's",BKT),
    r("flement-brax","riverlands","geographic region context",BKT),
    r("flement-brax","tumblestone","Andros's crossing; Flement was elsewhere",BKT),
    r("flement-brax","tyrion-lannister","challenged Tyrion's party but Tyrion is Lannister ally; no opposition edge",BKT),
    r("flement-brax","vale-mountain-clans","Tyrion's companions at the time; not a flement relationship",BKT),
    # ASOS
    r("flement-brax","dorne","geographic context for Oberyn's arrival",BKT),
    r("flement-brax","hornvale","Flement is heir to Hornvale but not yet lord; no RULES edge; HEIR_TO → title not place",BKT),
    r("flement-brax","joffrey-baratheon","witness at trial; no structural relationship",BKT),
    r("flement-brax","kings-landing","location context (duplicate)",BKT),
    r("flement-brax","oberyn-martell","part of welcoming delegation; too minor for structural edge",BKT),
    r("flement-brax","purple-wedding","trial context; Flement testified",BKT),
    r("flement-brax","tyrion-lannister","delegation and trial contexts; no structural relationship",BKT),
    # Quotes
    r("flement-brax","amethyst","quote about armor description",BKT),
    r("flement-brax","horse","quote about helmet",BKT),
    r("flement-brax","jaime-lannister","quote attribution only",BKT),
    r("flement-brax","silver","quote about armor description",BKT),
    r("flement-brax","tyrion-lannister","quote attribution only",BKT),
    r("flement-brax","tyrion-lannister","quote attribution (duplicate)",BKT),
    r("flement-brax","tyrion-lannister","quote attribution (duplicate)",BKT),
    r("flement-brax","unicorn","quote about shield sigil",BKT),
    r("flement-brax","vale-mountain-clans","quote attribution",BKT),
]
write_file(BKT, "flement-brax", rows)

# ── File 12: robert-brax ────────────────────────────────────────────────
rows = [
    e("robert-brax","battle-of-the-fords","FIGHTS_IN",
      "Robert is slain at the [LINK].",
      "## Narrative Arc / ### A Storm of Swords", BKT),
]
write_file(BKT, "robert-brax", rows)

# ── File 13: rupert-brax ────────────────────────────────────────────────
rows = [
    e("rupert-brax","battle-of-oxcross","FIGHTS_IN",
      "Ser Rupert is killed at the [LINK].",
      "## Narrative Arc / ### A Clash of Kings", BKT),
]
write_file(BKT, "rupert-brax", rows)

# ── File 14: tytos-brax ─────────────────────────────────────────────────
rows = [
    # ACOK
    e("tytos-brax","battle-of-the-blackwater","FIGHTS_IN",
      "A Brax is among the western lords present at King Joffrey's first audience after the [LINK].",
      "## Narrative Arc / ### A Clash of Kings", BKT, confidence="tier-3",
      qualifier="'A Brax' — may be Tytos; uncertainty noted"),
    e("tytos-brax","joffrey-baratheon","SERVES",
      "A Brax is among the western lords present at King [LINK]'s first audience in King's Landing.",
      "## Narrative Arc / ### A Clash of Kings", BKT, confidence="tier-2"),
    e("tytos-brax","kings-landing","LOCATED_AT",
      "A Brax is among the western lords present at King Joffrey's first audience in [LINK].",
      "## Narrative Arc / ### A Clash of Kings", BKT, confidence="tier-2"),
    r("tytos-brax","house-stark","speculative — may have been ransomed by House Stark; no confirmed relationship",BKT),
    # AFFC
    e("tytos-brax","casterly-rock","LOCATED_AT",
      "Tytos is among the gathered nobility that escorts the corpse of Lord Tywin Lannister back to [LINK].",
      "## Narrative Arc / ### A Feast for Crows", BKT),
    e("tytos-brax","jaime-lannister","ALLIES_WITH",
      "Tytos is among the gathered nobility that escorts the corpse of Lord Tywin Lannister back to Casterly Rock. Ser [LINK] thinks Lord Brax could deal with the outlaws.",
      "## Narrative Arc / ### A Feast for Crows", BKT),
    e("tytos-brax","tywin-lannister","SERVES",
      "Tytos is among the gathered nobility that escorts the corpse of Lord [LINK] back to Casterly Rock.",
      "## Narrative Arc / ### A Feast for Crows", BKT),
    r("tytos-brax","beric-dondarrion","Jaime's assessment of Brax's usefulness; no direct relationship",BKT),
    r("tytos-brax","hand-of-the-king","Jaime's musing about Hand candidates; Tytos mentioned but not a direct relationship",BKT),
    r("tytos-brax","sandor-clegane","Jaime's musing; no direct tytos→sandor relationship",BKT),
    # AGOT
    e("tytos-brax","battle-in-the-whispering-wood","FIGHTS_IN",
      "Ser Tytos is a member of the Lannister host besieging Riverrun, but he is captured at the [LINK].",
      "## Narrative Arc / ### A Game of Thrones", BKT),
    e("tytos-brax","house-lannister","MEMBER_OF",
      "Ser Tytos is a member of the [LINK] host besieging Riverrun.",
      "## Narrative Arc / ### A Game of Thrones", BKT),
    r("tytos-brax","battle-of-the-camps","about Andros Brax's death, not Tytos directly",BKT),
    r("tytos-brax","riverrun","siege location context",BKT),
    # ASOS
    e("tytos-brax","flement-brax","SIBLING_OF",
      "His younger brother, Ser [LINK], is his heir.",
      "## Narrative Arc / ### A Storm of Swords", BKT),
    e("tytos-brax","hornvale","RULES",
      "Previously a captive at the Twins, Tytos has become the new Lord of [LINK].",
      "## Narrative Arc / ### A Storm of Swords", BKT),
    e("tytos-brax","twins","LOCATED_AT",
      "Previously a captive at the [LINK], Tytos has become the new Lord of Hornvale.",
      "## Narrative Arc / ### A Storm of Swords", BKT,
      qualifier="held as captive at the Twins"),
]
write_file(BKT, "tytos-brax", rows)

# ── File 15: edmund-breakstone ───────────────────────────────────────────
BKT2 = "characters-house-breakstone"
rows = [
    e("edmund-breakstone","gates-of-the-moon","LOCATED_AT",
      "Ser Edmund has traveled to the [LINK] to participate in the tourney to select the membership of the Brotherhood of Winged Knights.",
      "## Narrative Arc / ### The Winds of Winter", BKT2),
    e("edmund-breakstone","nestor-royce","GUEST_OF",
      "Ser Edmund comments that their host, Lord [LINK], has an open hand.",
      "## Narrative Arc / ### The Winds of Winter", BKT2),
    e("edmund-breakstone","brotherhood-of-winged-knights","ALLIES_WITH",
      "Ser Edmund has traveled to the Gates of the Moon to participate in the tourney to select the membership of the [LINK].",
      "## Narrative Arc / ### The Winds of Winter", BKT2, confidence="tier-3",
      qualifier="competing to join; membership outcome not confirmed"),
]
write_file(BKT2, "edmund-breakstone", rows)

# ── File 16: ella-broome ─────────────────────────────────────────────────
BKT3 = "characters-house-broome"
rows = [
    e("ella-broome","alysanne-targaryen","SERVES",
      "she became a lady-in-waiting to his wife, Queen [LINK].",
      "## Origins", BKT3),
    r("ella-broome","jaehaerys-i-targaryen","briefly offered as a match; marriage never happened; no established relationship",BKT3),
]
write_file(BKT3, "ella-broome", rows)

# ── File 17: lucinda-tully ───────────────────────────────────────────────
rows = [
    e("lucinda-tully","faith-of-the-seven","WORSHIPS",
      "The redoubtable Lucinda was famous for her piety to the [LINK].",
      "## Appearances & Description", BKT3),
    e("lucinda-tully","alysanne-targaryen","SERVES",
      "Dowager Queen Alyssa Velaryon sent Lucinda to take charge of [LINK]'s household at Dragonstone.",
      "## Origins", BKT3),
    e("lucinda-tully","alyssa-velaryon","SERVES",
      "Dowager Queen [LINK] sent Lucinda to take charge of Alysanne's household at Dragonstone.",
      "## Origins", BKT3, confidence="tier-2"),
    e("lucinda-tully","dragonstone","LOCATED_AT",
      "Dowager Queen Alyssa Velaryon sent Lucinda to take charge of Alysanne's household at [LINK].",
      "## Origins", BKT3),
    e("lucinda-tully","kings-landing","LOCATED_AT",
      "When Prentys was called to serve as master of laws for Jaehaerys in 49 AC, Lucinda accompanied her husband to [LINK].",
      "## Origins", BKT3),
    e("lucinda-tully","maegor-i-targaryen","OPPOSES",
      "from Riverrun, was one of the first great lords to abandon King [LINK].",
      "## Origins", BKT3, confidence="tier-2",
      qualifier="Lucinda's house abandoned Maegor; Lucinda's position inferred"),
    e("lucinda-tully","myles-smallwood","ALLIES_WITH",
      "Lucinda and Prentys supported his replacement by [LINK], Lord of Acorn Hall.",
      "## Origins", BKT3),
    r("lucinda-tully","shivers","no DIED_OF edge type in vocabulary; disease-death relationship not representable",BKT3),
    r("lucinda-tully","acorn-hall","Myles Smallwood's seat; not Lucinda's location",BKT3),
    r("lucinda-tully","daemon-velaryon-son-of-aethan","Lucinda opposed his replacement as Hand; OPPOSES too strong for political support of successor",BKT3),
    r("lucinda-tully","ella-broome","complex sister/sister-in-law relationship; no clean kinship type determinable",BKT3),
    r("lucinda-tully","faith-militant","Lucinda supported Faith Militant's reinstatement; ALLIES_WITH requires more than advocacy",BKT3),
    r("lucinda-tully","hand-of-the-king","title, not a character; contextual",BKT3),
    r("lucinda-tully","iron-throne","contextual — Faith Militant outlawed by the Iron Throne",BKT3),
    r("lucinda-tully","jaehaerys-i-targaryen","refused her request to reinstate Faith Militant; no allegiance edge",BKT3),
    r("lucinda-tully","joffrey-doggett","Lucinda supported his activities indirectly; too indirect for edge",BKT3),
    r("lucinda-tully","lord-justiciar","Prentys's title, not Lucinda's",BKT3),
    r("lucinda-tully","lord-of-storms-end","Rogar's title; contextual",BKT3),
    r("lucinda-tully","master-of-laws","Prentys's title, not Lucinda's",BKT3),
    r("lucinda-tully","riverlands","geographic region context",BKT3),
    r("lucinda-tully","rogar-baratheon","wanted Lucinda's influence; no direct relationship",BKT3),
    r("lucinda-tully","small-council","Prentys dismissed from small council; Lucinda's relationship is through her husband",BKT3),
    r("lucinda-tully","westerlands","geographic region context",BKT3),
]
write_file(BKT3, "lucinda-tully", rows)

# ── File 18: walter-brownhill ────────────────────────────────────────────
BKT4 = "characters-house-brownhill"
rows = [
    e("walter-brownhill","cape-wrath","RULES",
      "Ser Walter ruled a few hides of land on [LINK] from a castle described as being made of 'mud and tree roots'.",
      "## Origins", BKT4),
    r("walter-brownhill","aegon-iii-targaryen","Cassandra Baratheon attempted to poison the king; Walter married Cassandra as punishment — indirect relationship",BKT4),
    r("walter-brownhill","daenaera-velaryon","same context as aegon-iii; Cassandra's target, not Walter's direct relationship",BKT4),
    r("walter-brownhill","elenda-baratheon","arranged Walter's marriage to Cassandra; no direct relationship to Walter",BKT4),
    r("walter-brownhill","lorent-grandison","arranged Walter's marriage to Cassandra; no direct relationship to Walter",BKT4),
    r("walter-brownhill","poison","concept; no applicable edge type from character to poison",BKT4),
]
write_file(BKT4, "walter-brownhill", rows)

# ── File 19: lothor-brune ────────────────────────────────────────────────
BKT5 = "characters-house-brune-of-brownhollow"
rows = [
    # Appearances
    e("lothor-brune","petyr-baelish","SERVES",
      "Sansa considers Lothor to be honest, and [LINK] deems him to be loyal.",
      "## Appearances & Description", BKT5),
    e("lothor-brune","sansa-stark","ALLIES_WITH",
      "[LINK] thinks that Lothor is not handsome, but also not ugly.",
      "## Appearances & Description", BKT5, confidence="tier-2",
      qualifier="Lothor repeatedly protects and assists Sansa"),
    # ACOK
    e("lothor-brune","battle-of-the-blackwater","FIGHTS_IN",
      "Lothor fights on behalf of Joffrey during the [LINK], cutting his way through House Fossoway men-at-arms.",
      "## Narrative Arc / ### A Clash of Kings", BKT5),
    e("lothor-brune","bryan-fossoway","KILLS",
      "to capture Ser Jon Fossoway and kill Ser [LINK] and Ser Edwyd Fossoway.",
      "## Narrative Arc / ### A Clash of Kings", BKT5),
    e("lothor-brune","edwyd-fossoway","KILLS",
      "to capture Ser Jon Fossoway and kill Ser Bryan and Ser [LINK], earning him the nickname 'Lothor Apple-Eater'.",
      "## Narrative Arc / ### A Clash of Kings", BKT5),
    e("lothor-brune","jon-fossoway","CAPTURES",
      "cutting his way through House Fossoway men-at-arms to capture Ser [LINK].",
      "## Narrative Arc / ### A Clash of Kings", BKT5),
    e("lothor-brune","tourney-on-king-joffreys-name-day","FIGHTS_IN",
      "Lothor is in the lists for the [LINK].",
      "## Narrative Arc / ### A Clash of Kings", BKT5),
    r("lothor-brune","apple","etymology of nickname; no structural relationship",BKT5),
    r("lothor-brune","dontos-hollard","tilt called off due to Dontos being drunk; no combat result",BKT5),
    r("lothor-brune","knight","concept — knighthood awarded; no character→concept edge",BKT5),
    r("lothor-brune","riverlands","future grant location; no present residence",BKT5),
    r("lothor-brune","war-of-the-five-kings","general war context",BKT5),
    # AFFC
    e("lothor-brune","gates-of-the-moon","LOCATED_AT",
      "Lord Robert is reluctant to leave the Eyrie when it is time to descend to the [LINK].",
      "## Narrative Arc / ### A Feast for Crows", BKT5),
    e("lothor-brune","giants-lance","LOCATED_AT",
      "Ossy helps the knight descend the [LINK] to the Gates of the Moon.",
      "## Narrative Arc / ### A Feast for Crows", BKT5),
    e("lothor-brune","lyn-corbray","OPPOSES",
      "When Ser [LINK] draws Lady Forlorn, Lothor goes for his own sword.",
      "## Narrative Arc / ### A Feast for Crows", BKT5, confidence="tier-2"),
    e("lothor-brune","lords-declarant","OPPOSES",
      "During the parley with the [LINK], Ser Lothor stands at the door of Petyr's solar, ready to defend.",
      "## Narrative Arc / ### A Feast for Crows", BKT5, confidence="tier-2"),
    r("lothor-brune","bastard","generic concept",BKT5),
    r("lothor-brune","colemon","Lothor sought Sansa for help; no direct lothor→colemon edge",BKT5),
    r("lothor-brune","gates-of-the-moon","duplicate candidate (second section reference)",BKT5),
    r("lothor-brune","lady-forlorn","Lyn's sword; Lothor reacted to it but no lothor→sword relationship",BKT5),
    r("lothor-brune","mord","loading supplies together; too minor for structural edge",BKT5),
    r("lothor-brune","mya-stone","Sansa's inference that Lothor fancies Mya; not a confirmed relationship edge",BKT5),
    r("lothor-brune","myranda-royce","quote attribution context",BKT5),
    r("lothor-brune","ossy","working together briefly; too minor",BKT5),
    r("lothor-brune","robert-arryn","Lothor locked Robert in room at Sansa's request; no structural relationship",BKT5),
    r("lothor-brune","solar","Petyr's solar location context",BKT5),
    r("lothor-brune","weirwood","caught Robert who slipped from weirwood throne; contextual",BKT5),
    # AGOT
    e("lothor-brune","jory-cassel","DEFEATS",
      "He defeats [LINK] on a judgment by King Robert I Baratheon.",
      "## Narrative Arc / ### A Game of Thrones", BKT5),
    e("lothor-brune","kings-landing","LOCATED_AT",
      "Lothor takes part in the Hand's tourney in [LINK] as a freerider.",
      "## Narrative Arc / ### A Game of Thrones", BKT5),
    e("lothor-brune","robar-royce","DUELS",
      "ties with Ser Aron Santagar, and finally loses to Ser [LINK].",
      "## Narrative Arc / ### A Game of Thrones", BKT5),
    r("lothor-brune","aron-santagar","tied with Aron in tournament; DUELS is symmetric but covered by main joust result",BKT5),
    r("lothor-brune","robert-i-baratheon","King Robert judged the tourney; no specific relationship to Lothor",BKT5),
    # ASOS
    e("lothor-brune","dontos-hollard","KILLS",
      "Taking orders from Petyr, Lothor commands the crossbowmen on Merling King who kill Ser [LINK].",
      "## Narrative Arc / ### A Storm of Swords", BKT5),
    e("lothor-brune","drearfort","LOCATED_AT",
      "Following the wedding feast of Lysa Arryn and Petyr at the [LINK], Lothor protects Sansa.",
      "## Narrative Arc / ### A Storm of Swords", BKT5),
    e("lothor-brune","eyrie","LOCATED_AT",
      "Upon his arrival at the [LINK], Lord Baelish dismisses the captain of the House Arryn guards.",
      "## Narrative Arc / ### A Storm of Swords", BKT5),
    e("lothor-brune","fingers","LOCATED_AT",
      "Lothor and Oswell Kettleblack row Petyr and Sansa to the shore when Merling King arrives at the [LINK].",
      "## Narrative Arc / ### A Storm of Swords", BKT5),
    e("lothor-brune","house-arryn-guards","COMMANDS",
      "Lord Baelish dismisses the captain of the [LINK], Ser Marwyn Belmore, and names Lothor as his replacement.",
      "## Narrative Arc / ### A Storm of Swords", BKT5),
    e("lothor-brune","marillion","OPPOSES",
      "Lothor protects Sansa, now under the alias 'Alayne Stone', from the unwanted advances of the singer [LINK].",
      "## Narrative Arc / ### A Storm of Swords", BKT5),
    r("lothor-brune","lysa-arryn","context of Petyr's marriage; no direct lothor→lysa relationship",BKT5),
    r("lothor-brune","marwyn-belmore","Lothor replaced Marwyn; no direct relationship beyond succession",BKT5),
    r("lothor-brune","master-of-coin","Petyr's title; contextual",BKT5),
    r("lothor-brune","merling-king","the ship; no applicable lothor→ship edge type",BKT5),
    r("lothor-brune","oswell-kettleblack","co-participant in rowing scene; too minor for structural edge",BKT5),
    r("lothor-brune","petyr-baelish","duplicate SERVES candidate (already emitted from Appearances)",BKT5),
    r("lothor-brune","purple-wedding","context of Dontos's death",BKT5),
    r("lothor-brune","red-keep","location where Sansa departed from; contextual",BKT5),
    r("lothor-brune","sansa-stark","duplicate candidate (already emitted from Appearances)",BKT5),
    r("lothor-brune","wedding-of-petyr-baelish-and-lysa-arryn","wedding context; no lothor→wedding edge",BKT5),
    # WINDS
    r("lothor-brune","harrold-hardyng","Lothor dismisses Harrold verbally; too minor for OPPOSES",BKT5),
    r("lothor-brune","m-l-e-at-runestone","Lothor refers to it derisively; no relationship",BKT5),
    # Quotes (all rejections)
    r("lothor-brune","bastard","quote context",BKT5),
    r("lothor-brune","battle-of-the-blackwater","duplicate quote reference",BKT5),
    r("lothor-brune","kings-landing","quote context (duplicate)",BKT5),
    r("lothor-brune","knight","quote context",BKT5),
    r("lothor-brune","mya-stone","quote about potential match; not confirmed relationship",BKT5),
    r("lothor-brune","mya-stone","quote (duplicate)",BKT5),
    r("lothor-brune","myranda-royce","quote attribution",BKT5),
    r("lothor-brune","nestor-royce","Myranda's father mentioned in quote context",BKT5),
    r("lothor-brune","oswell-kettleblack","quote context about Oswell rowing",BKT5),
    r("lothor-brune","petyr-baelish","quote attribution (duplicate)",BKT5),
    r("lothor-brune","petyr-baelish","quote attribution (duplicate)",BKT5),
    r("lothor-brune","purple-wedding","quote context",BKT5),
    r("lothor-brune","sansa-stark","quote attribution (duplicate)",BKT5),
    r("lothor-brune","sansa-stark","quote attribution (duplicate)",BKT5),
    r("lothor-brune","sansa-stark","quote attribution (duplicate)",BKT5),
    r("lothor-brune","sansa-stark","quote attribution (duplicate)",BKT5),
    r("lothor-brune","harrold-hardyng","quote attribution",BKT5),
    r("lothor-brune","m-l-e-at-runestone","quote reference",BKT5),
    r("lothor-brune","marillion","quote attribution",BKT5),
    r("lothor-brune","petyr-baelish","quote attribution (duplicate)",BKT5),
    r("lothor-brune","sansa-stark","quote attribution (duplicate)",BKT5),
    r("lothor-brune","sansa-stark","quote attribution (duplicate)",BKT5),
]
write_file(BKT5, "lothor-brune", rows)

# ── File 20: eustace-brune ───────────────────────────────────────────────
BKT6 = "characters-house-brune-of-the-dyre-den"
rows = [
    e("eustace-brune","dyre-den","RULES",
      "Dick Crabb claims to have some knowledge of Lord Eustace as he guides Brienne and Podrick past the [LINK].",
      "## Narrative Arc / ### A Feast for Crows", BKT6, confidence="tier-2",
      qualifier="Lord of Dyre Den inferred from House name and context"),
    r("eustace-brune","bennard-brune","COUSIN_OF not in edge vocabulary — filing vocab-gap separately",BKT6),
    r("eustace-brune","knight-of-brownhollow","title held by Bennard, not Eustace",BKT6),
    r("eustace-brune","brienne-tarth","Dick Crabb guides Brienne past Dyre Den; Brienne does not interact directly with Eustace",BKT6),
    r("eustace-brune","dick-crabb","Dick claims knowledge of Eustace; no direct relationship",BKT6),
    r("eustace-brune","podrick-payne","guided past Dyre Den with Brienne; no direct relationship to Eustace",BKT6),
    r("eustace-brune","war-of-the-five-kings","Eustace's descendants went to war; no direct eustace→war edge",BKT6),
]
write_file(BKT6, "eustace-brune", rows)

# ── File 21: bernarr-brune ───────────────────────────────────────────────
BKT7 = "characters-house-brune"
rows = [
    e("bernarr-brune","alyn-stokeworth","SERVES",
      "Bernarr was the squire of Lord [LINK], who was the Hand of the King for the newly crowned King Aenys I Targaryen.",
      "## Origins", BKT7),
    e("bernarr-brune","aenys-i-targaryen","SERVES",
      "Bernarr avenged him by killing Harren. Bernarr was rewarded with a knighthood by the grateful King [LINK].",
      "## Origins", BKT7, confidence="tier-2"),
    e("bernarr-brune","harren-the-red","KILLS",
      "When Lord Alyn was slain by the rebel [LINK], Bernarr avenged him by killing Harren.",
      "## Origins", BKT7),
    e("bernarr-brune","maegor-i-targaryen","ALLIES_WITH",
      "Ser Bernarr spoke out, offering to stand beside King [LINK], and noting that all present were no true knights.",
      "## Origins", BKT7),
    e("bernarr-brune","visenyas-hill","LOCATED_AT",
      "In 42 AC, Ser Bernarr was present at [LINK] when King Maegor I Targaryen was challenged.",
      "## Origins", BKT7),
    e("bernarr-brune","warriors-sons","OPPOSES",
      "the Warrior's Sons, to a trial of seven... Ser Bernarr spoke out, offering to stand beside King Maegor.",
      "## Origins", BKT7),
    r("bernarr-brune","damon-morrigen","Damon challenged Maegor; Bernarr's opposition is to Warriors Sons, not Damon specifically",BKT7),
    r("bernarr-brune","dick-bean","Dick Bean shamed Bernarr into action; incidental character",BKT7),
    r("bernarr-brune","grand-captain","Damon Morrigen's title; not about Bernarr",BKT7),
    r("bernarr-brune","hand-of-the-king","Alyn Stokeworth's title; not Bernarr's",BKT7),
    r("bernarr-brune","iron-throne","contextual — Maegor's legitimacy claim",BKT7),
    r("bernarr-brune","knight","concept — knighthood; no character→concept edge",BKT7),
    r("bernarr-brune","man-at-arms","Dick Bean described as man-at-arms; not about Bernarr",BKT7),
    r("bernarr-brune","squire","Bernarr's former role as squire; concept not a character",BKT7),
    r("bernarr-brune","trial-of-seven","concept.custom not event.*",BKT7),
    r("bernarr-brune","true-knight","concept; no character→concept edge",BKT7),
    r("bernarr-brune","dick-bean","Quotes — 'This bean shames us all'; quote context only",BKT7),
    r("bernarr-brune","true-knight","Quotes — concept in quote",BKT7),
]
write_file(BKT7, "bernarr-brune", rows)

# ── File 22: brus-buckler ─────────────────────────────────────────────────
BKT8 = "characters-house-buckler"
rows = [
    e("brus-buckler","stannis-baratheon","SERVES",
      "Brus is one of the queen's men in the service of King [LINK].",
      "## Narrative Arc / ### A Dance with Dragons", BKT8),
    e("brus-buckler","selyse-florent","SERVES",
      "Brus stays with Queen [LINK] at Eastwatch-by-the-Sea as one of her protectors.",
      "## Narrative Arc / ### A Dance with Dragons", BKT8),
    e("brus-buckler","gerrick-kingsbloods-second-daughter","BETROTHED_TO",
      "Selyse arranges for Brus to wed the [LINK] of Gerrick Kingsblood.",
      "## Narrative Arc / ### A Dance with Dragons", BKT8),
    e("brus-buckler","eastwatch-by-the-sea","LOCATED_AT",
      "Brus stays with Queen Selyse at [LINK] as one of her protectors.",
      "## Narrative Arc / ### A Dance with Dragons", BKT8),
    e("brus-buckler","wun-weg-wun-dar-wun","FEARS",
      "Brus is nervous after hearing that [LINK] is a guest of the Night's Watch.",
      "## Narrative Arc / ### A Dance with Dragons", BKT8, confidence="tier-2"),
    r("brus-buckler","battle-beneath-the-wall","anchor text is 'Castle Black' but target is battle event; Brus stayed at Eastwatch, did not fight",BKT8),
    r("brus-buckler","fight-by-deepwood-motte","Brus stayed with Selyse at Eastwatch while Stannis went to Deepwood Motte",BKT8),
    r("brus-buckler","gerrick-kingsblood","relationship to Gerrick covered by betrothal to his daughter",BKT8),
    r("brus-buckler","nightfort","Brus accompanied Selyse to Castle Black; Nightfort is nearby but not Brus's specific location",BKT8),
    r("brus-buckler","nights-watch","Brus is nervous about Wun Wun being a guest; no MEMBER_OF or ALLIED_WITH relationship",BKT8),
    r("brus-buckler","shireen-baratheon","gave Shireen first dance at wedding; too minor for structural edge",BKT8),
    r("brus-buckler","wedding-of-sigorn-and-alys-karstark","social attendance; no structural relationship",BKT8),
]
write_file(BKT8, "brus-buckler", rows)

# ── File 23: cedrik-storm ────────────────────────────────────────────────
rows = [
    e("cedrik-storm","barristan-selmy","KILLED_BY",
      "In the White Book, Ser [LINK]'s victory over Cedrik is recorded.",
      "## Origins", BKT8, confidence="tier-2",
      qualifier="White Book records Barristan's victory over Cedrik; death inferred from context"),
    r("cedrik-storm","white-book","record book; no applicable character→book edge type",BKT8),
]
write_file(BKT8, "cedrik-storm", rows)

# ── File 24: lady-buckler ────────────────────────────────────────────────
rows = [
    e("lady-buckler","kings-landing","LOCATED_AT",
      "Lady Buckler came to [LINK] with her two daughters, hoping that one of the two maidens would be chosen.",
      "## Origins", BKT8),
    e("lady-buckler","maidens-day-ball","FIGHTS_IN",
      "In 133 AC, the [LINK] was held at the Red Keep to find a second wife and new queen for King Aegon III Targaryen. Lady Buckler came to King's Landing.",
      "## Origins", BKT8,
      qualifier="FIGHTS_IN is the vocabulary type for event participation; event.battle type"),
    r("lady-buckler","aegon-iii-targaryen","Lady Buckler hoped her daughter would be chosen; no direct lady-buckler→king relationship",BKT8),
    r("lady-buckler","hand-of-the-king","Unwin Peake's title; contextual",BKT8),
    r("lady-buckler","myrielle-peake","Unwin's daughter, rival candidate; no direct relationship",BKT8),
    r("lady-buckler","red-keep","location of Maiden's Day Ball; covered by LOCATED_AT kings-landing",BKT8),
    r("lady-buckler","unwin-peake","possibly orchestrated the drowning; no confirmed direct relationship with Lady Buckler",BKT8),
    r("lady-buckler","watercraft","the boat she drowned in; no applicable character→object edge",BKT8),
]
write_file(BKT8, "lady-buckler", rows)

# ── File 25: lord-buckler ─────────────────────────────────────────────────
rows = [
    e("lord-buckler","aegon-ii-targaryen","OPPOSES",
      "Lord Buckler was arrested and put in the Red Keep's dungeons by [LINK]'s supporters for supporting his half-sister, Princess Rhaenyra.",
      "## Origins", BKT8),
    e("lord-buckler","dance-of-the-dragons","FIGHTS_IN",
      "At the start of the [LINK], Lord Buckler was arrested and put in the Red Keep's dungeons.",
      "## Origins", BKT8),
    e("lord-buckler","rhaenyra-targaryen","ALLIES_WITH",
      "Lord Buckler was arrested by Aegon II's supporters for supporting his half-sister, Princess [LINK].",
      "## Origins", BKT8),
    r("lord-buckler","kings-justice","Lord Buckler chose death over swearing allegiance; Kings Justice is the executioner's title, no direct lord-buckler→title edge",BKT8),
]
write_file(BKT8, "lord-buckler", rows)

# ── File 26: ralph-buckler ────────────────────────────────────────────────
rows = [
    e("ralph-buckler","joffrey-baratheon","ALLIES_WITH",
      "Ralph offers a toast to the royal couple during the wedding feast at the Red Keep.",
      "## Narrative Arc / ### A Storm of Swords", BKT8, confidence="tier-2",
      qualifier="toasted at Joffrey's wedding; social alliance marker"),
    e("ralph-buckler","red-keep","LOCATED_AT",
      "Ralph offers a toast to the royal couple during the wedding feast at the [LINK].",
      "## Narrative Arc / ### A Storm of Swords", BKT8),
    r("ralph-buckler","oberyn-martell","HOST_OF not in edge vocabulary — filing vocab-gap separately",BKT8),
    r("ralph-buckler","kings-landing","destination context; LOCATED_AT red-keep is more specific",BKT8),
    r("ralph-buckler","margaery-tyrell","at Joffrey's wedding; no direct ralph→margaery relationship",BKT8),
    r("ralph-buckler","poison","Joffrey was poisoned; ralph was present but no ralph→poison edge",BKT8),
]
write_file(BKT8, "ralph-buckler", rows)

# ── File 27: jarman-buckwell ──────────────────────────────────────────────
BKT9 = "characters-house-buckwell"
rows = [
    e("jarman-buckwell","great-ranging","FIGHTS_IN",
      "Jarman is the leader of the scouts on the [LINK] beyond the Wall.",
      "## Narrative Arc / ### A Clash of Kings", BKT9),
    e("jarman-buckwell","beyond-the-wall","LOCATED_AT",
      "Jarman is the leader of the scouts on the great ranging [LINK].",
      "## Narrative Arc / ### A Clash of Kings", BKT9),
    e("jarman-buckwell","frostfangs","LOCATED_AT",
      "Qhorin Halfhand suggests ... Jarman ... as leaders of small scouting groups sent into the [LINK] to seek out the wildling camp.",
      "## Narrative Arc / ### A Clash of Kings", BKT9),
    e("jarman-buckwell","qhorin-halfhand","ALLIES_WITH",
      "[LINK] suggests himself, Jarman, and Thoren Smallwood as leaders of small scouting groups.",
      "## Narrative Arc / ### A Clash of Kings", BKT9),
    e("jarman-buckwell","thoren-smallwood","ALLIES_WITH",
      "Qhorin Halfhand suggests himself, Jarman, and [LINK] as leaders of small scouting groups.",
      "## Narrative Arc / ### A Clash of Kings", BKT9),
    e("jarman-buckwell","castle-black","LOCATED_AT",
      "Jarman's team is able to return to [LINK], after the main party arrives but before Jon Snow does.",
      "## Narrative Arc / ### A Storm of Swords", BKT9),
    e("jarman-buckwell","giants-stair","LOCATED_AT",
      "Jarman leads the scouting mission to climb the [LINK] in search of the wildlings.",
      "## Narrative Arc / ### A Storm of Swords", BKT9),
    e("jarman-buckwell","jeor-mormont","SERVES",
      "By the time they return, the disastrous fight at the Fist has already happened and Lord Commander [LINK]'s party evacuates for Craster's Keep.",
      "## Narrative Arc / ### A Storm of Swords", BKT9, confidence="tier-2"),
    e("jarman-buckwell","mance-rayder","OPPOSES",
      "Jarman's team remains in the wilderness, tracking [LINK]'s host.",
      "## Narrative Arc / ### A Storm of Swords", BKT9),
    r("jarman-buckwell","aemon-targaryen-son-of-maekar-i","Jarman reports to Aemon; no REPORTS_TO type; informing not a structural edge",BKT9),
    r("jarman-buckwell","crasters-keep","Mormont's party went there; Jarman's team stayed in wilderness",BKT9),
    r("jarman-buckwell","donal-noye","Jarman reported to Noye along with Aemon; same issue as aemon candidate",BKT9),
    r("jarman-buckwell","fight-at-the-fist","Jarman was NOT at the Fight at the Fist; was away scouting",BKT9),
    r("jarman-buckwell","jon-snow","spotted Jon with wildlings; observation not a structural relationship",BKT9),
]
write_file(BKT9, "jarman-buckwell", rows)

# ── File 28: alyn-bullock ─────────────────────────────────────────────────
BKT10 = "characters-house-bullock"
rows = [
    e("alyn-bullock","dragonstone","LOCATED_AT",
      "When King Jaehaerys was on [LINK] during his regency, he spent every morning... Ser Alyn, along with his father Merrell and brother Howard... would spar with the young king.",
      "## Origins", BKT10),
    e("alyn-bullock","howard-bullock","SIBLING_OF",
      "Ser Alyn, along with his father Merrell and [LINK], Ser Elyas Scales... would spar with the young king.",
      "## Origins", BKT10),
    r("alyn-bullock","elyas-scales","fellow sparring partner; too minor for structural relationship",BKT10),
    r("alyn-bullock","kingsguard","co-sparring partners; Alyn has no MEMBER_OF relationship to Kingsguard",BKT10),
    r("alyn-bullock","knight","generic concept",BKT10),
]
write_file(BKT10, "alyn-bullock", rows)

# ── File 29: howard-bullock ───────────────────────────────────────────────
rows = [
    e("howard-bullock","alyn-bullock","SIBLING_OF",
      "his father Merrell, his brother [LINK], Ser Elyas Scales, and knights of the Kingsguard.",
      "## Origins", BKT10),
    e("howard-bullock","dragonstone","LOCATED_AT",
      "When King Jaehaerys I Targaryen was on [LINK] during his regency, he spent every morning... sparring.",
      "## Origins", BKT10),
    e("howard-bullock","driftmark","LOCATED_AT",
      "A fishing boat took them to [LINK], where they took ship for Pentos.",
      "## Origins", BKT10),
    e("howard-bullock","disputed-lands","LOCATED_AT",
      "made their way to the [LINK], where Howard joined the Free Company.",
      "## Origins", BKT10),
    e("howard-bullock","free-company-sellsword-company","MEMBER_OF",
      "made their way to the Disputed Lands, where Howard joined the [LINK].",
      "## Origins", BKT10),
    e("howard-bullock","jaehaerys-i-targaryen","SERVES",
      "When King [LINK] was on Dragonstone during his regency, he spent every morning until midday in the castle yard. Howard... would spar with the young king.",
      "## Origins", BKT10, confidence="tier-2"),
    e("howard-bullock","pentos","LOCATED_AT",
      "A fishing boat took them to Driftmark, where they took ship for [LINK].",
      "## Origins", BKT10),
    r("howard-bullock","alcoholic-beverages","cause of death context; no character→concept edge type",BKT10),
    r("howard-bullock","elyas-scales","fellow sparring partner; too minor",BKT10),
    r("howard-bullock","horse","fell from horse; no character→horse edge type applicable",BKT10),
    r("howard-bullock","jewelry","stole wife's jewelry; no applicable edge to jewelry concept",BKT10),
    r("howard-bullock","kingsguard","co-sparring partners; Howard has no MEMBER_OF relationship",BKT10),
    r("howard-bullock","knight","generic concept",BKT10),
]
write_file(BKT10, "howard-bullock", rows)

# ── File 30: merrell-bullock ──────────────────────────────────────────────
rows = [
    e("merrell-bullock","rhaena-targaryen-daughter-of-aenys-i","SERVES",
      "When [LINK] was given Dragonstone as her seat, Ser Merrell continued in his service to her.",
      "## Origins", BKT10),
    r("merrell-bullock","dragon-egg","three dragon eggs stolen from Dreamfyre; Merrell lost his post but no character→dragon-egg edge",BKT10),
    r("merrell-bullock","dreamfyre","Elissa Farman stole eggs from Dreamfyre; Merrell's relationship to the dragon is indirect",BKT10),
    r("merrell-bullock","elissa-farman","stole the eggs; Merrell dismissed because of it; indirect relationship",BKT10),
    r("merrell-bullock","elyas-scales","fellow sparring partner with Jaehaerys; too minor",BKT10),
    r("merrell-bullock","kingsguard","co-sparring partners; Merrell has no MEMBER_OF relationship",BKT10),
    r("merrell-bullock","knight","generic concept",BKT10),
    r("merrell-bullock","master-at-arms","Elyas Scales held this title, not Merrell",BKT10),
]
write_file(BKT10, "merrell-bullock", rows)

print("\nAll 28 files written successfully.")
