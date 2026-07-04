// The Weirwood Network — front-end (S174).
//
// One set of renderers drives BOTH the featured landing exchange and every live
// answer — the only difference is the data source: a pre-baked transcript vs the
// live SSE stream from /api/chat. So the static showpiece IS the design fixture
// for the dynamic chat; they render identically by construction.
//
// SSE contract (web/netlify/edge-functions/README.md): events `token` (prose
// delta), `receipt` ({tool,input,result} — the panel renders from `result`, never
// from the prose), `cite-check`, `status` (failure/empty states), `error`, `done`.
//
// "The chain walked" panel is one deduped vertical spine (S177; the full-width
// Band was retired): each node appears once, joined by its typed edge, with the
// ENABLES precondition web behind a "show preconditions" toggle. Every node opens
// a dossier (live /api/node lookup); hovering a node lights the edges it touches.

const $ = (sel, root = document) => root.querySelector(sel);

/** Tiny DOM builder. children: string (text) | Node | array. */
function el(tag, props = {}, children = []) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(props)) {
    if (k === "class") node.className = v;
    else if (k === "html") node.innerHTML = v;
    else if (k === "dataset") Object.assign(node.dataset, v);
    else if (k === "onclick") node.addEventListener("click", v);
    else if (k in node) node[k] = v;
    else node.setAttribute(k, v);
  }
  // Flatten nested arrays so a child that is itself a list (e.g. a mapped row set)
  // renders its members, never String([div,div]) → "[object HTMLDivElement]".
  for (const c of [].concat(children).flat(Infinity)) {
    if (c == null || c === false) continue;
    node.append(c.nodeType ? c : document.createTextNode(String(c)));
  }
  return node;
}

// ---- Edge-type styling -----------------------------------------------------

const ET_CLASS = {
  CAUSES: "et-causes",
  TRIGGERS: "et-triggers",
  MOTIVATES: "et-motivates",
  ENABLES: "et-enables",
};
const etClass = (t) => ET_CLASS[String(t || "").toUpperCase()] || "et-default";

/** Prettify a kebab slug for display when no name is known (live walk_chain). */
function pretty(slug) {
  const s = String(slug || "").replace(/-/g, " ").trim();
  return s ? s[0].toUpperCase() + s.slice(1) : "—";
}

/** A cite token or chapter file path → a short human chapter label:
 *  "sources/chapters/asos/asos-arya-11.md:51" → "ASOS Arya 11". The chapter file
 *  name is `{book}-{pov}-{number}.md`; drop the path, the `.md`, and the line
 *  number. Non-chapter refs (wiki cite_refs, anything unmatched) come back merely
 *  stripped of their path prefix + backticks. */
function prettyCite(ref) {
  const s = String(ref || "").replace(/`/g, "").trim();
  if (!s) return "";
  const file = s.split("/").pop();
  const m = file.match(/^([a-z0-9]+)-(.+)-(\d+)\.md(?::\d+)?$/i);
  if (!m) return s.replace(/^sources\/chapters\//, "");
  const pov = m[2].split("-").map((w) => (w ? w[0].toUpperCase() + w.slice(1) : w)).join(" ");
  return `${m[1].toUpperCase()} ${pov} ${Number(m[3])}`;
}

/** Strip wiki-markup artifacts the build left in some curated quotes
 *  (`[label](wiki:Page)` → `label`, bare `(wiki:…)` → removed), and collapse any
 *  baked-in source — a "BOOK Pov Roman (sources/…md:NN)" tail, or a bare chapter
 *  path — down to the short chapter label ("ASOS Arya 11"). */
function cleanQuote(text) {
  return String(text || "")
    .replace(/\[([^\]]+)\]\(wiki:[^)]*\)/g, "$1")
    .replace(/\(wiki:[^)]*\)/g, "")
    // "ASOS Arya XI (`sources/…asos-arya-11.md:51`)" → "ASOS Arya 11" (optional
    // human label + parenthesised path collapse together to the short label).
    .replace(
      /(?:[A-Z][\w']*(?:\s+[A-Za-z][\w']*)*\s+[IVXLCDM]+\s*)?\(`?\s*(sources\/chapters\/\S+?\.md:\d+)\s*`?\)/g,
      (_m, path) => prettyCite(path),
    )
    // any bare leftover chapter path → the same short label
    .replace(/`?\b(sources\/chapters\/[a-z0-9/_-]+\.md:\d+)`?/gi, (_m, path) => prettyCite(path))
    // cut internal build provenance some curated attributions carry as a tail
    // ("… — book-cite overlay (harvest row 1001); <gloss>") — never user-facing.
    .replace(/\s*[—–-]\s*(?:book-cite overlay|harvest row)\b[\s\S]*$/i, "")
    .replace(/`/g, "") // strip any remaining markdown backticks
    .replace(/\s+/g, " ")
    .trim();
}

/** True for the auto-generated placeholder identity ("<name> is a <type> from the
 *  AWOIAF wiki.") that 81% of nodes carry — worthless copy, never shown. */
function isWikiBoilerplate(identity) {
  return /\bfrom the AWOIAF wiki\.?\s*$/i.test(String(identity || "").trim());
}

/** A node's type, prettified for the card subtitle ("event.wedding" → "event · wedding"). */
function prettyType(t) {
  const s = String(t || "").trim();
  return s ? s.replace(/[._]/g, " · ") : "";
}

// Normalize a typed-edge link from EITHER the live walk_chain/neighbors shape
// ({source, target, ref}) OR the build-export chain shape ({source_name,
// target_name, evidence_ref}) into one render contract. Slug stays in
// source/target on both; the display name is *_name (when present) or prettified.
function normLink(l) {
  return {
    sourceSlug: l.source || "",
    targetSlug: l.target || "",
    source: l.source_name || pretty(l.source),
    target: l.target_name || pretty(l.target),
    sourceType: l.source_type || "",
    targetType: l.target_type || "",
    edgeType: l.edge_type || l.type || "",
    quote: l.evidence_quote ?? l.quote ?? null,
    ref: l.evidence_ref ?? l.ref ?? null,
    tier: l.tier ?? null,
  };
}

/** Collapse a list of typed links into a deduped node/edge sequence: a shared
 *  node (target of one link == source of the next) is emitted ONCE. */
