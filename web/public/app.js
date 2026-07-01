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
  return { chainLinks: [], enables: [], nodes: new Map(), resolves: [], neighbors: [], title: "", querySlug: null };
}

// The last turn that produced a chain. The featured chain persists across a
// failed/empty turn (design fix): a new turn only REPLACES it once it has its
// own chain — so a "no scene here" answer never blanks the showpiece.
let lastGoodChain = null;

function addChainLinks(links, title) {
  turn.chainLinks.push(...links);
  if (title) turn.title = title;
}
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

function renderSpine(seq, chainTurn) {
  const degree = degreeMap(chainTurn.chainLinks);
  const flow = el("div", { class: "chain-flow spine" });
  for (const it of seq) {
    flow.append(it.type === "node" ? spineNode(it, degree) : spineEdge(it.link));
  }
  receiptsEl.append(el("div", { class: "card chain-card" }, [
    chainHeader(chainTurn),
    flow,
    preconditionsBlock(chainTurn.enables),
  ]));
}

// ---- Hover-peek: light the edges a node touches (desktop affordance) --------
// Touch never fires mouseenter, so this is inert on mobile.
let hotFlow = null;
function highlightNode(slug) {
  const flow = receiptsEl.querySelector(".chain-flow.spine");
  if (!flow) return;
  hotFlow = flow;
  flow.classList.add("has-hot");
  for (const edge of flow.querySelectorAll(".spine-edge")) {
    edge.classList.toggle("hot", edge.dataset.src === slug || edge.dataset.tgt === slug);
  }
  for (const node of flow.querySelectorAll(".spine-node")) {
    node.classList.toggle("hot", node.dataset.slug === slug);
  }
}
function clearHighlight() {
  if (!hotFlow) return;
  hotFlow.classList.remove("has-hot");
  for (const hot of hotFlow.querySelectorAll(".hot")) hot.classList.remove("hot");
  hotFlow = null;
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
      children = [
        el("div", { class: "dossier-head" }, [
          el("h3", {}, node.name || label),
          node.type ? el("span", { class: "dossier-type" }, prettyType(node.type)) : false,
        ]),
        node.identity ? el("p", { class: "dossier-identity" }, cleanQuote(node.identity)) : false,
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

// ---- The master render -----------------------------------------------------

function renderReceipts() {
  // The chain renders from the current turn once it has one, otherwise from the
  // last good chain — so a failed or chain-less turn never blanks the showpiece.
  const chainTurn = turn.chainLinks.length ? turn : (lastGoodChain || turn);
  const seq = buildSequence(chainTurn.chainLinks, chainTurn.querySlug);
  const hasChain = seq.length > 0;
  const supporting = [
    ...turn.resolves.map((r) => resolveCard(r.phrase, r.cands)),
    ...turn.neighbors.map((n) => neighborsCard(n)),
  ];

  receiptsEl.replaceChildren();
  if (hasChain) renderSpine(seq, chainTurn);
  for (const card of supporting) receiptsEl.append(card);
  if (!hasChain && supporting.length === 0) {
    receiptsEl.append(el("p", { class: "receipts-empty" },
      walking ? "walking the graph…" : "Ask a question to see the chain the loremaster walks."));
  }
}

// ---- Thread state ----------------------------------------------------------

const threadEl = $("#thread");
const history = [];
const MAX_HISTORY = 8;

function addUserBubble(text) {
  threadEl.append(el("div", { class: "msg user" }, [
    el("div", { class: "msg-role" }, "you"),
    el("div", { class: "bubble" }, text),
  ]));
  scrollIn();
}

function addBotBubble() {
  const bubble = el("div", { class: "bubble" }, "");
  const wrap = el("div", { class: "msg bot streaming" }, [
    el("div", { class: "msg-role" }, "the loremaster"),
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
        addChainLinks([...(result.upstream || []).slice().reverse(), ...(result.downstream || [])]);
        if (Array.isArray(result.enables)) turn.enables = result.enables;
      }
      break;
    case "neighbors":
      if (result) turn.neighbors.push(result);
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
    showError("Lost the connection to the loremaster.");
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

$("#examples").addEventListener("click", (e) => {
  const q = e.target.closest(".chip")?.dataset.q;
  if (q) { inputEl.value = q; autosize(); inputEl.focus(); }
});

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
