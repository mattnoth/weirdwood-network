// walkChain() + neighbors() + familyTree() tests against the real bundle.

import assert from "node:assert/strict";
import { familyTree, neighbors, walkChain } from "./graph.ts";
import { data, TYWIN_SLUG } from "./_fixtures.ts";

// The Conqueror roots a large, permanent Targaryen lineage — a rich family tree.
const AEGON_SLUG = "aegon-i-targaryen";

Deno.test("walkChain: the default walk is a depth-bounded spine, not the whole component", () => {
  const chain = walkChain(TYWIN_SLUG, data);

  // The default walk is capped at DEFAULT_MAX_DEPTH (2) hops each direction so
  // the "chain walked" panel reads as a tight spine, not a 50-edge graph dump.
  for (const l of [...chain.upstream, ...chain.downstream]) {
    assert.ok(l.depth <= 2, "default walk must not exceed maxDepth=2");
    assert.ok(l.source && l.edge_type && l.target, "link missing source/edge_type/target");
  }

  // Raising maxDepth recovers the deeper transitive chain (proves the cap is the
  // only thing limiting it, not a broken walk).
  const deep = walkChain(TYWIN_SLUG, data, { maxDepth: 10 });
  assert.ok(
    deep.upstream.length > chain.upstream.length,
    "a deeper walk should reach more upstream links than the bounded default",
  );

  // Links remain unique within the bounded walk.
  const key = (l: { source: string; edge_type: string; target: string }) =>
    `${l.source}|${l.edge_type}|${l.target}`;
  const keys = chain.upstream.map(key);
  assert.equal(new Set(keys).size, keys.length, "upstream links must be unique");
});

Deno.test("walkChain: links are enriched with node display names + types", () => {
  const chain = walkChain(TYWIN_SLUG, data);
  const l = [...chain.upstream, ...chain.downstream].find((x) => x.depth === 1);
  assert.ok(l, "expected at least one adjacent link");
  // The receipts panel renders source_name/target_name so live chains show
  // "Assassination of Tywin Lannister", not the raw slug.
  assert.ok(l!.source_name && l!.target_name, "links must carry display names");
  assert.ok(l!.source_type && l!.target_type, "links must carry node types");
});

Deno.test("walkChain: links carry the receipts fields", () => {
  const chain = walkChain(TYWIN_SLUG, data);
  const adjacent = chain.upstream.find((l) => l.depth === 1);
  assert.ok(adjacent, "expected a depth-1 upstream link");
  // depth-1 upstream of the assassination is the Tysha reveal causing it.
  assert.equal(adjacent!.target, TYWIN_SLUG);
  assert.equal(adjacent!.edge_type, "CAUSES");
  assert.ok("evidence_quote" in adjacent! && "ref" in adjacent! && "tier" in adjacent!);
});

Deno.test("walkChain: downstream effects are reachable too", () => {
  const chain = walkChain(TYWIN_SLUG, data);
  assert.ok(chain.downstream.length > 0, "expected downstream consequences");
  // Every downstream link originates from the queried node (depth 1) or a node
  // reached from it; the nearest must have the pivot as source.
  assert.ok(chain.downstream.some((l) => l.source === TYWIN_SLUG && l.depth === 1));
});

Deno.test("walkChain: preconditions return as a separate `enables` array, never in the spine", () => {
  const chain = walkChain(TYWIN_SLUG, data);

  // No ENABLES ever leaks into the causal spine — the model narrates that clean.
  assert.ok(![...chain.upstream, ...chain.downstream].some((l) => l.edge_type === "ENABLES"));

  // The preconditions come back in one round-trip as `enables`, capped (≤24) so a
  // dense hub can't flood the toggle, deduped, and each is a real ENABLES edge
  // whose target is a node the causal spine touches.
  assert.ok(Array.isArray(chain.enables), "enables must be present (possibly empty)");
  assert.ok(chain.enables.length <= 24, "enables is capped");
  const spine = new Set<string>([chain.slug]);
  for (const l of [...chain.upstream, ...chain.downstream]) { spine.add(l.source); spine.add(l.target); }
  const seen = new Set<string>();
  for (const e of chain.enables) {
    assert.equal(e.edge_type, "ENABLES", "every enables link is an ENABLES edge");
    assert.ok(spine.has(e.target), "an ENABLES precondition must target a spine node");
    const key = `${e.source} ${e.target}`;
    assert.ok(!seen.has(key), "enables links are deduped by source->target");
    seen.add(key);
  }
});

