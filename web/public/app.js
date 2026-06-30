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
// "The chain walked" panel has TWO layouts, toggleable live (Matt S174): BAND
// (full-width horizontal flow) and SPINE (vertical, in the side panel). Both
// dedup shared nodes — each node appears once, joined by its typed edge.

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
  for (const c of [].concat(children)) {
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

// Normalize a typed-edge link from EITHER the live walk_chain/neighbors shape
// ({source, target, ref}) OR the featured-tywin.json shape ({source_name,
// target_name, evidence_ref}) into one render contract. Slug stays in
// source/target on both; the display name is *_name (featured) or prettified.
function normLink(l) {
  return {
    sourceSlug: l.source || "",
    targetSlug: l.target || "",
    source: l.source_name || pretty(l.source),
    target: l.target_name || pretty(l.target),
    edgeType: l.edge_type || l.type || "",
    quote: l.evidence_quote ?? l.quote ?? null,
    ref: l.evidence_ref ?? l.ref ?? null,
    tier: l.tier ?? null,
  };
}

/** Collapse a list of typed links into a deduped node/edge sequence: a shared
 *  node (target of one link == source of the next) is emitted ONCE. */
function buildSequence(rawLinks) {
  const items = [];
  let lastSlug = null;
  for (const raw of rawLinks) {
    const l = normLink(raw);
    if (l.sourceSlug !== lastSlug) {
      items.push({ type: "node", slug: l.sourceSlug, name: l.source });
    }
    items.push({ type: "edge", link: l });
    items.push({ type: "node", slug: l.targetSlug, name: l.target, terminal: true });
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
// cards render from it. Re-rendering on a layout toggle just re-reads the model.

let turn = freshTurn();
function freshTurn() {
  return { chainLinks: [], nodes: new Map(), resolves: [], neighbors: [], title: "" };
}

function addChainLinks(links, title) {
  turn.chainLinks.push(...links);
  if (title) turn.title = title;
}
function addNode(slug, rec) {
  if (slug && rec) turn.nodes.set(slug, rec);
}

// ---- Quote / evidence atoms ------------------------------------------------

function quoteList(quotes) {
  return el("div", { class: "quotes" }, (quotes || []).map((q) =>
    el("div", { class: "quote-row" }, [
      el("p", { class: "quote" }, `“${q.text}”`),
      (q.attribution || q.cite)
        ? el("span", { class: "attribution" }, q.attribution || q.cite)
        : false,
    ])
  ));
}

function edgeEvidence(l) {
  const body = [];
  if (l.quote) body.push(el("p", { class: "quote" }, `“${l.quote}”`));
  if (l.ref) body.push(el("span", { class: "cite" }, l.ref));
  if (l.tier != null) body.push(el("span", { class: "tier-badge" }, `Tier ${l.tier}`));
  return body.length
    ? el("div", { class: "link-evidence" }, body)
    : el("div", { class: "link-evidence" }, el("span", { class: "cite" }, "no evidence quote on this edge"));
}

function edgePill(edgeType) {
  return el("span", { class: `edge-label ${etClass(edgeType)}` }, edgeType || "RELATED");
}

// ---- Chain layouts ---------------------------------------------------------

const chainBandEl = $("#chain-band");
const receiptsEl = $("#receipts");
const stageEl = $(".stage");
let walking = false; // true while a live turn is gathering, before the chain lands

let layout = localStorage.getItem("weirwood-layout") || "band";

function layoutToggle() {
  const mk = (mode, label) =>
    el("button", {
      class: "lt-btn" + (layout === mode ? " active" : ""),
      type: "button",
      onclick: () => { layout = mode; localStorage.setItem("weirwood-layout", mode); renderReceipts(); },
    }, label);
  return el("div", { class: "layout-toggle", role: "group", "aria-label": "Chain layout" }, [
    mk("band", "Band"), mk("spine", "Spine"),
  ]);
}

function chainHeader() {
  return el("div", { class: "chain-header" }, [
    el("div", {}, [
      el("h2", { class: "chain-title" }, "The chain walked"),
      turn.title ? el("p", { class: "chain-sub" }, turn.title) : false,
    ]),
    layoutToggle(),
  ]);
}

// One detail panel (BAND only) — clicking a node/edge fills it.
let bandDetailEl = null;
function selectDetail(content) {
  if (!bandDetailEl) return;
  bandDetailEl.replaceChildren(content);
}

function renderBand(seq) {
  const flow = el("div", { class: "chain-flow band" });
  for (const it of seq) {
    if (it.type === "node") {
      const rec = turn.nodes.get(it.slug);
      const cls = "chain-node" + (it.terminal ? " terminal" : "") + (rec?.quotes?.length ? " has-quotes" : "");
      flow.append(el("button", {
        class: cls, type: "button",
        onclick: rec?.quotes?.length
          ? () => selectDetail(el("div", { class: "detail-body" }, [
              el("div", { class: "card-title" }, rec.name || it.name),
              rec.type ? el("div", { class: "card-type" }, rec.type) : false,
              quoteList(rec.quotes),
            ]))
          : () => selectDetail(el("p", { class: "detail-empty" }, `${it.name} — no curated quotes on this node.`)),
      }, it.name));
    } else {
      const l = it.link;
      flow.append(el("button", {
        class: `chain-edge ${etClass(l.edgeType)}`, type: "button",
        onclick: () => selectDetail(el("div", { class: "detail-body" }, [
          el("div", { class: "detail-edge" }, [l.source, " ", edgePill(l.edgeType), " ", l.target]),
          edgeEvidence(l),
        ])),
      }, [edgePill(l.edgeType), el("span", { class: "edge-arrow" }, "→")]));
    }
  }
  bandDetailEl = el("div", { class: "chain-detail" },
    el("p", { class: "detail-empty" }, "Click a node for its book quotes, or an edge for the evidence line."));
  chainBandEl.replaceChildren(chainHeader(), flow, bandDetailEl);
  chainBandEl.hidden = false;
}

function renderSpine(seq) {
  bandDetailEl = null;
  const flow = el("div", { class: "chain-flow spine" });
  for (const it of seq) {
    if (it.type === "node") {
      const rec = turn.nodes.get(it.slug);
      const cls = "spine-node" + (it.terminal ? " terminal" : "");
      if (rec?.quotes?.length) {
        flow.append(el("details", { class: cls }, [
          el("summary", {}, [el("span", { class: "node-name" }, it.name)]),
          el("div", { class: "spine-body" }, [
            rec.type ? el("div", { class: "card-type" }, rec.type) : false,
            quoteList(rec.quotes),
          ]),
        ]));
      } else {
        flow.append(el("div", { class: cls }, el("span", { class: "node-name" }, it.name)));
      }
    } else {
      const l = it.link;
      flow.append(el("details", { class: `spine-edge ${etClass(l.edgeType)}` }, [
        el("summary", {}, [edgePill(l.edgeType)]),
        edgeEvidence(l),
      ]));
    }
  }
  receiptsEl.append(el("div", { class: "card chain-card" }, [chainHeader(), flow]));
}

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
  const seq = buildSequence(turn.chainLinks);
  const hasChain = seq.length > 0;
  const supporting = [
    ...turn.resolves.map((r) => resolveCard(r.phrase, r.cands)),
    ...turn.neighbors.map((n) => neighborsCard(n)),
  ];

  chainBandEl.replaceChildren();
  chainBandEl.hidden = true;
  receiptsEl.replaceChildren();

  const band = layout === "band" && hasChain;
  stageEl.classList.toggle("mode-band", band);
  stageEl.classList.toggle("no-aside", band && supporting.length === 0);

  if (hasChain) {
    if (band) renderBand(seq);
    else renderSpine(seq);
  }

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
  return {
    append(t) { buf += t; bubble.textContent = buf; scrollIn(); },
    setText(t) { buf = t; bubble.textContent = buf; },
    bubbleEl: bubble,
    finish() { wrap.classList.remove("streaming"); return buf; },
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
      if (result) addChainLinks([...(result.upstream || []).slice().reverse(), ...(result.downstream || [])]);
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

// ---- Featured exchange (the design fixture; real chain + quotes) ------------
//
// DESIGN FIXTURE — NOT shipped-as-real content. featured-tywin.json carries the
// REAL graph chain, beats, and book quotes; the answer prose below is a layout
// PLACEHOLDER only. Before the public deploy, replace this with a CAPTURED REAL
// transcript (run the live function over the seed question, save its genuine
// model answer) per Matt's "no mocked AI responses" rule. Tracked in the worklog.
const FEATURED_PLACEHOLDER_ANSWER =
  "[ design placeholder — to be replaced by a captured real model answer before deploy ]\n\n" +
  "A girl took a stone from her hair, and a king choked on his wine. They named the dwarf for it. " +
  "He was tried, and a viper died screaming on his behalf, and a brother came in the dark to cut him loose — " +
  "and to give him, too late, the truth of a girl called Tysha. So the small man climbed a ladder to his father's " +
  "chamber, and the crossbow spoke twice.";

async function loadFeatured() {
  let data;
  try {
    const res = await fetch("/data/featured-tywin.json");
    if (!res.ok) throw new Error(String(res.status));
    data = await res.json();
  } catch {
    renderReceipts();
    return;
  }
  renderFeatured(data);
}

function renderFeatured(data) {
  addUserBubble(data.question || "Who killed Tywin Lannister, and why?");

  const bot = addBotBubble();
  bot.setText(FEATURED_PLACEHOLDER_ANSWER);
  if (data.closing?.text) {
    bot.bubbleEl.append(el("blockquote", {}, `“${data.closing.text}”`));
  }
  bot.finish();

  turn = freshTurn();
  if (Array.isArray(data.chain)) addChainLinks(data.chain, data.title || "");
  for (const beat of data.beats || []) {
    if (beat.slug) addNode(beat.slug, { name: beat.name, type: beat.type, quotes: beat.quotes || [] });
  }
  renderReceipts();
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

const aboutToggle = $("#about-toggle");
aboutToggle.addEventListener("click", () => {
  const details = $(".intro-more");
  const open = !details.open;
  details.open = open;
  aboutToggle.setAttribute("aria-expanded", String(open));
  if (open) details.scrollIntoView({ behavior: "smooth", block: "nearest" });
});

loadFeatured();