function buildSequence(rawLinks, querySlug) {
  const items = [];
  const seen = new Set();
  let lastSlug = null;
  const nodeItem = (slug, name, nodeType) => ({
    type: "node",
    slug,
    name,
    nodeType,
    queried: !!querySlug && slug === querySlug,
    repeat: seen.has(slug), // already shown once → render as a slim back-reference
  });
  for (const raw of rawLinks) {
    const l = normLink(raw);
    if (l.sourceSlug !== lastSlug) {
      items.push(nodeItem(l.sourceSlug, l.source, l.sourceType));
      seen.add(l.sourceSlug);
    }
    items.push({ type: "edge", link: l });
    items.push(nodeItem(l.targetSlug, l.target, l.targetType));
    seen.add(l.targetSlug);
    lastSlug = l.targetSlug;
  }
  // Mark only the final node terminal.
  for (let i = 0; i < items.length; i++) {
    if (items[i].type === "node") items[i].terminal = false;
  }
  for (let i = items.length - 1; i >= 0; i--) {
    if (items[i].type === "node") { items[i].terminal = true; break; }
  }
  return items;
}

// ---- Per-turn receipt model ------------------------------------------------
//
// Receipts accumulate into this for the CURRENT turn, then the chain + supporting
// cards render from it. Re-rendering (e.g. on the preconditions toggle) just
// re-reads the model.

let turn = freshTurn();
function freshTurn() {
  // upstream/downstream are kept SEPARATE (rendered as "what led to this" vs "what
  // followed") so a downstream consequence can never surface among the causes;
  // chainLinks is their union, used only for the degree badges + has-chain checks.
  return { chainLinks: [], upstream: [], downstream: [], enables: [], nodes: new Map(), resolves: [], neighbors: [], familyTrees: [], title: "", querySlug: null };
}

// The last turn that produced a chain. The featured chain persists across a
// failed/empty turn (design fix): a new turn only REPLACES it once it has its
// own chain — so a "no scene here" answer never blanks the showpiece.
let lastGoodChain = null;

function addNode(slug, rec) {
  if (slug && rec) turn.nodes.set(slug, rec);
}

// ---- Quote / evidence atoms ------------------------------------------------

// The one book-quote renderer used everywhere — Bloodraven's answer prose, the
// dossier, chain edges, preconditions, neighbours. When speaker/source arrive as
// separate fields (prose markers, or a node with structured fields), the
// attribution sits OUTSIDE the quote marks; when they're absent the text already
// carries its own marks + "— speaker, source", so it renders as-is. A missing
// speaker or source simply drops out (handles quotes with no attributable voice).
// Trim one layer of leading/trailing DOUBLE quote marks (straight or curly) so a
// line the source already wrapped in quotes isn't double-wrapped when we add our
// own — no more dangling `"”`. Apostrophes/single quotes are left untouched.
function stripEdgeQuotes(s) {
  return String(s).replace(/^\s*["“”]+/, "").replace(/["“”]+\s*$/, "").trim();
}

function bookQuote(text, speaker, cite) {
  const spk = speaker ? cleanQuote(speaker) : "";
  const src = prettyCite(cite);
  // Some curated quotes bake the chapter into BOTH the attribution and the cite;
  // don't print the source twice.
  const attr = (src && !spk.includes(src) ? [spk, src] : [spk]).filter(Boolean).join(", ");
  const body = cleanQuote(text);
  if (attr) {
    return el("blockquote", { class: "bookquote" }, [
      el("span", { class: "bq-text" }, `“${stripEdgeQuotes(body)}”`),
      el("span", { class: "bq-attr" }, `— ${attr}`),
    ]);
  }
  return el("blockquote", { class: "bookquote" }, el("span", { class: "bq-text" }, body));
}

