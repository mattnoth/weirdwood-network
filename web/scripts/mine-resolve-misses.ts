// web/scripts/mine-resolve-misses.ts — resolver telemetry miner (query-layer Track,
// step 4d, S190-line). LOCAL only, NOT shipped. READ-ONLY on the Blobs store.
//
// Mines the live chat-UI's per-turn usage logs (S186, Netlify Blobs `weirwood-chat`,
// keys `log/YYYY-MM-DD/<uuid>` — see DEPLOY.md + read-logs.ts) for every `resolve`
// tool call a real visitor's turn made, and aggregates a ranked alias-backfill queue.
//
// CLOSED (S190, step 5c): agent.ts's runAgent() now attaches a small `outcome`
// slice (`{matchType, topSlug, score}` for resolve; `{matchType, topSlug,
// resultCount}` for search_quotes — see `outcomeFor()` in agent.ts) to each
// resolve/search_quotes toolTrace entry, so records logged going forward carry
// the true outcome directly. This script PREFERS that logged outcome
// (`fromLoggedOutcome()`) when present.
//
// Historical-gap finding (still relevant for records logged BEFORE the fix):
// older persisted TurnLog.toolTrace entries are `{tool, input}` ONLY (no
// `outcome` field), so the resolve() OUTCOME (hit / fuzzy / miss, score,
// candidates) isn't recoverable from the record itself. For those, this script
// falls back to the DETERMINISTIC reconstruction it always used: load the SAME
// production bundle (web/data/, built by build-chat-export.py) and re-run the
// SAME resolve() the app used, phrase-for-phrase, against it. That recovers
// the outcome for every phrase AS OF the bundle currently on disk (not
// necessarily bit-identical to whatever bundle was live the moment that turn
// ran, if the graph has since changed — see report caveat, which now applies
// only to the fallback path). No LLM, no API spend, no network beyond the
// Blobs read.
//
//   NETLIFY_SITE_ID=… NETLIFY_AUTH_TOKEN=… \
//     ~/.deno/bin/deno run -A --node-modules-dir=auto web/scripts/mine-resolve-misses.ts [--since YYYY-MM-DD]
//
// Writes working/query-layer/resolve-misses.md. Touches nothing else — no Blobs
// writes/deletes, no graph/index mutation.
import { getStore } from "npm:@netlify/blobs@8";
import { loadGraphData } from "../src/lib/data.ts";
import { resolve } from "../src/lib/resolve.ts";
import { normalize } from "../src/lib/normalize.ts";
import type { GraphData, ResolveCandidate } from "../src/lib/types.ts";

const siteID = Deno.env.get("NETLIFY_SITE_ID");
const token = Deno.env.get("NETLIFY_AUTH_TOKEN");

const sinceIdx = Deno.args.indexOf("--since");
const since = sinceIdx >= 0 ? Deno.args[sinceIdx + 1] : null;
if (sinceIdx >= 0 && !since) {
  console.error("--since requires a YYYY-MM-DD value");
  Deno.exit(1);
}

const OUT_PATH = new URL("../../working/query-layer/resolve-misses.md", import.meta.url);

// ---- Types for the persisted log record (mirrors chat.ts TurnLog) ----

/** The small logged outcome slice agent.ts's `outcomeFor()` attaches to a
 *  resolve()/search_quotes() toolTrace entry (query-layer step 5c, S190 — the
 *  fix for this exact gap). Present on records logged after that change;
 *  absent on older records, which fall back to the re-resolve reconstruction
 *  below. */
interface LoggedOutcome {
  matchType: string;
  topSlug: string | null;
  score?: number;
  resultCount?: number;
}

interface ToolTraceEntry {
  tool: string;
  input: Record<string, unknown>;
  outcome?: LoggedOutcome;
}

interface TurnLog {
  question: string;
  toolTrace: ToolTraceEntry[] | null;
  toolCalls: number;
  stopState: string;
  model: string;
  persona: string;
  timestamp: string;
}

interface ResolveCallSite {
  phrase: string;
  question: string;
  timestamp: string;
  key: string;
  /** Present when this call site's toolTrace entry already carries the
   *  logged outcome (S190 fix) — preferred over re-resolving. */
  loggedOutcome?: LoggedOutcome;
}

