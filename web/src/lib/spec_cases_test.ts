// The Python <-> TS drift alarm (query-layer Track, step 1 / session A).
//
// Discovers every golden case in graph/query/spec/cases/*.json and runs the ones
// whose profile is "bounded" or "both" against the real TS lib + the real bundle
// (web/data/, loaded once via _fixtures.ts's `data`). Cases whose profile is
// "full" only are for the (separate, optional) Python runner
// (graph/query/spec/run_cases.py) and are skipped here — not failed.
//
// This file is the FIRST piece of the eventual traversal test suite (D-G in
// working/query-layer/design.md), but it is not that suite: it has no fixtures
// of its own, no synthetic mini-graph — it is a thin, generic case-runner over
// externally-authored JSON, so the same fixtures can also run under pytest once
// the Python engine exists. See graph/query/spec/cases/README.md for the case
// schema this file implements.

import assert from "node:assert/strict";
import { resolve } from "./resolve.ts";
import { familyTree, neighbors, walkChain } from "./graph.ts";
import { searchQuotes } from "./search.ts";
import { listNodes } from "./list.ts";
import { theme } from "./themes.ts";
import { container } from "./container.ts";
import { path } from "./path.ts";
import { participants } from "./participants.ts";
import { data } from "./_fixtures.ts";
import type {
  ChainResult,
  ContainerResult,
  FamilyTreeResult,
  ListResult,
  NeighborsResult,
  ParticipantsResult,
  PathResult,
  ResolveCandidate,
  SearchResult,
  ThemeResult,
} from "./types.ts";

// Path is relative to THIS file (web/src/lib/spec_cases_test.ts), so it resolves
// regardless of the caller's cwd: ../../.. -> web/ -> repo root -> graph/query/spec/cases.
const CASES_DIR = new URL("../../../graph/query/spec/cases/", import.meta.url);

interface Case {
  id: string;
  op:
    | "resolve"
    | "neighbors"
    | "chain"
    | "family"
    | "search"
    | "list"
    | "theme"
    | "container"
    | "path"
    | "participants";
  profile: "bounded" | "full" | "both";
  // deno-lint-ignore no-explicit-any
  input: Record<string, any>;
  // deno-lint-ignore no-explicit-any
  expect: Record<string, any>;
  note?: string;
}

async function loadCases(filename: string): Promise<Case[]> {
  const url = new URL(filename, CASES_DIR);
  const text = await Deno.readTextFile(url);
  return JSON.parse(text) as Case[];
}

function runsUnderBounded(c: Case): boolean {
  return c.profile === "bounded" || c.profile === "both";
}

// ---- per-op runners: each takes a case's `input` + `expect` and asserts ----