// Parse a [[q|…]] marker's inner text into {text, speaker, cite}, tolerant of
// 1–3 fields: text; text + (speaker OR cite — a cite is detected by an .md:NN
// token); or text|speaker|cite.
function parseQuoteFields(inner) {
  const parts = String(inner).split("|");
  const text = parts[0] || "";
  let speaker = "", cite = "";
  if (parts.length >= 3) {
    speaker = parts[1];
    cite = parts.slice(2).join("|");
  } else if (parts.length === 2) {
    if (/\.md:\d+|chapters\//.test(parts[1])) cite = parts[1];
    else speaker = parts[1];
  }
  return { text, speaker, cite };
}

// Render streamed answer prose: [[q|…]] markers become styled bookQuote blocks,
// the rest stays text. Streaming-safe — an incomplete trailing marker is hidden
// until it closes, so the reader never sees a half-typed "[[q|".
const QUOTE_MARK_RE = /\[\[q\|([\s\S]*?)\]\]/g;
function renderProse(buf) {
  const out = [];
  let last = 0, m;
  QUOTE_MARK_RE.lastIndex = 0;
  while ((m = QUOTE_MARK_RE.exec(buf)) !== null) {
    if (m.index > last) out.push(document.createTextNode(buf.slice(last, m.index)));
    const f = parseQuoteFields(m[1]);
    out.push(bookQuote(f.text, f.speaker, f.cite));
    last = m.index + m[0].length;
  }
  let tail = buf.slice(last);
  const open = tail.lastIndexOf("[[q|");
  if (open !== -1 && tail.indexOf("]]", open) === -1) tail = tail.slice(0, open);
  if (tail) out.push(document.createTextNode(tail));
  return out;
}

function quoteList(quotes) {
  return el("div", { class: "quotes" }, (quotes || []).map((q) => bookQuote(q.text, q.attribution, q.cite)));
}

function edgeEvidence(l) {
  const body = [];
  if (l.quote) body.push(bookQuote(l.quote, null, l.ref));
  else if (l.ref) body.push(el("span", { class: "cite" }, prettyCite(l.ref)));
  if (l.tier != null) body.push(el("span", { class: "tier-badge" }, `Tier ${l.tier}`));
  return body.length
    ? el("div", { class: "link-evidence" }, body)
    : el("div", { class: "link-evidence" }, el("span", { class: "cite" }, "no evidence quote on this edge"));
}

function edgePill(edgeType) {
  return el("span", { class: `edge-label ${etClass(edgeType)}` }, edgeType || "RELATED");
}

// ---- The chain walked: one deduped, annotated, vertical spine --------------
//
// A single layout now — the full-width "Band" was retired (S177). The typed-edge
// spine renders into the receipts rail (desktop) / below the prose (mobile). Each
// node appears ONCE (a node seen earlier collapses to a slim, still-clickable
// back-reference; a `·N` degree badge marks one several links touch). The clean
// CAUSES/TRIGGERS/MOTIVATES spine shows by default; the ENABLES precondition web
// hides behind ONE "show preconditions (+N)" toggle (progressive disclosure —
// keep the detail, one tap away). Every node opens its dossier (a live /api/node
// lookup); hovering a node lights the edges that touch it.

const receiptsEl = $("#receipts");
let walking = false; // true while a live turn is gathering, before the chain lands

// The preconditions toggle is sticky across turns (default: collapsed).
let showPre = localStorage.getItem("weirwood-show-pre") === "1";

// How many causal-spine links touch each node slug (drives the `·N` degree badge).
function degreeMap(rawLinks) {
  const d = new Map();
  for (const raw of rawLinks) {
    const l = normLink(raw);
    d.set(l.sourceSlug, (d.get(l.sourceSlug) || 0) + 1);
    d.set(l.targetSlug, (d.get(l.targetSlug) || 0) + 1);
  }
  return d;
}

function chainHeader(chainTurn) {
  return el("div", { class: "chain-header" }, [
    el("h2", { class: "chain-title" }, "The chain walked"),
    chainTurn.title ? el("p", { class: "chain-sub" }, chainTurn.title) : false,
    el("p", { class: "chain-hint" }, "click any node to open its record"),
  ]);
}

// One node in the spine — always a button that opens its dossier. The queried
// node is the hub; a repeat collapses to a slim back-reference; a degree badge
// marks a well-connected node. Hover lights the edges touching it (desktop).
function spineNode(it, degree) {
  const deg = degree.get(it.slug) || 0;
  const cls = "spine-node"
    + (it.queried ? " hub" : "")
    + (it.terminal ? " terminal" : "")
    + (it.repeat ? " repeat" : "");
  const head = el("div", { class: "node-head" }, [
    el("span", { class: "node-name" }, it.name),
    !it.repeat && it.nodeType ? el("span", { class: "node-type" }, prettyType(it.nodeType)) : false,
    !it.repeat && deg > 1
      ? el("span", { class: "node-degree", title: deg + " links in this chain" }, "·" + deg)
      : false,
  ]);
  return el("button", {
    class: cls, type: "button",
    dataset: { slug: it.slug },
    onclick: () => openDossier(it.slug, it.name),
    onmouseenter: () => highlightNode(it.slug),
    onmouseleave: clearHighlight,
  }, head);
}

// One edge in the spine — the evidence quote + cite + tier always visible (the
// edge IS the evidence). Carries its endpoint slugs so a node hover can light it.
function spineEdge(l) {
  return el("div", {
    class: "spine-edge " + etClass(l.edgeType),
    dataset: { src: l.sourceSlug, tgt: l.targetSlug },
  }, [
    el("div", { class: "spine-edge-head" }, [
      edgePill(l.edgeType),
      l.tier != null ? el("span", { class: "tier-inline" }, "Tier " + l.tier) : false,
    ]),
    l.quote
      ? bookQuote(l.quote, null, l.ref)
      : (l.ref ? el("span", { class: "spine-cite" }, prettyCite(l.ref)) : false),
  ]);
}

// The ENABLES precondition web, behind one toggle (progressive disclosure). Each
// row is a precondition that ENABLES a spine node — dimmed/indented, default
// hidden; the spine reads clean until the visitor asks for the fuller picture.
function preconditionsBlock(enables) {
  if (!enables || !enables.length) return false;
  const btn = el("button", {
    class: "pre-toggle" + (showPre ? " open" : ""),
    type: "button",
    "aria-expanded": String(showPre),
    onclick: () => {
      showPre = !showPre;
      localStorage.setItem("weirwood-show-pre", showPre ? "1" : "0");
      renderReceipts();
    },
  }, showPre ? "hide preconditions" : `show preconditions (+${enables.length})`);

  if (!showPre) return el("div", { class: "pre-wrap" }, btn);

  const preNode = (slug, name) =>
    el("button", { class: "pre-node", type: "button", onclick: () => openDossier(slug, name) }, name);

  const rows = enables.map((raw) => {
    const l = normLink(raw);
    return el("div", { class: "pre-row" }, [
      el("div", { class: "pre-row-head" }, [
        preNode(l.sourceSlug, l.source),
        edgePill("ENABLES"),
        preNode(l.targetSlug, l.target),
      ]),
      l.quote
        ? bookQuote(l.quote, null, l.ref)
        : (l.ref ? el("span", { class: "spine-cite" }, prettyCite(l.ref)) : false),
    ]);
  });
  return el("div", { class: "pre-wrap open" }, [btn, el("div", { class: "pre-list" }, rows)]);
}

// One direction's spine: the deduped node/edge sequence for a link list, as a
// labelled section. Returns false for an empty direction (rendered nothing).
function spineSection(label, links, querySlug, degree) {
  if (!links || !links.length) return false;
  const flow = el("div", { class: "chain-flow spine" });
  for (const it of buildSequence(links, querySlug)) {
    flow.append(it.type === "node" ? spineNode(it, degree) : spineEdge(it.link));
  }
  return el("div", { class: "chain-section" }, [
    el("p", { class: "chain-section-label" }, label),
    flow,
  ]);
}

// The causal chain, rendered as TWO separate story-time-ordered sections —
// antecedents ("what led to this") and consequences ("what followed") — never
// merged into one list, so a downstream consequence can't read as a cause (S185).
// The queried event is the pivot each section runs to/from.
function renderSpine(chainTurn) {
  const degree = degreeMap(chainTurn.chainLinks);
  receiptsEl.append(el("div", { class: "card chain-card" }, [
    chainHeader(chainTurn),
    spineSection("What led to this", chainTurn.upstream, chainTurn.querySlug, degree),
    spineSection("What followed", chainTurn.downstream, chainTurn.querySlug, degree),
    preconditionsBlock(chainTurn.enables),
  ]));
}

// ---- Hover-peek: light the edges a node touches (desktop affordance) --------
// Touch never fires mouseenter, so this is inert on mobile.
let hotFlows = [];
function highlightNode(slug) {
  const flows = [...receiptsEl.querySelectorAll(".chain-flow.spine")]; // both sections
  if (!flows.length) return;
  hotFlows = flows;
  for (const flow of flows) {
    flow.classList.add("has-hot");
    for (const edge of flow.querySelectorAll(".spine-edge")) {
      edge.classList.toggle("hot", edge.dataset.src === slug || edge.dataset.tgt === slug);
    }
    for (const node of flow.querySelectorAll(".spine-node")) {
      node.classList.toggle("hot", node.dataset.slug === slug);
    }
  }
}
function clearHighlight() {
  for (const flow of hotFlows) {
    flow.classList.remove("has-hot");
    for (const hot of flow.querySelectorAll(".hot")) hot.classList.remove("hot");
  }
  hotFlows = [];
}

// ---- Node dossier: a live /api/node lookup in a modal over the page ---------
//
// Every chain node opens here. The chain receipts carry only name+type; the
// dossier fetches the FULL node (identity prose + every curated book quote) from
// the graph — the proof the nodes are live, not baked into a transcript. A
// generation counter makes the latest open win (a stale fetch never overwrites a
// newer one, and closing mid-flight discards the result).

const dossierEl = $("#dossier");
let dossierGen = 0;

function dossierShell(children) {
  return el("div", { class: "dossier-card", role: "dialog", "aria-modal": "true", "aria-label": "Node detail" }, [
    el("button", { class: "dossier-close", type: "button", "aria-label": "Close", onclick: closeDossier }, "✕"),
    el("div", { class: "dossier-body" }, children),
  ]);
}

function closeDossier() {
  dossierGen++; // invalidate any in-flight fetch
  dossierEl.hidden = true;
  dossierEl.replaceChildren();
  document.body.classList.remove("dossier-open");
}

async function openDossier(slug, fallbackName) {
  if (!slug) return;
  const gen = ++dossierGen;
  const label = fallbackName || pretty(slug);
  document.body.classList.add("dossier-open");
  dossierEl.hidden = false;
  dossierEl.replaceChildren(dossierShell(el("p", { class: "dossier-loading" }, `Reading ${label}…`)));

  let children;
  try {
    const res = await fetch(`/api/node?slug=${encodeURIComponent(slug)}`);
    if (res.status === 404) {
      children = [
        el("div", { class: "dossier-head" }, [el("h3", {}, label), el("code", { class: "dossier-slug" }, slug)]),
        el("p", { class: "dossier-empty" }, "No node by that slug in the graph."),
      ];
    } else if (!res.ok) {
      throw new Error("status " + res.status);
    } else {
      const node = await res.json();
      // The nodes' `## Identity` is wiki-derived; 81% of it is the useless
      // boilerplate "<name> is a <type> from the AWOIAF wiki." — never show that
      // (a character is from the BOOKS, not the wiki). Real identity prose IS
      // shown, but labelled "From the wiki" so its provenance is explicit.
      const wikiIdentity = isWikiBoilerplate(node.identity) ? "" : cleanQuote(node.identity || "");
      children = [
        el("div", { class: "dossier-head" }, [
          el("h3", {}, node.name || label),
          node.type ? el("span", { class: "dossier-type" }, prettyType(node.type)) : false,
        ]),
        wikiIdentity
          ? el("div", { class: "dossier-wiki" }, [
              el("div", { class: "dossier-sub" }, "From the wiki"),
              el("p", { class: "dossier-identity" }, wikiIdentity),
            ])
          : false,
        node.quotes && node.quotes.length
          ? el("div", { class: "dossier-quotes" }, [el("div", { class: "dossier-sub" }, "From the books"), quoteList(node.quotes)])
          : el("p", { class: "dossier-empty" }, "No curated book quotes on this node yet."),
      ];
    }
  } catch (_err) {
    children = el("p", { class: "dossier-empty" }, "Could not reach the graph for this node.");
  }
  if (gen !== dossierGen) return; // a newer dossier opened, or it was closed
  dossierEl.replaceChildren(dossierShell(children));
}

// Close on backdrop click or Escape.
dossierEl.addEventListener("click", (e) => { if (e.target === dossierEl) closeDossier(); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !dossierEl.hidden) closeDossier(); });