interface Outcome {
  kind: "miss" | "exact" | "fuzzy";
  topSlug: string | null;
  topScore: number | null;
  candidateCount: number;
}

interface Aggregate {
  normPhrase: string;
  examplePhrase: string; // first-seen original casing
  outcome: Outcome;
  count: number;
  exampleQuestions: string[]; // up to 3
  keys: string[];
}

// ---- 1. Fetch logs (read-only) ----

async function fetchLogs(): Promise<{ logs: TurnLog[]; keys: string[]; authOk: boolean; error?: string }> {
  if (!siteID || !token) {
    return { logs: [], keys: [], authOk: false, error: "NETLIFY_SITE_ID / NETLIFY_AUTH_TOKEN not set" };
  }
  try {
    const store = getStore({ name: "weirwood-chat", siteID, token });
    const { blobs } = await store.list({ prefix: "log/" });
    blobs.sort((a, b) => a.key.localeCompare(b.key));
    const logs: TurnLog[] = [];
    const keys: string[] = [];
    for (const { key } of blobs) {
      const date = key.split("/")[1] ?? "";
      if (since && date < since) continue;
      const raw = await store.get(key);
      if (!raw) continue;
      try {
        const rec = JSON.parse(raw) as TurnLog;
        logs.push(rec);
        keys.push(key);
      } catch {
        // malformed record — skip, don't crash the whole mine
      }
    }
    return { logs, keys, authOk: true };
  } catch (err) {
    return { logs: [], keys: [], authOk: false, error: String(err) };
  }
}

// ---- 2. Extract every resolve() call site across all turns ----

function extractResolveCalls(logs: TurnLog[], keys: string[]): ResolveCallSite[] {
  const out: ResolveCallSite[] = [];
  logs.forEach((rec, i) => {
    if (!Array.isArray(rec.toolTrace)) return;
    for (const entry of rec.toolTrace) {
      if (entry.tool !== "resolve") continue;
      const phrase = typeof entry.input?.phrase === "string" ? entry.input.phrase : "";
      if (!phrase) continue;
      out.push({
        phrase,
        question: rec.question ?? "",
        timestamp: rec.timestamp ?? "",
        key: keys[i] ?? "",
        loggedOutcome: entry.outcome,
      });
    }
  });
  return out;
}

// ---- 3. Recover the outcome: PREFER the logged outcome (S190 fix); fall back
// to re-running production resolve() against the current bundle for older
// records that predate the fix (see the module header + report §Recommendation) ----

function classify(candidates: ResolveCandidate[]): Outcome {
  if (candidates.length === 0) {
    return { kind: "miss", topSlug: null, topScore: null, candidateCount: 0 };
  }
  const top = candidates[0];
  return {
    kind: top.matchType === "exact" ? "exact" : "fuzzy",
    topSlug: top.slug,
    topScore: top.score,
    candidateCount: candidates.length,
  };
}

/** Convert a directly-logged outcome into the report's `Outcome` shape. The
 *  logged record has no candidateCount for a miss/exact-vs-fuzzy tier beyond
 *  what `matchType` already states, and never carries the full candidate
 *  list (records stay small by design) — candidateCount is left at 1 for a
 *  hit (we know there was at least a top candidate) or 0 for a miss, since
 *  the exact count isn't persisted and re-resolving would defeat the point
 *  of preferring the logged record. */
function fromLoggedOutcome(logged: LoggedOutcome): Outcome {
  if (logged.matchType === "miss" || logged.topSlug === null) {
    return { kind: "miss", topSlug: null, topScore: null, candidateCount: 0 };
  }
  return {
    kind: logged.matchType === "exact" ? "exact" : "fuzzy",
    topSlug: logged.topSlug,
    topScore: logged.score ?? null,
    candidateCount: 1,
  };
}

// ---- 4. Aggregate by normalized phrase ----