function runResolve(c: Case) {
  const hits: ResolveCandidate[] = resolve(c.input.phrase, data);
  const exp = c.expect;

  if (exp.candidates !== undefined) {
    assert.equal(hits.length, exp.candidates.length, `${c.id}: candidate count`);
    for (let i = 0; i < exp.candidates.length; i++) {
      const want = exp.candidates[i];
      assert.equal(hits[i].slug, want.slug, `${c.id}: candidate[${i}].slug`);
      assert.equal(hits[i].category, want.category, `${c.id}: candidate[${i}].category`);
      assert.equal(hits[i].score, want.score, `${c.id}: candidate[${i}].score`);
      assert.equal(hits[i].matchType, want.matchType, `${c.id}: candidate[${i}].matchType`);
    }
  }
  if (exp.top !== undefined) {
    assert.ok(hits.length > 0, `${c.id}: expected at least one hit`);
    if (exp.top.slug !== undefined) assert.equal(hits[0].slug, exp.top.slug, `${c.id}: top.slug`);
    if (exp.top.category !== undefined) {
      assert.equal(hits[0].category, exp.top.category, `${c.id}: top.category`);
    }
    if (exp.top.score !== undefined) assert.equal(hits[0].score, exp.top.score, `${c.id}: top.score`);
    if (exp.top.matchType !== undefined) {
      assert.equal(hits[0].matchType, exp.top.matchType, `${c.id}: top.matchType`);
    }
  }
  if (exp.mustIncludeSlug !== undefined) {
    assert.ok(
      hits.some((h) => h.slug === exp.mustIncludeSlug),
      `${c.id}: expected ${exp.mustIncludeSlug} among candidates`,
    );
  }
  if (exp.candidateSlugs !== undefined) {
    const gotSlugs = new Set(hits.map((h) => h.slug));
    for (const s of exp.candidateSlugs) {
      assert.ok(gotSlugs.has(s), `${c.id}: expected candidate slug ${s}`);
    }
  }
  if (exp.topSlugIsNot !== undefined) {
    if (hits.length > 0) {
      assert.notEqual(hits[0].slug, exp.topSlugIsNot, `${c.id}: top slug must not be ${exp.topSlugIsNot}`);
    }
  }
  if (exp.allScoresBelow !== undefined) {
    for (const h of hits) {
      assert.ok(h.score < exp.allScoresBelow, `${c.id}: score ${h.score} must be < ${exp.allScoresBelow}`);
    }
  }
  if (exp.rankBefore !== undefined) {
    const firstIdx = hits.findIndex((h) => h.slug === exp.rankBefore.first);
    const secondIdx = hits.findIndex((h) => h.slug === exp.rankBefore.second);
    assert.ok(firstIdx !== -1 && secondIdx !== -1, `${c.id}: both rankBefore slugs must be present`);
    assert.ok(firstIdx < secondIdx, `${c.id}: ${exp.rankBefore.first} must rank before ${exp.rankBefore.second}`);
  }
}

function runNeighbors(c: Case) {
  const n: NeighborsResult = neighbors(c.input.slug, data);
  const exp = c.expect;

  if (exp.outgoingCount !== undefined) assert.equal(n.outgoingCount, exp.outgoingCount, `${c.id}: outgoingCount`);
  if (exp.incomingCount !== undefined) assert.equal(n.incomingCount, exp.incomingCount, `${c.id}: incomingCount`);
  if (exp.outgoing !== undefined) assert.deepEqual(n.outgoing, exp.outgoing, `${c.id}: outgoing`);
  if (exp.incoming !== undefined) assert.deepEqual(n.incoming, exp.incoming, `${c.id}: incoming`);

  if (exp.outgoingCountAtLeast !== undefined) {
    assert.ok(n.outgoingCount >= exp.outgoingCountAtLeast, `${c.id}: outgoingCount >= ${exp.outgoingCountAtLeast}`);
  }
  if (exp.incomingCountAtLeast !== undefined) {
    assert.ok(n.incomingCount >= exp.incomingCountAtLeast, `${c.id}: incomingCount >= ${exp.incomingCountAtLeast}`);
  }
  if (exp.hasOutgoingTypes !== undefined) {
    for (const t of exp.hasOutgoingTypes) {
      assert.ok(t in n.outgoing, `${c.id}: expected outgoing edge type ${t}`);
    }
  }
  if (exp.hasIncomingTypes !== undefined) {
    for (const t of exp.hasIncomingTypes) {
      assert.ok(t in n.incoming, `${c.id}: expected incoming edge type ${t}`);
    }
  }
  if (exp.outgoingTypeTargets !== undefined) {
    for (const [edgeType, targets] of Object.entries(exp.outgoingTypeTargets) as [string, string[]][]) {
      const links = n.outgoing[edgeType] ?? [];
      const gotTargets = links.map((l) => l.target);
      for (const t of targets) {
        assert.ok(gotTargets.includes(t), `${c.id}: expected ${edgeType} -> ${t}`);
      }
    }
  }
  if (exp.assertion !== undefined) {
    // The one structural-invariant case: counts equal the sum of the grouped links.
    const sum = (g: Record<string, unknown[]>) => Object.values(g).reduce((a, b) => a + b.length, 0);
    assert.equal(n.outgoingCount, sum(n.outgoing), `${c.id}: outgoingCount == sum(outgoing groups)`);
    assert.equal(n.incomingCount, sum(n.incoming), `${c.id}: incomingCount == sum(incoming groups)`);
  }
}