// ---- Supporting receipts (resolve / neighbors) into the sidebar ------------

function resolveCard(phrase, cands) {
  const top = (cands || []).slice(0, 3).map((c) =>
    el("div", { class: "resolve-line" }, [el("code", {}, c.slug), ` · ${c.category}${c.matchType ? ` (${c.matchType})` : ""}`]));
  return el("div", { class: "card" }, [
    el("div", { class: "card-kind" }, [el("span", { class: "glyph" }, "⌕"), "resolve"]),
    el("div", { class: "resolve-line" }, [`“${phrase}” →`]),
    top.length ? top : el("div", { class: "resolve-line" }, "no match"),
  ]);
}

function neighborsCard(result) {
  const groups = [];
  for (const [dir, mark] of [["outgoing", "→"], ["incoming", "←"]]) {
    for (const [type, links] of Object.entries(result[dir] || {})) {
      groups.push(el("div", { class: "neigh-group" }, [
        el("span", { class: `edge-label ${etClass(type)}` }, `${mark} ${type}`),
        el("div", { class: "chain spine" }, (links || []).map((lk) => {
          const l = normLink(lk);
          return el("details", { class: `spine-edge ${etClass(l.edgeType)}` }, [
            el("summary", {}, [el("span", { class: "node-name" }, l.target || l.source)]),
            edgeEvidence(l),
          ]);
        })),
      ]));
    }
  }
  return el("div", { class: "card" }, [
    el("div", { class: "card-kind" }, [el("span", { class: "glyph" }, "✦"), "neighbors"]),
    groups.length ? groups : el("div", { class: "resolve-line" }, "no connections"),
  ]);
}

// ---- The family tree: a generational ladder of the lineage -----------------
//
// A dynasty/lineage query (family_tree receipt) is NOT a causal spine — it is
// kin banded by generation, ancestors at the top down to descendants. Each
// generation is a labelled row of people; married couples in the same generation
// are joined by a ⚭. Every person with a node is a button that opens the same
// dossier the chain nodes use; a name the graph names but has no node of its own
// renders as plain, dimmed text (nothing to open). The queried root is the hub.