Deno.test("walkChain: invalid slug returns an empty chain, no throw", () => {
  const chain = walkChain("not a slug!!", data);
  assert.deepEqual(chain.upstream, []);
  assert.deepEqual(chain.downstream, []);
  assert.deepEqual(chain.enables, []);
});

Deno.test("neighbors: groups edges by direction and type", () => {
  const n = neighbors(TYWIN_SLUG, data);
  assert.ok(n.outgoingCount > 0 || n.incomingCount > 0, "Tywin node should have edges");
  // Counts equal the sum of each direction's grouped links.
  const sum = (g: Record<string, unknown[]>) => Object.values(g).reduce((a, b) => a + b.length, 0);
  assert.equal(sum(n.outgoing), n.outgoingCount);
  assert.equal(sum(n.incoming), n.incomingCount);
  // Every outgoing link has the pivot as source; every incoming as target.
  for (const links of Object.values(n.outgoing)) {
    for (const l of links) assert.equal(l.source, TYWIN_SLUG);
  }
  for (const links of Object.values(n.incoming)) {
    for (const l of links) assert.equal(l.target, TYWIN_SLUG);
  }
});

Deno.test("neighbors: invalid slug returns empty groups, no throw", () => {
  const n = neighbors("../etc/passwd", data);
  assert.equal(n.outgoingCount, 0);
  assert.equal(n.incomingCount, 0);
  assert.deepEqual(n.outgoing, {});
});

Deno.test("familyTree: roots at the queried node and finds its known children", () => {
  const t = familyTree(AEGON_SLUG, data);
  assert.equal(t.root, AEGON_SLUG);
  assert.equal(t.rootName, "Aegon I Targaryen");

  // The root is generation 0.
  const root = t.members.find((m) => m.slug === AEGON_SLUG);
  assert.ok(root && root.generation === 0, "root member must be generation 0");

  // Aegon I's sons (Aenys I + Maegor I) are children one generation DOWN, wired
  // by a PARENT_OF bond rooted at Aegon (source = parent, target = child).
  for (const child of ["aenys-i-targaryen", "maegor-i-targaryen"]) {
    const m = t.members.find((x) => x.slug === child);
    assert.ok(m && m.generation === 1, `${child} should be a gen +1 descendant`);
    assert.ok(
      t.parentBonds.some((b) => b.parent === AEGON_SLUG && b.child === child),
      `expected PARENT_OF bond ${AEGON_SLUG} -> ${child}`,
    );
  }
});

Deno.test("familyTree: attaches the root's spouse at the same generation", () => {
  // Ned Stark's line is clean (no era-collided slugs), so the spouse lands at the
  // partner's generation. Catelyn is Ned's wife → a spouse bond at generation 0.
  const t = familyTree("eddard-stark", data, { generationsUp: 1, generationsDown: 1 });
  const catelyn = t.members.find((m) => m.slug === "catelyn-stark");
  assert.ok(catelyn, "spouse Catelyn should be a member");
  assert.equal(catelyn!.generation, 0, "a spouse sits at the partner's generation");
  assert.ok(
    t.spouseBonds.some(
      (b) =>
        (b.a === "eddard-stark" && b.b === "catelyn-stark") ||
        (b.b === "eddard-stark" && b.a === "catelyn-stark"),
    ),
    "expected a SPOUSE_OF bond between Eddard and Catelyn",
  );
});