function aggregate(calls: ResolveCallSite[], data: GraphData): Aggregate[] {
  const byNorm = new Map<string, Aggregate>();
  for (const call of calls) {
    const norm = normalize(call.phrase);
    const outcome = call.loggedOutcome
      ? fromLoggedOutcome(call.loggedOutcome)
      : classify(resolve(call.phrase, data));
    let agg = byNorm.get(norm);
    if (!agg) {
      agg = {
        normPhrase: norm,
        examplePhrase: call.phrase,
        outcome,
        count: 0,
        exampleQuestions: [],
        keys: [],
      };
      byNorm.set(norm, agg);
    }
    agg.count++;
    agg.keys.push(call.key);
    if (call.question && agg.exampleQuestions.length < 3 && !agg.exampleQuestions.includes(call.question)) {
      agg.exampleQuestions.push(call.question);
    }
  }
  return [...byNorm.values()];
}

// ---- 5. Rank: misses first, then fuzzy-with-low/questionable top score, then exact ----

function rankKey(a: Aggregate): [number, number, number] {
  // Lower tuple sorts first. Priority: miss (0) < fuzzy (1) < exact (2).
  const kindRank = a.outcome.kind === "miss" ? 0 : a.outcome.kind === "fuzzy" ? 1 : 2;
  // Within fuzzy, a lower score is a worse (more suspect) match — surface first.
  const scoreRank = a.outcome.kind === "fuzzy" ? (a.outcome.topScore ?? 0) : 0;
  // Within a tier, higher frequency matters more — surface first (negate for ascending sort).
  return [kindRank, scoreRank, -a.count];
}

function compareAggregates(a: Aggregate, b: Aggregate): number {
  const ka = rankKey(a);
  const kb = rankKey(b);
  for (let i = 0; i < ka.length; i++) {
    if (ka[i] !== kb[i]) return ka[i] - kb[i];
  }
  return 0;
}

// ---- 6. Render the report ----

function renderRow(a: Aggregate): string {
  const outcomeLabel = a.outcome.kind === "miss"
    ? "MISS"
    : a.outcome.kind === "fuzzy"
    ? `fuzzy (${a.outcome.topScore})`
    : "exact";
  const top = a.outcome.topSlug ? `\`${a.outcome.topSlug}\`` : "—";
  const examples = a.exampleQuestions.length
    ? a.exampleQuestions.map((q) => `"${q.slice(0, 80)}${q.length > 80 ? "…" : ""}"`).join("; ")
    : "—";
  return `| ${a.examplePhrase} | ${outcomeLabel} | ${top} | ${a.outcome.candidateCount} | ${a.count} | ${examples} |`;
}