/** A generation offset → a kinship band label, relative to the queried root. */
function ftGenLabel(g, rootName) {
  if (g === 0) return rootName ? `${rootName} & siblings` : "This generation";
  const n = Math.abs(g);
  if (n === 1) return g < 0 ? "Parents" : "Children";
  const greats = "Great-".repeat(n - 2);
  return greats + (g < 0 ? "Grandparents" : "Grandchildren");
}

/** One person chip — a dossier button when the graph holds a node, else plain text. */
function ftChip(m, rootSlug) {
  const cls = "ft-node" + (m.slug === rootSlug ? " hub" : "") + (m.hasNode ? "" : " no-node");
  if (!m.hasNode) return el("span", { class: cls, title: "no node in the graph" }, m.name);
  return el("button", {
    class: cls, type: "button",
    dataset: { slug: m.slug },
    onclick: () => openDossier(m.slug, m.name),
  }, m.name);
}

function familyTreeCard(result) {
  const rootSlug = result.root;
  // Spouse lookup, so a couple in the same generation renders joined.
  const spouseOf = new Map();
  for (const b of result.spouseBonds || []) {
    (spouseOf.get(b.a) || spouseOf.set(b.a, new Set()).get(b.a)).add(b.b);
    (spouseOf.get(b.b) || spouseOf.set(b.b, new Set()).get(b.b)).add(b.a);
  }

  // Bucket members by generation.
  const byGen = new Map();
  for (const m of result.members) {
    if (!byGen.has(m.generation)) byGen.set(m.generation, []);
    byGen.get(m.generation).push(m);
  }
  const gens = [...byGen.keys()].sort((a, b) => a - b);

  const rows = gens.map((g) => {
    const people = byGen.get(g);
    const bySlug = new Map(people.map((m) => [m.slug, m]));
    const done = new Set();
    const items = [];
    for (const m of people) {
      if (done.has(m.slug)) continue;
      done.add(m.slug);
      // Pull in a spouse who sits in this same generation, as a joined couple.
      const mate = [...(spouseOf.get(m.slug) || [])].find((s) => bySlug.has(s) && !done.has(s));
      if (mate) {
        done.add(mate);
        items.push(el("span", { class: "ft-couple" }, [
          ftChip(m, rootSlug),
          el("span", { class: "ft-marr", title: "married" }, "⚭"),
          ftChip(bySlug.get(mate), rootSlug),
        ]));
      } else {
        items.push(ftChip(m, rootSlug));
      }
    }
    return el("div", { class: "ft-gen" }, [
      el("div", { class: "ft-gen-label" }, ftGenLabel(g, result.rootName)),
      el("div", { class: "ft-gen-row" }, items),
    ]);
  });

  const rootName = result.rootName || pretty(result.root);
  const count = result.memberCount != null ? result.memberCount : result.members.length;
  return el("div", { class: "card ft-card" }, [
    el("div", { class: "card-kind" }, [el("span", { class: "glyph" }, "⚶"), "family tree"]),
    el("div", { class: "ft-root-label" }, [
      rootName,
      el("span", { class: "ft-count" }, ` · ${count} kin${result.truncated ? " (pruned)" : ""}`),
    ]),
    ...rows,
  ]);
}

// ---- The family-tree DIAGRAM: an SVG descendant chart, in the chat ----------
//
// The rail card (above) is the structured receipt; THIS is the picture people
// actually want for a lineage question — a real node-link tree drawn into the
// answer itself (persona narration is dropped for this shape). Layout is a tidy
// top-down descendant tree: root at top, each child below its parent, sub-tree
// x-positions assigned post-order so parents centre over their children
// (Reingold–Tilford-lite). Only descendants reachable from the root via
// PARENT_OF are drawn — ancestors + married-in spouses live in the rail card.
// Every node is clickable → the same dossier the chain/rail nodes open.

const SVGNS = "http://www.w3.org/2000/svg";
function svgEl(tag, attrs = {}, children = []) {
  const n = document.createElementNS(SVGNS, tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === false || v == null) continue;
    n.setAttribute(k, v);
  }
  for (const c of [].concat(children).flat(Infinity)) {
    if (c == null || c === false) continue;
    n.append(c.nodeType ? c : document.createTextNode(String(c)));
  }
  return n;
}

// A full name → 1–2 short label lines. Parentheticals ("(son of Aenys I)") drop
// to a second line; long plain names wrap at a space; the full name lives in a
// <title> tooltip so nothing is lost.
function nameLines(name) {
  const paren = String(name).match(/^(.*?)\s*(\(.*\))$/);
  if (paren) return [paren[1].trim(), paren[2].trim()];
  if (name.length <= 20) return [name];
  const words = name.split(" ");
  if (words.length > 1) {
    let l1 = "", i = 0;
    while (i < words.length && (l1 + " " + words[i]).trim().length <= 18) { l1 = (l1 + " " + words[i]).trim(); i++; }
    const l2 = words.slice(i).join(" ");
    return l2 ? [l1, l2] : [l1];
  }
  return [name];
}
const clip = (s, n) => (s.length > n ? s.slice(0, n - 1) + "…" : s);

const FT_NODE_W = 148, FT_NODE_H = 38, FT_X_GAP = 44, FT_Y_GAP = 10, FT_PAD = 16;

// Prominence tiers: prominence = degree + 4*quoteCount (computed in graph.ts
// familyTree). Marquee kin (Dany, Rhaegar, Egg, Daemon...) clear P_MAJOR and get
// the accent fill + a "worth a click" dot; historical filler / bare-surname stubs
// fall to tier-minor and visually recede. Cutoffs mirror web/dev/family-tree-fixture.html.
const FT_P_MAJOR = 40, FT_P_NOTABLE = 12;
const ftTierOf = (p) => (p >= FT_P_MAJOR ? "major" : p >= FT_P_NOTABLE ? "notable" : "minor");

/** Lay out the root's descendants as a tidy LEFT-TO-RIGHT tree: root at the left,
 *  each generation a column to its right, siblings stacked vertically. A deep
 *  dynasty stays narrow (a few generation-columns) and grows DOWN (natural
 *  vertical scroll) instead of ballooning sideways. Returns positioned nodes +
 *  parent→child elbow edges + the canvas size + the root's y (for auto-centring),
 *  or null if the root has no drawable descendants. */