function runChain(c: Case) {
  const opts: { maxDepth?: number; expandBeats?: boolean } = {};
  if (c.input.maxDepth !== undefined) opts.maxDepth = c.input.maxDepth;
  if (c.input.expandBeats !== undefined) opts.expandBeats = c.input.expandBeats;
  const chain: ChainResult = walkChain(c.input.slug, data, opts);
  const exp = c.expect;

  if (exp.beats !== undefined) {
    assert.deepEqual(chain.beats, exp.beats, `${c.id}: beats`);
  }

  // deno-lint-ignore no-explicit-any
  const linkSubset = (l: any, want: Record<string, unknown>) => {
    for (const k of ["source", "edge_type", "target", "depth"]) {
      if (want[k] !== undefined) assert.equal(l[k], want[k], `${c.id}: link.${k}`);
    }
  };

  if (exp.upstreamOrder !== undefined) {
    assert.equal(chain.upstream.length, exp.upstreamOrder.length, `${c.id}: upstream length`);
    exp.upstreamOrder.forEach((want: Record<string, unknown>, i: number) => linkSubset(chain.upstream[i], want));
  }
  if (exp.downstreamOrder !== undefined) {
    assert.equal(chain.downstream.length, exp.downstreamOrder.length, `${c.id}: downstream length`);
    exp.downstreamOrder.forEach((want: Record<string, unknown>, i: number) => linkSubset(chain.downstream[i], want));
  }
  if (exp.enables !== undefined) {
    assert.equal(chain.enables.length, exp.enables.length, `${c.id}: enables length`);
    exp.enables.forEach((want: Record<string, unknown>, i: number) => linkSubset(chain.enables[i], want));
  }
  if (exp.enablesCount !== undefined) {
    assert.equal(chain.enables.length, exp.enablesCount, `${c.id}: enablesCount`);
  }
  if (exp.upstream !== undefined) assert.deepEqual(chain.upstream, exp.upstream, `${c.id}: upstream`);
  if (exp.downstream !== undefined) assert.deepEqual(chain.downstream, exp.downstream, `${c.id}: downstream`);

  if (exp.upstreamLengthGreaterThanDefaultDepth === true) {
    const defaultChain = walkChain(c.input.slug, data);
    assert.ok(
      chain.upstream.length > defaultChain.upstream.length,
      `${c.id}: deeper maxDepth must recover more upstream links than the default`,
    );
  }
}

// JSON case files can't express `undefined` (only `null`/absent-key), but real
// records (e.g. a FamilyMember with no `type`) carry an explicit `type: undefined`
// key. Strip undefined-valued keys before a deepEqual so a case author writing
// `{slug, generation}` (no `type` key at all) matches a real object that has
// `type: undefined` sitting on it.
// deno-lint-ignore no-explicit-any
function stripUndefined(v: any): any {
  if (Array.isArray(v)) return v.map(stripUndefined);
  if (v !== null && typeof v === "object") {
    const out: Record<string, unknown> = {};
    for (const [k, val] of Object.entries(v)) {
      if (val !== undefined) out[k] = stripUndefined(val);
    }
    return out;
  }
  return v;
}

