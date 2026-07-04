// participants(hub) — union of participant role edges across a hub event's
// SUB_BEAT_OF children (query-layer Track, step 6b).
//
// Ports `graph/query/weirwood_query/traverse.py::event_participants()`
// (absorbed from scripts/graph-query.py::cmd_event_participants). The
// reification pattern's read-side: an n-ary event hub's actual participants
// live one hop down, on its reified sub-beats, not on the hub itself — this
// unions them and presents them as if directly attached to the hub.
//
// Per the design doc, this stays dossier-side (no chat tool) — the evals
// showed no failing connection row for it; `path`/`chain` cover the archetype
// queries a public chat turn needs.
//
// No LLM in the loop, ever — pure data.

import type { Edge, GraphData, ParticipantRecord, ParticipantsResult } from "./types.ts";
import { isValidSlug } from "./validate.ts";

const PARTICIPANT_ROLE_TYPES: ReadonlySet<string> = new Set([
  "AGENT_IN",
  "COMMANDS_IN",
  "VICTIM_IN",
  "WIELDED_IN",
  "ATTENDS",
  "LOCATED_AT",
]);

function toParticipantRecord(e: Edge, beatSlug: string): ParticipantRecord {
  return {
    roleType: e.type,
    sourceSlug: e.source,
    beatSlug,
    evidenceQuote: e.quote ?? null,
    tier: e.tier ?? null,
  };
}

/**
 * Union the participant role edges (AGENT_IN/COMMANDS_IN/VICTIM_IN/
 * WIELDED_IN/ATTENDS/LOCATED_AT) across every SUB_BEAT_OF child of
 * `hubSlug`. An invalid or unknown hub slug returns `{error: ...}` with no
 * `beats`/`participants` (mirrors `familyTree`'s "unknown-but-well-formed
 * slug" distinctness — here any hub absent from the bundle's node map is
 * treated as not-found, since there's no edge-name-alone signal the way the
 * full-profile CLI's filesystem probe has). A hub with no SUB_BEAT_OF
 * children returns `beatCount: 0` + an explanatory `message`, not an error.
 */
export function participants(hubSlug: string, data: GraphData): ParticipantsResult {
  if (!isValidSlug(hubSlug)) {
    return {
      hubSlug: String(hubSlug),
      beatCount: 0,
      participantCount: 0,
      participants: [],
      error: `hub not found: '${String(hubSlug)}'`,
    };
  }
  if (!data.nodes[hubSlug]) {
    return {
      hubSlug,
      beatCount: 0,
      participantCount: 0,
      participants: [],
      error: `hub not found: '${hubSlug}'`,
    };
  }

  const beatSlugs: string[] = [];
  for (const e of data.edges) {
    if (e.type === "SUB_BEAT_OF" && e.target === hubSlug) beatSlugs.push(e.source);
  }

  if (beatSlugs.length === 0) {
    return {
      hubSlug,
      beatCount: 0,
      beats: [],
      participantCount: 0,
      participants: [],
      message: "no beats found; this hub has no reified children (no SUB_BEAT_OF edges incoming)",
    };
  }

  const beatSlugSet = new Set(beatSlugs);
  const records: ParticipantRecord[] = [];
  for (const e of data.edges) {
    if (PARTICIPANT_ROLE_TYPES.has(e.type) && beatSlugSet.has(e.target)) {
      records.push(toParticipantRecord(e, e.target));
    }
  }

  return {
    hubSlug,
    beatCount: beatSlugs.length,
    beats: beatSlugs,
    participantCount: records.length,
    participants: records,
  };
}