function descendantLayout(result) {
  const rootSlug = result.root;
  const member = new Map(result.members.map((m) => [m.slug, m]));
  if (!member.has(rootSlug)) return null;

  // children adjacency within the member set.
  const kids = new Map();
  for (const b of result.parentBonds || []) {
    if (!member.has(b.parent) || !member.has(b.child)) continue;
    (kids.get(b.parent) || kids.set(b.parent, []).get(b.parent)).push(b.child);
  }

  // Spanning tree from root (BFS): each node gets ONE tree-parent, so the DAG
  // (incest, two-parent edges) draws as a clean tree; the extra parent is a
  // spouse shown in the rail card.
  const treeParent = new Map();
  const seen = new Set([rootSlug]);
  const q = [rootSlug];
  const tkids = new Map();
  while (q.length) {
    const n = q.shift();
    for (const c of kids.get(n) || []) {
      if (seen.has(c)) continue;
      seen.add(c);
      treeParent.set(c, n);
      (tkids.get(n) || tkids.set(n, []).get(n)).push(c);
      q.push(c);
    }
  }
  if (seen.size <= 1) return null; // root alone — no tree to draw

  // Depth = generation column (BFS guarantees parent before child).
  const depth = new Map([[rootSlug, 0]]);
  const bfs = [rootSlug];
  for (let i = 0; i < bfs.length; i++) {
    const n = bfs[i];
    for (const c of tkids.get(n) || []) { depth.set(c, depth.get(n) + 1); bfs.push(c); }
  }

  // Post-order row-slots: leaves take the next row; parents centre on their kids.
  const slot = new Map();
  let next = 0;
  const assign = (n) => {
    const ch = tkids.get(n) || [];
    if (!ch.length) { slot.set(n, next++); return; }
    ch.forEach(assign);
    slot.set(n, (slot.get(ch[0]) + slot.get(ch[ch.length - 1])) / 2);
  };
  assign(rootSlug);

  const stepX = FT_NODE_W + FT_X_GAP, stepY = FT_NODE_H + FT_Y_GAP;
  const pos = new Map();
  for (const n of seen) {
    pos.set(n, {
      x: FT_PAD + depth.get(n) * stepX, // depth → column (left to right)
      y: FT_PAD + slot.get(n) * stepY, // sibling order → row (top to bottom)
      m: member.get(n),
    });
  }
  const maxDepth = Math.max(...[...depth.values()]);
  return {
    pos,
    edges: [...treeParent].map(([c, p]) => [p, c]),
    width: FT_PAD * 2 + (maxDepth + 1) * stepX,
    height: FT_PAD * 2 + next * stepY,
    rootY: pos.get(rootSlug).y,
    count: seen.size,
  };
}

// Builds a fresh <svg> node-link tree from a layout — called once per mount
// (inline preview and the expanded modal each need their own SVG instance).
function buildTreeSVG(result, layout) {
  // Elbow from a parent's RIGHT edge to its child's LEFT edge (left-to-right tree).
  const edgeEls = layout.edges.map(([p, c]) => {
    const a = layout.pos.get(p), b = layout.pos.get(c);
    const x1 = a.x + FT_NODE_W, y1 = a.y + FT_NODE_H / 2;
    const x2 = b.x, y2 = b.y + FT_NODE_H / 2;
    const midX = (x1 + x2) / 2;
    return svgEl("path", {
      class: "ft-link",
      d: `M ${x1} ${y1} H ${midX} V ${y2} H ${x2}`,
      fill: "none",
    });
  });

  const nodeEls = [...layout.pos.values()].map(({ x, y, m }) => {
    const lines = nameLines(m.name);
    const isRoot = m.slug === result.root;
    const tier = ftTierOf(m.prominence || 0);
    const g = svgEl("g", {
      class: `ft-dnode tier-${tier}` + (isRoot ? " hub" : "") + (m.hasNode ? "" : " no-node"),
      transform: `translate(${x} ${y})`,
    });
    g.dataset.slug = m.slug;
    g.dataset.prom = m.prominence;
    if (m.hasNode) { g.setAttribute("role", "button"); g.setAttribute("tabindex", "0"); }
    g.append(svgEl("title", {}, `${m.name} — prominence ${m.prominence} (degree ${m.degree}, ${m.quoteCount} quotes)`));
    g.append(svgEl("rect", { class: "ft-dnode-box", width: FT_NODE_W, height: FT_NODE_H, rx: 6 }));
    // A small accent dot on marquee kin = "this one's worth a click".
    if (tier === "major") g.append(svgEl("circle", { class: "ft-prom-dot", cx: FT_NODE_W - 8, cy: 8, r: 3 }));
    const text = svgEl("text", { class: "ft-dnode-text", x: FT_NODE_W / 2, y: lines.length > 1 ? FT_NODE_H / 2 - 6 : FT_NODE_H / 2 });
    lines.forEach((ln, i) => {
      text.append(svgEl("tspan", { x: FT_NODE_W / 2, dy: i === 0 ? 0 : 14, class: i === 0 ? "ln1" : "ln2" }, clip(ln, 22)));
    });
    g.append(text);
    return g;
  });

  const svg = svgEl("svg", {
    class: "ft-diagram",
    width: layout.width,
    height: layout.height,
    viewBox: `0 0 ${layout.width} ${layout.height}`,
  }, [svgEl("g", { class: "ft-links" }, edgeEls), svgEl("g", { class: "ft-nodes" }, nodeEls)]);

  // One delegated click/keydown → open the dossier for the clicked person.
  const open = (target) => {
    const g = target.closest?.(".ft-dnode");
    if (g && g.classList.contains("no-node") === false && g.dataset.slug) openDossier(g.dataset.slug, g.querySelector("title")?.textContent);
  };
  svg.addEventListener("click", (e) => open(e.target));
  svg.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(e.target); } });
  return svg;
}

// ---- Tree modal: the same descendant chart, popped out full-size ----------
// The inline rail preview is squeezed into a 62vh scroll box; a deep dynasty
// is easier to read blown up in a modal (same overlay language as the node
// dossier). Rebuilds its own SVG instance from the cached layout/result.