function runFamily(c: Case) {
  const opts: { generationsUp?: number; generationsDown?: number } = {};
  if (c.input.generationsUp !== undefined) opts.generationsUp = c.input.generationsUp;
  if (c.input.generationsDown !== undefined) opts.generationsDown = c.input.generationsDown;
  const t: FamilyTreeResult = familyTree(c.input.slug, data, opts);
  const exp = c.expect;

  if (exp.root !== undefined) assert.equal(t.root, exp.root, `${c.id}: root`);
  if (exp.rootName !== undefined) assert.equal(t.rootName, exp.rootName, `${c.id}: rootName`);
  if (exp.memberCount !== undefined) assert.equal(t.memberCount, exp.memberCount, `${c.id}: memberCount`);
  if (exp.truncated !== undefined) assert.equal(t.truncated, exp.truncated, `${c.id}: truncated`);
  if (exp.members !== undefined) {
    assert.deepEqual(stripUndefined(t.members), exp.members, `${c.id}: members`);
  }
  if (exp.parentBonds !== undefined) {
    assert.deepEqual(stripUndefined(t.parentBonds), exp.parentBonds, `${c.id}: parentBonds`);
  }
  if (exp.spouseBonds !== undefined) {
    assert.deepEqual(stripUndefined(t.spouseBonds), exp.spouseBonds, `${c.id}: spouseBonds`);
  }

  if (exp.generationCounts !== undefined) {
    const counts = new Map<number, number>();
    for (const m of t.members) counts.set(m.generation, (counts.get(m.generation) ?? 0) + 1);
    for (const [gen, want] of Object.entries(exp.generationCounts)) {
      assert.equal(counts.get(Number(gen)) ?? 0, want, `${c.id}: generation ${gen} member count`);
    }
  }
  if (exp.generationBounds !== undefined) {
    for (const m of t.members) {
      assert.ok(
        m.generation >= exp.generationBounds.min && m.generation <= exp.generationBounds.max,
        `${c.id}: member ${m.slug} generation ${m.generation} within [${exp.generationBounds.min}, ${exp.generationBounds.max}]`,
      );
    }
  }
  if (exp.mustInclude !== undefined) {
    const slugs = new Set(t.members.map((m) => m.slug));
    for (const s of exp.mustInclude) assert.ok(slugs.has(s), `${c.id}: expected member ${s}`);
  }
  if (exp.mustExclude !== undefined) {
    const slugs = new Set(t.members.map((m) => m.slug));
    for (const s of exp.mustExclude) assert.ok(!slugs.has(s), `${c.id}: expected member ${s} to be absent`);
  }
  if (exp.spouseBondIncludes !== undefined) {
    const { a, b } = exp.spouseBondIncludes;
    assert.ok(
      t.spouseBonds.some((bond) => (bond.a === a && bond.b === b) || (bond.a === b && bond.b === a)),
      `${c.id}: expected a spouse bond between ${a} and ${b}`,
    );
  }
}

function runSearch(c: Case) {
  const opts: { type?: string; limit?: number } = {};
  if (c.input.type !== undefined) opts.type = c.input.type;
  if (c.input.limit !== undefined) opts.limit = c.input.limit;
  const results: SearchResult[] = searchQuotes(c.input.query, data, opts);
  const exp = c.expect;

  if (exp.results !== undefined) {
    assert.deepEqual(results, exp.results, `${c.id}: results`);
  }
  if (exp.top !== undefined) {
    assert.ok(results.length > 0, `${c.id}: expected at least one result`);
    if (exp.top.slug !== undefined) assert.equal(results[0].slug, exp.top.slug, `${c.id}: top.slug`);
    if (exp.top.type !== undefined) assert.equal(results[0].type, exp.top.type, `${c.id}: top.type`);
  }
  if (exp.topCiteContains !== undefined) {
    assert.ok(results.length > 0, `${c.id}: expected at least one result`);
    assert.ok(
      (results[0].cite ?? "").includes(exp.topCiteContains),
      `${c.id}: top.cite ${results[0].cite} must contain ${exp.topCiteContains}`,
    );
  }
  if (exp.mustIncludeSlug !== undefined) {
    assert.ok(
      results.some((r) => r.slug === exp.mustIncludeSlug),
      `${c.id}: expected ${exp.mustIncludeSlug} among results`,
    );
  }
  if (exp.topTypeIn !== undefined) {
    assert.ok(results.length > 0, `${c.id}: expected at least one result`);
    assert.ok(
      (exp.topTypeIn as string[]).includes(results[0].type),
      `${c.id}: top.type ${results[0].type} must be one of ${exp.topTypeIn}`,
    );
  }
  if (exp.topScoreAtLeast !== undefined) {
    assert.ok(results.length > 0, `${c.id}: expected at least one result`);
    assert.ok(
      results[0].score >= exp.topScoreAtLeast,
      `${c.id}: top score ${results[0].score} must be >= ${exp.topScoreAtLeast}`,
    );
  }
  if (exp.allTypesEqual !== undefined) {
    for (const r of results) {
      assert.equal(r.type, exp.allTypesEqual, `${c.id}: every result must have type ${exp.allTypesEqual}`);
    }
  }
}