Deno.test("familyTree: bonds only ever connect members, and the size cap holds", () => {
  const t = familyTree(AEGON_SLUG, data);
  const memberSlugs = new Set(t.members.map((m) => m.slug));

  // Every bond's endpoints are members (no dangling references into the panel).
  for (const b of t.parentBonds) {
    assert.ok(memberSlugs.has(b.parent) && memberSlugs.has(b.child), "parent bond off-tree");
  }
  for (const b of t.spouseBonds) {
    assert.ok(memberSlugs.has(b.a) && memberSlugs.has(b.b), "spouse bond off-tree");
  }

  // spouseBonds are deduped by unordered pair.
  const seen = new Set<string>();
  for (const b of t.spouseBonds) {
    const key = b.a < b.b ? `${b.a}|${b.b}` : `${b.b}|${b.a}`;
    assert.ok(!seen.has(key), "spouse bonds must be deduped");
    seen.add(key);
  }

  // memberCount is the honest size of the returned set, capped at MAX_FAMILY_MEMBERS.
  assert.equal(t.memberCount, t.members.length);
  assert.ok(t.memberCount <= 96, "member set is capped");

  // Aegon I's dynasty — the near-root breadth PLUS the threaded deep main-line
  // spine down to the book era — overflows the cap, so it must REPORT truncation
  // rather than silently dropping kin.
  assert.equal(t.truncated, true, "a dynasty larger than the cap reports truncated");
});

Deno.test("familyTree: the deep main-line spine reaches the book era from a distant ancestor", () => {
  // Aegon I → Daenerys is 12 PARENT_OF hops — far past the breadth horizon. The
  // deep spine must thread the main lines down to the book generation.
  const t = familyTree(AEGON_SLUG, data);
  const slugs = new Set(t.members.map((m) => m.slug));
  for (const book of ["daenerys-targaryen", "rhaegar-targaryen", "aerys-ii-targaryen", "aegon-v-targaryen"]) {
    assert.ok(slugs.has(book), `deep spine reaches ${book}`);
  }
  // The Blackfyre cadet split (the great bastards) sits on the main line.
  assert.ok(slugs.has("daemon-i-blackfyre"), "deep spine reaches the Blackfyre split");

  // A deep generation stays NARROW — the main line, not the full brood — so a
  // 12-generation dynasty doesn't spiral out of control.
  const gen9 = t.members.filter((m) => m.generation === 9).length;
  assert.ok(gen9 <= 8, `a deep generation is a narrow main line, got ${gen9}`);

  // A tight explicit window opts OUT of the deep spine (bounded local view).
  const local = familyTree(AEGON_SLUG, data, { generationsUp: 1, generationsDown: 1 });
  assert.ok(!new Set(local.members.map((m) => m.slug)).has("daenerys-targaryen"),
    "an explicit shallow window does not thread the deep spine");
});

Deno.test("familyTree: generation bounds are respected (up ancestors / down descendants)", () => {
  const t = familyTree(AEGON_SLUG, data, { generationsUp: 1, generationsDown: 1 });
  for (const m of t.members) {
    assert.ok(m.generation >= -1 && m.generation <= 1, "members must stay within the generation bound");
  }
  // At least one parent (gen -1) and one child (gen +1) appear at bound 1.
  assert.ok(t.members.some((m) => m.generation === -1), "expected an ancestor at gen -1");
  assert.ok(t.members.some((m) => m.generation === 1), "expected a descendant at gen +1");
});

Deno.test("familyTree: members carry a prominence proxy that ranks marquee kin above filler", () => {
  const t = familyTree(AEGON_SLUG, data);
  for (const m of t.members) {
    assert.ok(typeof m.prominence === "number" && m.prominence >= 0, "every member has a prominence");
    assert.ok(typeof m.degree === "number" && typeof m.quoteCount === "number");
    assert.equal(m.prominence, m.degree + 4 * m.quoteCount, "prominence = degree + 4·quoteCount");
  }
  // A book-present character (Daenerys) must outrank a bare-surname stub.
  const dany = t.members.find((m) => m.slug === "daenerys-targaryen");
  const stub = t.members.find((m) => m.slug === "targaryen" || m.slug === "velaryon");
  if (dany && stub) {
    assert.ok(dany.prominence > stub.prominence, "a book character outranks a surname stub");
  }
});

Deno.test("familyTree: invalid slug returns an empty tree, no throw", () => {
  const t = familyTree("../etc/passwd", data);
  assert.deepEqual(t.members, []);
  assert.deepEqual(t.parentBonds, []);
  assert.deepEqual(t.spouseBonds, []);
  assert.equal(t.memberCount, 0);
  assert.equal(t.truncated, false);
});