const treeModalEl = $("#tree-modal");

function closeTreeModal() {
  treeModalEl.hidden = true;
  treeModalEl.replaceChildren();
  document.body.classList.remove("tree-modal-open");
}

function openTreeModal(result, layout, rootName) {
  const svg = buildTreeSVG(result, layout);
  const scroll = el("div", { class: "ft-modal-scroll" }, svg);
  scroll.dataset.rootY = String(layout.rootY + FT_NODE_H / 2);
  const card = el("div", { class: "ft-modal-card", role: "dialog", "aria-modal": "true", "aria-label": "Family tree" }, [
    el("button", { class: "dossier-close", type: "button", "aria-label": "Close", onclick: closeTreeModal }, "✕"),
    el("figcaption", { class: "ft-diagram-cap" }, [
      `${rootName} — descendants`,
      el("span", { class: "ft-diagram-sub" }, ` · ${layout.count} shown${result.truncated ? " (pruned)" : ""} · click a name`),
    ]),
    scroll,
  ]);
  treeModalEl.replaceChildren(card);
  treeModalEl.hidden = false;
  document.body.classList.add("tree-modal-open");
  // Auto-centre the root vertically, same as the inline preview does.
  requestAnimationFrame(() => { scroll.scrollTop = Math.max(0, layout.rootY + FT_NODE_H / 2 - scroll.clientHeight / 2); });
}

treeModalEl.addEventListener("click", (e) => { if (e.target === treeModalEl) closeTreeModal(); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !treeModalEl.hidden) closeTreeModal(); });

function familyTreeDiagram(result) {
  const layout = descendantLayout(result);
  const rootName = result.rootName || pretty(result.root);
  if (!layout) {
    // Nothing to draw (no descendants in graph) — a plain line, no empty canvas.
    return el("figure", { class: "ft-diagram-wrap" }, [
      el("figcaption", { class: "ft-diagram-cap" }, `${rootName} — no descendants recorded in the graph.`),
    ]);
  }

  const svg = buildTreeSVG(result, layout);
  const scroll = el("div", { class: "ft-diagram-scroll" }, svg);
  scroll.dataset.rootY = String(layout.rootY + FT_NODE_H / 2);
  return el("figure", { class: "ft-diagram-wrap" }, [
    el("figcaption", { class: "ft-diagram-cap" }, [
      `${rootName} — descendants`,
      el("span", { class: "ft-diagram-sub" }, ` · ${layout.count} shown${result.truncated ? " (pruned)" : ""} · click a name`),
      el("button", {
        class: "ft-expand-btn", type: "button", "aria-label": "Open family tree full-size",
        onclick: () => openTreeModal(result, layout, rootName),
      }, "⤢ expand"),
    ]),
    scroll,
  ]);
}

// ---- The master render -----------------------------------------------------

function renderReceipts() {
  // The chain renders from the current turn once it has one, otherwise from the
  // last good chain — so a failed or chain-less turn never blanks the showpiece.
  const chainTurn = turn.chainLinks.length ? turn : (lastGoodChain || turn);
  const hasChain = chainTurn.chainLinks.length > 0;
  const supporting = [
    ...turn.resolves.map((r) => resolveCard(r.phrase, r.cands)),
    ...turn.neighbors.map((n) => neighborsCard(n)),
  ];

  receiptsEl.replaceChildren();
  // A family tree is the star of a lineage query — render it above the spine.
  for (const ft of turn.familyTrees) receiptsEl.append(familyTreeCard(ft));
  if (hasChain) renderSpine(chainTurn);
  for (const card of supporting) receiptsEl.append(card);
  if (!hasChain && supporting.length === 0 && turn.familyTrees.length === 0) {
    receiptsEl.append(el("p", { class: "receipts-empty" },
      walking ? "walking the graph…" : "Ask a question — the chain of cause and consequence it walks appears here."));
  }
}

// ---- Thread state ----------------------------------------------------------

const threadEl = $("#thread");
const history = [];
const MAX_HISTORY = 8;

function addUserBubble(text) {
  document.body.classList.remove("landing"); // first question → composer sticks to the bottom
  threadEl.append(el("div", { class: "msg user" }, [
    el("div", { class: "msg-role" }, "you"),
    el("div", { class: "bubble" }, text),
  ]));
  scrollIn();
}

function addBotBubble() {
  const bubble = el("div", { class: "bubble" }, "");
  const wrap = el("div", { class: "msg bot streaming" }, [
    el("div", { class: "msg-role" }, "the three-eyed raven"),
    bubble,
  ]);
  threadEl.append(wrap);
  scrollIn();
  let buf = "";
  // Paint the whole buffer each token: [[q|…]] markers become styled quote blocks,
  // the rest stays text. Re-parsing the full (short) reply per token is cheap and
  // keeps streaming correct as a marker completes mid-stream.
  const paint = () => bubble.replaceChildren(...renderProse(buf));
  return {
    append(t) { buf += t; paint(); scrollIn(); },
    setText(t) { buf = t; paint(); },
    bubbleEl: bubble,
    // Mount a family-tree diagram as the answer. The picture is what a lineage
    // question wants, so it leads; the persona prose is suppressed to a thin
    // caption (bubble gets `.as-caption`). Replaces any prior diagram this turn.
    mountDiagram(node) {
      wrap.classList.add("has-diagram");
      const prior = wrap.querySelector(".ft-diagram-wrap");
      if (prior) prior.replaceWith(node);
      else wrap.insertBefore(node, bubble);
      // Open on the root: left column visible, root row centred vertically. Run
      // after layout (rAF) so clientHeight is real, not 0 mid-stream.
      const sc = node.querySelector(".ft-diagram-scroll");
      if (sc) {
        const center = () => {
          sc.scrollLeft = 0;
          const ry = Number(sc.dataset.rootY || 0);
          sc.scrollTop = Math.max(0, ry - sc.clientHeight / 2);
        };
        center();
        requestAnimationFrame(center);
      }
      scrollIn();
    },
    finish() { wrap.classList.remove("streaming"); paint(); return buf; },
  };
}