function runList(c: Case) {
  const opts: { type: string; hasQuotes?: boolean; limit?: number; offset?: number } = {
    type: c.input.type,
  };
  if (c.input.hasQuotes !== undefined) opts.hasQuotes = c.input.hasQuotes;
  if (c.input.limit !== undefined) opts.limit = c.input.limit;
  if (c.input.offset !== undefined) opts.offset = c.input.offset;
  const result: ListResult = listNodes(data, opts);
  const exp = c.expect;

  if (exp.category !== undefined) assert.equal(result.category, exp.category, `${c.id}: category`);
  if (exp.total !== undefined) assert.equal(result.total, exp.total, `${c.id}: total`);
  if (exp.items !== undefined) assert.deepEqual(result.items, exp.items, `${c.id}: items`);
}

function runTheme(c: Case) {
  const opts: { category?: string } = {};
  if (c.input.category !== undefined) opts.category = c.input.category;
  const result: ThemeResult = theme(c.input.name, data, opts);
  const exp = c.expect;

  if (exp.memberCount !== undefined) {
    assert.equal(result.memberCount, exp.memberCount, `${c.id}: memberCount`);
  }
  if (exp.members !== undefined) assert.deepEqual(result.members, exp.members, `${c.id}: members`);
  if (exp.hasError !== undefined) {
    assert.equal(!!result.error, exp.hasError, `${c.id}: hasError`);
  }
  if (exp.mustIncludeSlug !== undefined) {
    assert.ok(
      result.members.some((m) => m.slug === exp.mustIncludeSlug),
      `${c.id}: expected ${exp.mustIncludeSlug} among theme members`,
    );
  }
  if (exp.memberCountAtLeast !== undefined) {
    assert.ok(
      result.members.length >= exp.memberCountAtLeast,
      `${c.id}: memberCountAtLeast ${result.members.length} >= ${exp.memberCountAtLeast}`,
    );
  }
  if (exp.themeNameEquals !== undefined) {
    assert.equal(
      result.theme.toLowerCase(),
      exp.themeNameEquals.toLowerCase(),
      `${c.id}: themeNameEquals`,
    );
  }
  if (exp.allCategoriesEqual !== undefined) {
    for (const m of result.members) {
      assert.equal(m.category, exp.allCategoriesEqual, `${c.id}: every member must have category ${exp.allCategoriesEqual}`);
    }
  }
}

function runContainer(c: Case) {
  const result: ContainerResult = container(c.input.name, data);
  const exp = c.expect;
  const memberSlugs = result.nodes.map((n) => n.slug);

  if (exp.count !== undefined) assert.equal(result.count, exp.count, `${c.id}: count`);
  if (exp.nodes !== undefined) assert.deepEqual(result.nodes, exp.nodes, `${c.id}: nodes`);
  if (exp.mustIncludeSlug !== undefined) {
    assert.ok(
      memberSlugs.includes(exp.mustIncludeSlug),
      `${c.id}: expected ${exp.mustIncludeSlug} among container members`,
    );
  }
  if (exp.memberCountAtLeast !== undefined) {
    assert.ok(
      result.count >= exp.memberCountAtLeast,
      `${c.id}: memberCountAtLeast ${result.count} >= ${exp.memberCountAtLeast}`,
    );
  }
}

