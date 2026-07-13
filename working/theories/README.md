# Theories track — ACTIVE (gate opened by Matt 2026-07-12, S213)

> Supersedes the DEFERRED status in `working/theories-staging/README.md` (that folder
> stays as the design record + the eldritch-apocalypse seed). Matt's kickoff steer:
> **video-transcript-first** — Alt Shift X (ASX) is the ingestion source for wave 1;
> build the video list, narrow to the theory-focused ones, use transcripts + our
> existing theory-node list to shape the schema.

## Why ASX transcripts first

ASX theory videos are already curated syntheses: each states the claim, walks the
book evidence (often quoting exact lines), and weighs counter-evidence. A transcript
gives a theory's *evidence skeleton* — which we then re-ground against OUR corpus
(every cited line grep-verified to chapter:line, same machine as the S213 quote-cite
upgrade) rather than trusting the video. ASX is the source of the *map*, the books
stay the source of *truth*.

## Pipeline (per theory)

1. **Transcript** → `videos/transcripts/<video-id>.en.vtt` (yt_dlp captions; ~10KB each).
2. **Claim + evidence extraction** (agent): claim one-liner, sub-claims, each evidence
   beat the video cites (paraphrase + book location hint).
3. **Re-grounding** (deterministic + agent): each beat matched to our chapter corpus →
   verbatim quote + `chapter:line`; unmatched beats flagged, never invented.
4. **Node + edges** (the proven dip machine: propose → fresh-verify → adjudicate →
   audits → mint): `concept.theory` node (enrich existing stub or mint), evidence
   edges `SUPPORTS` / `CONTRADICTS` (evidence → theory), `CITED_BY` (theory → source).
   Theories are Tier 3–5 ALWAYS — never tier-1/2 (interpretive layer).
5. **Chat surface**: UNCHANGED for now — SHARED_RULES still forbids theory talk in
   answers. The theory layer lands in the graph first; how/whether the chat exposes
   it (a "theories mode"?) is a separate Matt decision.

## Schema (from the eldritch seed template + video sourcing)

```yaml
type: concept.theory
name: "Grand Northern Conspiracy"
slug: grand-northern-conspiracy
claim: "<one-line falsifiable statement of the theory>"
confidence: tier-3|4|5        # 3 = strong textual case, 5 = crackpot
status: open | show-confirmed | jossed   # show events ≠ book canon; status only annotates
origin: "<theorist/community>"           # -> CITED_BY edge
video_sources:
  - {channel: "Alt Shift X", id: "<yt-id>", title: "...", transcript: "working/theories/videos/transcripts/<id>.en.vtt"}
```

Body sections: `## Claim`, `## Evidence For` (each beat with verbatim quote +
chapter:line), `## Evidence Against`, `## Status Notes` (show outcome, GRRM comments).

## Files

- `videos/asx-inventory-raw.json` — all 183 ASX channel videos (2026-07-12 pull).
- `videos/asx-triage-v1.json` — deterministic split: 72 theory-candidates /
  83 show-recaps / 28 non-ASOIAF (title-pattern pass; a few false positives weeded
  by hand in the curated set below).
- `videos/asx-starter-set.json` — the curated wave-1 set (below), Matt-narrowable.
- `videos/transcripts/` — pulled caption files.

## Wave-1 starter set (curated; Matt narrows/vetoes)

Selection: canonical named theories, theory-focused (not episode recaps, not joke
videos, not 2-hour character epics), preferring ones with an existing dark-stub node
to enrich. Existing-node matches noted.

| video | min | node |
|---|---|---|
| R+L=J: who are Jon Snow's parents? | 6 | jon-snow-theories |
| Rhaegar: was Jon's father the true hero…? | 16 | (same cluster) |
| Knight of the Laughing Tree | 14 | knight-of-the-laughing-tree-theories |
| Who is Azor Ahai? | 16 | azor-ahai-theories + the-prince-that-was-promised-theories |
| Euron Greyjoy's apocalypse in the books | 25 | NEW eldritch-apocalypse (staged seed S110) |
| "The north remembers": Grand Northern Conspiracy | 22 | NEW |
| The Grand Maester Conspiracy | 17 | NEW |
| Pink Letter: who will win Winterfell? | 18 | bastard-letter-theories |
| Bolt-On: is Roose Bolton immortal? | 7 | roose-bolton-theories |
| Tyrion Targaryen: is Tyrion the Mad King's son? | 9 | NEW (A+J=T) |
| Jojen Paste: does Bran eat Jojen? | 11 | NEW |
| Hooded Man: who is the Ghost in Winterfell? | 24 | hooded-man-theories |
| Who is Coldhands? | 8 | coldhands-theories |
| Bloodraven: the three-eyed raven's secret plan | 20 | ties the S130 Bloodraven dip |
| Patchface: the strangest character? | 13 | patchface-theories |

Deliberately NOT wave 1: joke theories (Ser Pounce=AA, Tormund's bear, Hodor),
character-study epics (The real Jon Snow 128m, The real Tyrion 75m — background, not
theory), deep-lore Tier B (Summerhall / Blackfyres / Doom of Valyria — arc-enrichment
food), Daario=Euron + HS=HR + Bolt-On-adjacent micro-theories can be wave 2.
**Matt (S214, mid-session): the "The real X" character epics are "all great" — bump
them to the FRONT of the wave-2 queue** (they're evidence-dense; treat as enrichment
substrate feeding character nodes + whichever theories they adjudicate, not as one
theory node each).

## Vocabulary

This is the **Theories track**; steps are lowercase; Tier = confidence 1–5 only.
Paste these into any subagent prompt that names or sequences work.