function scrollIn() {
  threadEl.lastElementChild?.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// ---- Status / failure-mode UX (design §9) ----------------------------------

const STATUS_UX = {
  "no-grounding": { cls: "warn", head: "The graph holds no scene here yet.", body: "Nothing in the network grounds this one — so it goes unanswered rather than invented. Try another name or event." },
  "loop-bound-hit": { cls: "warn", head: "The search was bounded.", body: "The loremaster reached its limit of graph steps for this question. The answer above is what it gathered within that bound." },
  "unverified-cites": { cls: "warn", head: "A citation could not be verified.", body: "One or more cited lines were not among what the tools returned this turn — flagged rather than shown as canon." },
  "api-error": { cls: "error", head: "The connection to the model failed.", body: "Something broke reaching the model. Ask again in a moment." },
  "cost-cap-tripped": { cls: "error", head: "The loremaster has answered enough for today.", body: "This is a small portfolio demo with a daily ceiling, and it has been reached. Come back tomorrow — or read the featured exchange above." },
};

function showStatus(state) {
  const ux = STATUS_UX[state] || { cls: "warn", head: state, body: "" };
  threadEl.append(el("div", { class: `status-line ${ux.cls}` }, [
    el("span", { class: "status-head" }, ux.head), ux.body,
  ]));
  scrollIn();
}

function showError(message) {
  threadEl.append(el("div", { class: "status-line error" }, [
    el("span", { class: "status-head" }, "Error"), message || "Something went wrong.",
  ]));
  scrollIn();
}

// ---- SSE client ------------------------------------------------------------

async function readSse(response, onEvent) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buf = "";
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    let sep;
    while ((sep = buf.indexOf("\n\n")) !== -1) {
      const frame = buf.slice(0, sep);
      buf = buf.slice(sep + 2);
      let event = "message";
      const dataLines = [];
      for (const line of frame.split("\n")) {
        if (line.startsWith("event:")) event = line.slice(6).trim();
        else if (line.startsWith("data:")) dataLines.push(line.slice(5).trim());
      }
      if (!dataLines.length) continue;
      let data = {};
      try { data = JSON.parse(dataLines.join("\n")); } catch { /* keep {} */ }
      onEvent(event, data);
    }
  }
}

let busy = false;
const inputEl = $("#input");
const sendBtn = $("#send");
const noteEl = $("#composer-note");

function ingestReceipt({ tool, input, result }) {
  switch (tool) {
    case "resolve":
      turn.resolves.push({ phrase: input?.phrase ?? "", cands: Array.isArray(result) ? result : [] });
      break;
    case "read_node":
      if (result) addNode(input?.slug ?? result.slug ?? result.name, result);
      break;
    case "walk_chain":
      if (result) {
        if (result.slug) turn.querySlug = result.slug;
        // walkChain already returns each direction in story-time order (S185); keep
        // them apart for the two-section render. chainLinks is the union.
        const up = result.upstream || [];
        const down = result.downstream || [];
        turn.upstream.push(...up);
        turn.downstream.push(...down);
        turn.chainLinks.push(...up, ...down);
        if (Array.isArray(result.enables)) turn.enables = result.enables;
      }
      break;
    case "neighbors":
      if (result) turn.neighbors.push(result);
      break;
    case "family_tree":
      if (result && Array.isArray(result.members) && result.members.length) turn.familyTrees.push(result);
      break;
  }
}

async function ask(question) {
  if (busy || !question.trim()) return;
  busy = true;
  sendBtn.disabled = true;
  noteEl.textContent = "";

  addUserBubble(question);
  history.push({ role: "user", content: question });
  while (history.length > MAX_HISTORY) history.shift();

  turn = freshTurn();
  walking = true;
  renderReceipts();

  const bot = addBotBubble();
  let answered = false;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ messages: history }),
    });
    if (!res.ok || !res.body) {
      showError(`The model endpoint returned ${res.status}.`);
      bot.finish();
      return;
    }
    await readSse(res, (event, data) => {
      switch (event) {
        case "token":
          if (data.text) { bot.append(data.text); answered = true; }
          break;
        case "receipt":
          ingestReceipt(data);
          renderReceipts();
          // A lineage answer is a picture: draw the tree into the chat itself.
          if (data.tool === "family_tree" && data.result && Array.isArray(data.result.members) && data.result.members.length) {
            bot.mountDiagram(familyTreeDiagram(data.result));
          }
          break;
        case "status":
          showStatus(data.state);
          break;
        case "error":
          showError(data.message);
          break;
        case "cite-check":
          if (data.unverified?.length) console.warn("unverified cites:", data.unverified);
          break;
        case "done":
          renderReceipts();
          break;
      }
    });
  } catch (err) {
    showError("Lost the connection to the three-eyed raven.");
    console.error(err);
  } finally {
    walking = false;
    // Promote this turn's chain to the persisted showpiece only if it produced
    // one — a failed/chain-less turn leaves the prior chain standing.
    if (turn.chainLinks.length) lastGoodChain = turn;
    renderReceipts();
    const finalProse = bot.finish();
    if (answered && finalProse.trim()) {
      history.push({ role: "assistant", content: finalProse });
      while (history.length > MAX_HISTORY) history.shift();
    }
    busy = false;
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

// ---- Wiring ----------------------------------------------------------------

$("#composer").addEventListener("submit", (e) => {
  e.preventDefault();
  const q = inputEl.value;
  inputEl.value = "";
  autosize();
  ask(q);
});

inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    $("#composer").requestSubmit();
  }
});

inputEl.addEventListener("input", autosize);
function autosize() {
  inputEl.style.height = "auto";
  inputEl.style.height = Math.min(inputEl.scrollHeight, 144) + "px";
}

// About view: the page opens to the chat; the header button swaps in the "what
// is this" framing (and back). Driven by a body class so CSS owns the show/hide.
const aboutToggle = $("#about-toggle");
function setAbout(open) {
  document.body.classList.toggle("about-open", open);
  aboutToggle.setAttribute("aria-expanded", String(open));
  aboutToggle.textContent = open ? "← Chat" : "About";
  if (open) window.scrollTo({ top: 0, behavior: "smooth" });
}
aboutToggle.addEventListener("click", () => setAbout(!document.body.classList.contains("about-open")));
$("#about-back").addEventListener("click", () => setAbout(false));

// Clean landing: empty thread + empty receipts rail, ready for the first question.
renderReceipts();