function runPath(c: Case) {
  const result: PathResult = path(c.input.slugA, c.input.slugB, data);
  const exp = c.expect;

  if (exp.directEdges !== undefined) assert.deepEqual(result.directEdges, exp.directEdges, `${c.id}: directEdges`);
  if (exp.totalBridges !== undefined) assert.equal(result.totalBridges, exp.totalBridges, `${c.id}: totalBridges`);
  if (exp.bridgesShown !== undefined) assert.equal(result.bridgesShown, exp.bridgesShown, `${c.id}: bridgesShown`);
  if (exp.bridges !== undefined) assert.deepEqual(result.bridges, exp.bridges, `${c.id}: bridges`);
  if (exp.directEdgesAtLeast !== undefined) {
    assert.ok(
      result.directEdges.length >= exp.directEdgesAtLeast,
      `${c.id}: directEdgesAtLeast ${result.directEdges.length} >= ${exp.directEdgesAtLeast}`,
    );
  }
  if (exp.totalBridgesAtLeast !== undefined) {
    assert.ok(
      result.totalBridges >= exp.totalBridgesAtLeast,
      `${c.id}: totalBridgesAtLeast ${result.totalBridges} >= ${exp.totalBridgesAtLeast}`,
    );
  }
  if (exp.mustIncludeBridges !== undefined) {
    const bridgeSlugs = new Set(result.bridges.map((b) => b.bridge));
    for (const s of exp.mustIncludeBridges) {
      assert.ok(bridgeSlugs.has(s), `${c.id}: expected bridge ${s}`);
    }
  }
}

function runParticipants(c: Case) {
  const result: ParticipantsResult = participants(c.input.hubSlug, data);
  const exp = c.expect;

  if (exp.hasError !== undefined) assert.equal(!!result.error, exp.hasError, `${c.id}: hasError`);
  if (exp.beatCount !== undefined) assert.equal(result.beatCount, exp.beatCount, `${c.id}: beatCount`);
  if (exp.participantCount !== undefined) {
    assert.equal(result.participantCount, exp.participantCount, `${c.id}: participantCount`);
  }
  if (exp.participants !== undefined) {
    assert.deepEqual(result.participants, exp.participants, `${c.id}: participants`);
  }
  if (exp.beatCountAtLeast !== undefined) {
    assert.ok(result.beatCount >= exp.beatCountAtLeast, `${c.id}: beatCountAtLeast`);
  }
  if (exp.participantCountAtLeast !== undefined) {
    assert.ok(
      result.participantCount >= exp.participantCountAtLeast,
      `${c.id}: participantCountAtLeast ${result.participantCount} >= ${exp.participantCountAtLeast}`,
    );
  }
  if (exp.mustIncludeSource !== undefined) {
    const sources = new Set(result.participants.map((p) => p.sourceSlug));
    for (const s of exp.mustIncludeSource) {
      assert.ok(sources.has(s), `${c.id}: expected participant source ${s}`);
    }
  }
  if (exp.hasRoleType !== undefined) {
    assert.ok(
      result.participants.some((p) => p.roleType === exp.hasRoleType),
      `${c.id}: expected a participant with roleType ${exp.hasRoleType}`,
    );
  }
}

const RUNNERS: Record<Case["op"], (c: Case) => void> = {
  resolve: runResolve,
  neighbors: runNeighbors,
  chain: runChain,
  family: runFamily,
  search: runSearch,
  list: runList,
  theme: runTheme,
  container: runContainer,
  path: runPath,
  participants: runParticipants,
};

// ---- discovery + registration ----

const CASE_FILES = [
  "resolve.json",
  "neighbors.json",
  "chain.json",
  "family.json",
  "search.json",
  "list.json",
  "theme.json",
  "container.json",
  "path.json",
  "participants.json",
];

for (const file of CASE_FILES) {
  const cases = await loadCases(file);
  for (const c of cases) {
    const testName = `spec-case [${file}] ${c.id}`;
    if (!runsUnderBounded(c)) {
      // full-profile-only case: no Python engine to run it against from this
      // runner. Register an ignored test so `deno test` still reports it (visible
      // as "ignored", not silently absent from the count) rather than skip.
      Deno.test({ name: testName, ignore: true, fn: () => {} });
      continue;
    }
    Deno.test(testName, () => {
      RUNNERS[c.op](c);
    });
  }
}