function renderReport(opts: {
  authOk: boolean;
  authError?: string;
  since: string | null;
  days: string[];
  turnsScanned: number;
  resolveCallsFound: number;
  loggedOutcomeCount: number;
  aggregates: Aggregate[];
}): string {
  const { authOk, authError, since, days, turnsScanned, resolveCallsFound, loggedOutcomeCount, aggregates } = opts;
  const rangeNote = days.length
    ? `${days[0]} .. ${days[days.length - 1]} (${days.length} day${days.length === 1 ? "" : "s"})`
    : "none";

  const lines: string[] = [];
  lines.push("# Resolve-Miss Report — mined from live chat-UI telemetry");
  lines.push("");
  lines.push(`Generated: ${new Date().toISOString()}`);
  lines.push(`Date range covered: ${rangeNote}${since ? ` (--since ${since})` : ""}`);
  lines.push(`Turns scanned: ${turnsScanned}`);
  lines.push(`\`resolve\` call sites found: ${resolveCallsFound}`);
  lines.push(`Distinct normalized phrases: ${aggregates.length}`);
  lines.push("");

  if (!authOk) {
    lines.push("## Auth / data-access outcome: FAILED");
    lines.push("");
    lines.push(
      `Could not reach the Netlify Blobs store \`weirwood-chat\`. Error: \`${authError}\`. ` +
        "No log data was reachable, so nothing below is mined. Run this script with " +
        "`NETLIFY_SITE_ID` and `NETLIFY_AUTH_TOKEN` set (see web/scripts/read-logs.ts header " +
        "for how to obtain a personal access token), or via the Deno stack from a shell where " +
        "the Netlify CLI is already linked/authenticated for this repo.",
    );
    lines.push("");
    return lines.join("\n");
  }

  lines.push("## Auth / data-access outcome: OK");
  lines.push("");
  lines.push(
    "Blobs store reached read-only via the `@netlify/blobs` SDK (same stack as `read-logs.ts`). " +
      "No writes or deletes were issued against the store.",
  );
  lines.push("");

  lines.push("## Logging-gap finding — CLOSED (S190, step 5c); read before trusting old rows");
  lines.push("");
  lines.push(
    "`agent.ts`'s `runAgent()` now attaches a small `outcome` slice " +
      "(`{matchType, topSlug, score}` for resolve; `{matchType, topSlug, resultCount}` for " +
      "search_quotes — `outcomeFor()`) to each resolve/search_quotes `toolTrace` entry, so " +
      `turns logged going forward carry the true outcome directly. Of the ${resolveCallsFound} ` +
      `\`resolve\` call sites found this run, **${loggedOutcomeCount} carried a logged outcome** ` +
      `(preferred, direct read) and ${resolveCallsFound - loggedOutcomeCount} predate the fix ` +
      "(reconstructed by the fallback below). For those older records: the persisted " +
      "`TurnLog.toolTrace` was `{tool, input}` only — never the tool's result — so this script " +
      "recovers the outcome **deterministically** by re-running the production `resolve()` " +
      "(web/src/lib/resolve.ts) against the CURRENT `web/data/` bundle for every logged phrase " +
      "lacking a logged outcome. Two caveats apply ONLY to that fallback path: (1) if the " +
      "graph/alias-map has changed since a given turn ran, the reconstructed outcome is AS OF " +
      "THE CURRENT BUNDLE, not necessarily what the live app returned that day; (2) a `resolve` " +
      "call followed immediately by a `read_node`/`walk_chain` on a DIFFERENT slug than the top " +
      "candidate (the model picked its own candidate, or moved on to a different phrase) isn't " +
      "flagged — this report only re-derives resolve()'s own answer, not what the model did " +
      "with it.",
  );
  lines.push("");

  lines.push("## Ranked queue (misses first, then fuzzy low-to-high score, then exact)");
  lines.push("");
  lines.push("| Phrase | Outcome | Top candidate | # candidates | Frequency | Example question(s) |");
  lines.push("|---|---|---|---|---|---|");
  for (const a of aggregates) {
    lines.push(renderRow(a));
  }
  lines.push("");

  lines.push("## Recommendation — DONE");
  lines.push("");
  lines.push(
    "Previously: add matchType/topSlug/score to each `toolTrace` entry in `TurnLog`. This " +
      "landed in agent.ts (`outcomeFor()`, wired into `runAgent()`'s toolTrace push) — the " +
      "recommendation is satisfied for all turns logged from that change forward. No further " +
      "action; this section stays as the historical record of the fix.",
  );
  lines.push("");

  return lines.join("\n");
}

// ---- main ----

async function main() {
  const { logs, keys, authOk, error } = await fetchLogs();

  if (!authOk) {
    const report = renderReport({
      authOk: false,
      authError: error,
      since,
      days: [],
      turnsScanned: 0,
      resolveCallsFound: 0,
      loggedOutcomeCount: 0,
      aggregates: [],
    });
    await Deno.writeTextFile(OUT_PATH, report);
    console.error(`AUTH/DATA-ACCESS FAILED: ${error}`);
    console.error(`Report written (auth-failure notice only): ${OUT_PATH.pathname}`);
    Deno.exit(1);
  }

  const days = [...new Set(logs.map((l) => (l.timestamp ?? "").slice(0, 10)))].filter(Boolean).sort();
  const calls = extractResolveCalls(logs, keys);
  const loggedOutcomeCount = calls.filter((c) => c.loggedOutcome !== undefined).length;

  const data = await loadGraphData();
  const aggregates = aggregate(calls, data).sort(compareAggregates);

  const report = renderReport({
    authOk: true,
    since,
    days,
    turnsScanned: logs.length,
    resolveCallsFound: calls.length,
    loggedOutcomeCount,
    aggregates,
  });
  await Deno.writeTextFile(OUT_PATH, report);

  console.log(`Turns scanned: ${logs.length}  days: ${days.join(", ")}`);
  console.log(`resolve() call sites: ${calls.length}  distinct phrases: ${aggregates.length}`);
  console.log(`Report written: ${OUT_PATH.pathname}`);
}

await main();
