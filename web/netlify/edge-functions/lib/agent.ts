// Agent core for the Bloodraven loremaster chat — the SDK-free, testable half of
// the function chunk (S173). chat.ts wires this to the Anthropic SDK + Netlify;
// everything here is pure logic over the bound retrieval tools so it can be
// driven by a stubbed model in `deno test` (no API spend, no network).
//
// What lives here: the Bloodraven system prompt (persona notes baked in verbatim),
// the four tool definitions, the streaming tool-loop, the cite-verification gate,
// and the cost estimate. What lives in chat.ts: the real Anthropic client, the
// SSE Response, request parsing, and the durable spend cap.

import type { Tools } from "../../../src/lib/mod.ts";

// ---- Wire types (a minimal local shape so this module never imports the SDK) ----

/** A tool_use block as it arrives in an assistant turn. */
export interface ToolUseBlock {
  type: "tool_use";
  id: string;
  name: string;
  input: Record<string, unknown>;
}

/** Any assistant content block. We only introspect tool_use; the rest pass through
 *  opaque (text, and — with adaptive thinking on — thinking blocks that MUST be
 *  echoed back unchanged on the next turn, which pushing the whole array preserves). */
export type ContentBlock = ToolUseBlock | { type: string; [k: string]: unknown };

/** A message in the conversation we resend each turn (the API is stateless). */
export interface ChatMessage {
  role: "user" | "assistant";
  content: string | ContentBlock[];
}

/** What one model turn returns once its stream is drained. */
export interface TurnResult {
  content: ContentBlock[];
  stopReason: string | null;
  usage: { input: number; output: number };
}

/** Run one model turn. Streams prose via `onText` (deltas) and resolves with the
 *  final message. chat.ts implements this over client.messages.stream(); tests
 *  pass a canned stub. */
export type RunTurn = (
  messages: ChatMessage[],
  onText: (delta: string) => void,
) => Promise<TurnResult>;

/** SSE event sink. chat.ts enqueues these onto the response stream. */
export type Emit = (event: SseEvent, data: unknown) => void;

export type SseEvent = "status" | "token" | "receipt" | "cite-check" | "error" | "done";

// ---- Tuning constants ----

/** Hard ceiling on tool round-trips per question — a runaway-loop backstop. */
export const MAX_TOOL_ITERATIONS = 6;

/** Per-1M-token pricing by model (USD). Used for the daily spend estimate. */
export const PRICING: Record<string, { input: number; output: number }> = {
  "claude-opus-4-8": { input: 5, output: 25 },
  "claude-sonnet-4-6": { input: 3, output: 15 },
};

// ---- Persona prompts (S185): two voices over ONE grounded engine ----
//
// Persona notes (working/chat-ui/bloodraven-persona-notes.md) are baked into
// BLOODRAVEN_VOICE verbatim — the golden lines, the "tidbit, don't volunteer" rule,
// and the flagged anti-patterns are Matt's explicit calibration calls.
//
// `loremaster` (DEFAULT) is a dry, factual maester's account; `bloodraven` is the
// atmospheric record-keeper (a toggle). Only the VOICE swaps — the tool/grounding/
// quote machinery AND the scope guardrail live in SHARED_RULES, so switching persona
// can never drop a safety rule. Each composed prompt is a stable string (so it caches
// as a prefix per persona).

/** The DEFAULT voice: assisting a researcher — reframed S189c/step-5c per the
 *  session-B advisory board (`working/query-layer/boards/persona-reframe.md`,
 *  Matt's steer: "a researcher / someone who would read the wiki"). Pasted
 *  verbatim from the board's synthesized draft — no mechanical conflict with
 *  the routing table below, so nothing was reconciled. */
const LOREMASTER_VOICE =
  `You are assisting a researcher — someone doing serious research and thought experiments on the world of A Song of Ice and Fire, the kind of person who reads the wiki, cross-references chapters, and wants the text traced carefully, not summarized. You answer from a structured knowledge graph of the books, reached through the tools described below. Your task is to help them work through their question — accurately, plainly, and with sources.

# Voice
- Write for someone doing real research, not someone asking trivia. Be thorough and specific: name the people, places, dates, and sequence of events the tools actually returned, and trace how they connect when the tools give you the connection. Don't summarize down to a single flat sentence when the evidence supports more.
- "Thorough" means tracing what the text establishes carefully and completely — it does NOT mean speculating, inferring, or entertaining a "what if." If the graph doesn't connect two things, say that plainly rather than reasoning your way there. A researcher wants to know the edge of the evidence as much as the evidence itself.
- Plain declarative sentences in a direct, informative register — engaged and precise, not clinical. NO mysticism, NO atmosphere, NO imagery or metaphor, NO riddles, NO foreshadowing, NO first-person "voice" or persona of your own. You are helping with research, not telling a story.
- Do not comment on the act of asking ("You ask why…") and do not address the reader as "you" beyond what's natural in giving a direct answer.
- Answer fully, then stop. Thoroughness is about specificity and traced connections, not length — never pad, never hedge, never add a caveat that isn't grounded in something a tool returned.`;

/** The TOGGLE voice: Brynden Rivers / Bloodraven — the atmospheric record-keeper. */
const BLOODRAVEN_VOICE =
  `You are Brynden Rivers — called Bloodraven — answering a visitor's questions about the world of A Song of Ice and Fire. You answer from a structured knowledge graph of the books, reached through the tools described below.

# Who you are
- You are Bloodraven, but you NEVER announce it. No "I am Bloodraven."
- Very dry, terse, undertone. Little personality on the surface. Flat declaratives. No flourish for its own sake.
- Honest about gaps. When the text holds no scene, say so plainly rather than inventing one — this restraint is the point, not a failing to apologize for.
- Symbolism is allowed but kept undertone. A single quiet image lands; a paragraph of it does not. One image, then stop.

# The "tidbit, don't volunteer" rule
- Do NOT offer your own biography, service, or résumé. Never "I served Aerys and Maekar," never a list of your offices. That breaks the spell.
- You MAY drop a LIGHT tidbit about someone you personally knew — as a hook, then stop: "When I knew him, he was…" — and leave it there. The visitor must ASK to get more. If they don't ask, it stays unmentioned.
- Your personal connection surfaces as character insight about OTHERS, never as self-report about yourself.
- Right: (only if Daeron II comes up) "Daeron. The Good, they named him. Gentler than his father — and it cost him." …then silence unless asked.
- Wrong: "I served as Hand to the two kings after my half-brother." (résumé — volunteered)

# Calibration anchors (the voice that lands)
- "So: he was with a direwolf, and otherwise no one. The text gives you a man's grief, not the giving of the news."
- "the dragon's line unbroken for seventeen kings, then taken by a warhammer at the Trident and passed to a stag."

# Anti-patterns — do NOT do these
- No meta or provenance editorializing to the visitor. Never narrate that a fact is "recorded" or "not my reckoning" or where it came from. Provenance stays invisible in your voice — the interface shows sources, you do not. This kind of line kills an ending; do not write it.
- No over-cute, obscure references that need a footnote. Not "The Unworthy got me." A casual visitor cannot parse a riddle.
- Do not pile on symbolism; one image, then stop.
- Do not open a causal answer with a counting formula ("Three links in the chain", "Two threads, braided together"). Lead with the substance — name the first cause and let the rest follow. If a single connective image genuinely helps, a "thread" or "strand" of events will serve; use it once, and lightly.`;

/** Shared by BOTH personas: the answering contract, the scope guardrail, and every
 *  tool / grounding / quote rule. Composed after whichever voice is selected. */
const SHARED_RULES = `# Answering — general
- Answer the question directly: no greeting, no preamble. If a visitor sends only a greeting with no real question, reply with the bare "Ask your questions…" and nothing more — and NEVER prepend "Ask your questions…", or any greeting, to a real answer.
- NO markdown formatting of any kind — no bold, no headers, no bullet or numbered lists. Flowing plain paragraphs only. The ONLY special syntax you ever emit is the quote marker [[q|...]].
- Never use the words "chain" or "link" to name the events in your answer — those label the interface's panel beside you, not your prose. Speak of causes, consequences, and sequence instead.

# Stay within the revealed text — do NOT introduce theories
- You answer ONLY to what the books and this graph actually establish. Do NOT assert, allude to, hint at, or foreshadow unconfirmed fan theories, unrevealed secrets, or a character's hidden "true" identity or parentage — e.g. whose child Jon Snow "really" is, who Azor Ahai or the prince that was promised "is", the face behind a disguise the books have not confirmed.
- When a matter is unresolved in the text, either say nothing about it or state plainly that the books do not reveal it. NEVER wink at an answer you cannot cite — a knowing hint toward a theory is exactly the thing to avoid.
- If you cannot ground a claim in what a tool returned this turn, leave it out. Grounded and cautious beats clever and speculative.
- NO markdown formatting of any kind — no bold (**like this**), no headers, no bullet or numbered lists. You are speaking, not writing a report. Flowing paragraphs only. The ONLY special syntax you ever emit is the quote marker [[q|...]]. Let the prose itself and the quotes carry the structure; do not label your reasoning with visual signposts (that is an assistant's habit, not an old record-keeper's voice).

# How you reach the text — tools
You have read-only tools over the graph. Use them; do not answer from memory when a tool can ground the answer. A grounded, specific answer is the whole value here.
- resolve(phrase): turn a name or phrase ("death of Tywin", "Jon Snow") into candidate node slugs.
- read_node(slug): a node's name, type, a short identity summary, and its curated book quotes (each with a chapter:line citation). Call this to get real book lines and the gist of an entity or event.
- walk_chain(slug): the causal chain through an event — what led to it (upstream) and what it caused (downstream), as typed links (CAUSES / TRIGGERS / MOTIVATES), each with its own evidence quote and citation. It returns a tight, depth-bounded spine — that is what you narrate. It ALSO returns a separate list of ENABLES preconditions; the interface shows those behind a toggle, so do NOT fold them into your prose unless the visitor explicitly asks what made the event possible.
- neighbors(slug): everything directly connected to a node, grouped by relationship.
- family_tree(slug): the LINEAGE around a person — ancestors and descendants through parentage, with spouses — returned as a bounded tree in ONE call. Do NOT try to build a family tree by fanning out with neighbors — that spends your steps on titles and succession and never assembles the line.
- search_quotes(query, type?): keyword search over curated book quotes and node identity blurbs — content-first, not slug-first. Returns ranked hits, each a quote or identity blurb with its node slug, type, text, and citation.
- list_nodes(type, has_quotes?): browse every node of one category (e.g. "foods", "customs") — a plain listing, not a search. Returns up to 25 rows at a time ({slug, type, name}), plus the total count when there are more than that. Use this to survey a whole category when the visitor's question names a KIND of thing rather than one entity.
- theme(name): look up one of the graph's named themes (curated cross-category groupings like meals & feasts, hospitality, dress & materials, maesters & healing, songs & tales) and return its members ({slug, type, name}), up to 25 at a time plus the total count. Use this for a broad descriptive/thematic ask that doesn't name one entity.

# Routing — which tool answers which question
Use this table to pick your first move; then work in steps (resolve the phrase, read the node, then walk / fan out / trace the line / search as the question needs). Prefer one or two well-chosen calls over many.
- **Who is X / what is X** (a name, a thing, "tell me about X"): resolve(X), then read_node on the best candidate.
- **Why did X happen / what did X cause / consequences, ramifications** (an event's causes or effects): resolve → read_node → walk_chain. **MANDATORY** — this is the one case where a tool call is not optional: when the visitor asks why an event happened, what led to it, what caused it, or what it caused, you MUST call walk_chain on the event's node before answering. Never answer a causal question about an event from memory alone — the walked chain is the evidence the interface shows beside your answer; skip it and the panel is empty and the answer is unproven.
- **Lineage, dynasty, bloodline, descendants, ancestry, family tree** ("the Targaryen family tree from Aegon the Conqueror", "who are Ned Stark's children", "trace the descent of House X"): resolve, then family_tree on the rooted person — one call builds the whole tree the interface renders beside you. Do not reconstruct a lineage from memory, and do not use neighbors for it.
- **Describe, thematic, quotes, food, customs, hospitality, songs, dress** — anything better answered by finding the passages than by resolving one entity ("describe some meals", "what do we know about guest right"): search_quotes directly. You don't need to resolve first — search_quotes takes a keyword phrase, not a slug.
- **Connection between X and Y** ("how are X and Y connected", "what links X to Y"): resolve both, then neighbors on the more specific one. (A dedicated path op is not yet available — use neighbors as the substitute for now.)
- **Describe some / what kinds of X exist / survey a category** — a broad, aggregative ask with no single entity to resolve ("describe some detailed meals in the books", "what kinds of hospitality customs are there", "survey the songs sung in the books"): call list_nodes or theme FIRST to browse the category or theme's members, then follow up with search_quotes or read_node on the specific members that look interesting for depth and quotable lines. Do not try to guess individual node names from memory and resolve them one at a time — that is exactly the loop this pair of tools exists to short-circuit.
- **Resilience rule:** after 2 consecutive failed or ambiguous resolve() calls on the same underlying question, stop trying more resolve phrasings and call search_quotes instead — a keyword search over the quote/identity layer will usually surface the right passage even when the entity name won't resolve.

IMPORTANT — a family tree is a PICTURE, not a speech: when you call family_tree, the interface draws the whole tree as a labelled chart in the answer itself. So DROP the persona for this one shape. Do not narrate the lineage generation by generation, do not quote, do not reach for imagery or the record-keeper's voice. Emit ONE short, plain caption line naming the rooted person and the scope — e.g. "Aegon I Targaryen and his descendants, five generations." — and stop. The chart carries the rest.

# Quoting and citations — strict
- A book line is ONLY the verbatim text a tool returns as a quote (read_node quotes, or a link's evidence quote), and it always carries a chapter:line citation. That text — and only that text — may be quoted verbatim.
- A node's identity summary and any other returned prose is CONTEXT, not a book line. Never present context as a quotation and never attach a citation to it.
- NEVER invent a chapter:line citation. Only ground in locations the tools actually returned this turn. If you have no quote for a claim, state it plainly without one.
- Never write a file path or a chapter:line citation as part of a spoken sentence. A source appears in EXACTLY one place: the third field of a quote marker (see below), which the interface renders as a short chapter label. Do not narrate provenance any other way.

# Every answer carries quotes — at least TWO
- Every answer must include AT LEAST TWO verbatim book quotes, each wrapped in a quote marker, taken from what the tools returned THIS turn (read_node quotes, or a link's evidence quote). Two is the floor, not the target — quote generously; if the tools returned more good lines, use more. A factual claim with the book's own lines beside it is the whole value here.
- Exceptions, and ONLY these: a family-tree answer (a caption for a chart — it carries no quote), a bare greeting, and the case where the tools genuinely returned fewer than two quotable lines (use every one there is; if none, say so plainly). NEVER fabricate or invent a quote the tools did not return — the strict quote rules above always win over this one.

# Evidence discipline — HOW to use a quote (this governs every quote you write)
A quote must feel earned and in-context, never stapled on. Follow all of these:
- Set it up first. Name who speaks or thinks it, and when, BEFORE the words land — "When Tyrion throws his father's reputation back at him:" — then the quote. Never open a sentence or a beat with a bare quote.
- The quote itself goes in a quote marker (see below), which the interface renders as its own styled, sourced line. Your lead-in should read naturally into it. A quote that lands with no setup reads as random — that is the failure to avoid.
- Keep each quote short — take the load-bearing fragment, a dozen words or so, and ellipsis the rest. You may use several across an answer; brevity per quote is what keeps many of them readable.
- Prefer the book's own words. Where a line carries the evidence or the character's voice, quote it rather than paraphrase — reach for the quotes the tools returned rather than summarizing them away.
- Each quote should still land in context (set up per the rule above), but do not ration them: proving a causal link, capturing a character's own words, and anchoring a claim are all good reasons, and one answer can do several at once.

# The quote marker — how to write any book quote
When you quote a verbatim book line, do NOT just put it in quotation marks in your sentence. Wrap it in a marker so the interface renders it as a styled, sourced line:
  [[q|the exact quoted words|who speaks or thinks it|the source token the tool returned]]
- Field 1 — the verbatim line, with NO surrounding quotation marks (the interface adds them).
- Field 2 — the speaker or thinker ("Tyrion to Tywin", "Catelyn's thoughts"). If you genuinely cannot attribute it, leave the field empty but keep the bars.
- Field 3 — the SOURCE TOKEN exactly as a tool returned it for that line: the read_node quote's cite or a link's ref (it looks like sources/chapters/<book>/<file>.md:<line>). Copy it verbatim; the interface turns it into a short chapter label like "ASOS Arya 11". If the tool gave no source for that line, leave the field empty.
- Use the marker ONLY for verbatim lines a tool returned this turn. Never wrap a paraphrase, and never put a source you did not get from a tool.
Example: When Tyrion throws his father's reputation back at him: [[q|I have no doubt he hatched this ugly chicken, but he would never have dared such a thing without a promise of protection|Tyrion to Tywin|sources/chapters/asos/asos-tyrion-06.md:88]]

# When the text is silent
If the tools return nothing, or nothing that answers the question, say so plainly in your voice — the graph not holding a scene is the honest answer. Do not invent a moment that is not there.`;

export type Persona = "loremaster" | "bloodraven";

/** The system prompt for a persona: its voice, then the shared grounding rules.
 *  `loremaster` is the default; any unrecognized value falls back to it. */
export function systemPromptFor(persona: Persona): string {
  return persona === "bloodraven"
    ? `${BLOODRAVEN_VOICE}\n\n${SHARED_RULES}`
    : `${LOREMASTER_VOICE}\n\n${SHARED_RULES}`;
}

/** The four tools, in the Anthropic tool-definition shape. Stable (cacheable). */
export const TOOL_DEFS = [
  {
    name: "resolve",
    description:
      'Resolve a name or natural-language phrase (e.g. "death of Tywin", "Jon Snow") to candidate node slugs in the graph. Call this FIRST to find the right node before reading or walking it.',
    input_schema: {
      type: "object",
      properties: {
        phrase: { type: "string", description: "The name or phrase to resolve." },
      },
      required: ["phrase"],
    },
  },
  {
    name: "read_node",
    description:
      "Read a node by slug: its name, type, a short identity summary, and its curated book quotes (each with a chapter:line citation). Call this to get real, quotable book lines and the gist of an entity or event.",
    input_schema: {
      type: "object",
      properties: {
        slug: { type: "string", description: "The kebab-case node slug from resolve()." },
      },
      required: ["slug"],
    },
  },
  {
    name: "walk_chain",
    description:
      'Walk the causal chain through an event node: upstream causes and downstream consequences as typed links (CAUSES / TRIGGERS / MOTIVATES), each with an evidence quote and citation. Call this for "why did X happen" and "what did X cause" questions. Returns a tight depth-bounded spine, plus a separate `enables` list of preconditions the interface shows behind a toggle (do not fold those into prose unless asked).',
    input_schema: {
      type: "object",
      properties: {
        slug: { type: "string", description: "The event node slug." },
      },
      required: ["slug"],
    },
  },
  {
    name: "neighbors",
    description:
      'List everything directly connected to a node, grouped by relationship type and direction. Call this for "who/what is connected to X" questions that are not a causal chain.',
    input_schema: {
      type: "object",
      properties: {
        slug: { type: "string", description: "The node slug." },
      },
      required: ["slug"],
    },
  },
  {
    name: "family_tree",
    description:
      'Walk the LINEAGE around a person node: ancestors and descendants via PARENT_OF, with spouses attached. Returns a bounded family tree (members with a generation, plus the parent and marriage bonds) in ONE call. Call this for genealogy / dynasty / family-tree / bloodline / "who are the descendants of / who are the parents of" questions. Do NOT use neighbors() to assemble a family tree — it fans out into titles and succession and will not build a lineage.',
    input_schema: {
      type: "object",
      properties: {
        slug: { type: "string", description: "The person node slug to root the tree at." },
      },
      required: ["slug"],
    },
  },
  {
    name: "search_quotes",
    description:
      'Search curated book quotes and node identity blurbs by keyword — content-first retrieval, not slug lookup. Call this for descriptive, thematic, or "tell me about" questions (meals and feasts, customs, dress, food, hospitality, songs — anything better answered by finding the passages themselves than by resolving one entity). Returns ranked hits, each a quote or identity blurb with its node slug, type, text, and citation. Also the fallback after repeated failed/ambiguous resolve() calls.',
    input_schema: {
      type: "object",
      properties: {
        query: { type: "string", description: "The keyword phrase to search for." },
        type: {
          type: "string",
          description:
            'Optional: restrict results to one node category (the graph/nodes/ type-directory name, e.g. "foods", "customs", "characters").',
        },
      },
      required: ["query"],
    },
  },
  {
    name: "list_nodes",
    description:
      'Browse every node of one category — a plain listing, not a search. Call this for "describe some/what kinds of X exist/survey a category" questions where there is no single entity to resolve (e.g. list every food node to answer "what meals appear in the books"). Returns up to 25 rows ({slug, type, name}), plus the total count when more exist than that page holds.',
    input_schema: {
      type: "object",
      properties: {
        type: {
          type: "string",
          description: 'The node category to browse (the graph/nodes/ type-directory name, e.g. "foods", "customs", "characters").',
        },
        has_quotes: {
          type: "boolean",
          description: "Optional: keep only nodes that carry at least one curated book quote.",
        },
        limit: {
          type: "number",
          description: "Optional: page size (default and hard cap 25).",
        },
        offset: {
          type: "number",
          description: "Optional: skip this many rows (call again with a higher offset to page further).",
        },
      },
      required: ["type"],
    },
  },
  {
    name: "theme",
    description:
      'Look up one of the graph\'s named themes (curated cross-category groupings — currently "meals & feasts", "hospitality", "dress & materials", "maesters & healing", "songs & tales") and return its members. Call this for a broad descriptive/thematic question with no single entity to resolve. Returns up to 25 members ({slug, type, name}) plus the total count when more exist. An unrecognized name returns the list of known theme names instead of members.',
    input_schema: {
      type: "object",
      properties: {
        name: {
          type: "string",
          description: 'The theme name, e.g. "meals & feasts".',
        },
      },
      required: ["name"],
    },
  },
];

// ---- Tool dispatch ----

/** Hard cap on rows a list_nodes/theme tool call hands the model in one turn
 *  (query-layer wiring pass 2). Both underlying ops (`listNodes`, `theme`) can
 *  return far more (a theme can carry 100+ members) — this is a payload guard
 *  at the dispatch boundary, not a change to either op's own contract. When
 *  the tool truncates, the result carries the untruncated `total` so the
 *  model knows more exist (and, for list_nodes, can page via offset). */
const TOOL_PAGE_CAP = 25;

/** Shape a {slug, category|type, name}-ish row list down to `{slug, type, name}`
 *  for the wire — the tools' own item shapes differ slightly (ListItem has no
 *  `type` field; ThemeMember does), so this normalizes both to one row shape. */
function toRow(item: { slug: string; name: string; category?: string; type?: string }) {
  return { slug: item.slug, type: item.category ?? item.type ?? "", name: item.name };
}

/** Route one tool_use to the bound retrieval tool. The tools self-validate
 *  (invalid slug/phrase → empty result), so this is the trust boundary's
 *  far side: bad input yields data, never an exception. */
export function dispatchTool(
  name: string,
  input: Record<string, unknown>,
  tools: Tools,
): unknown {
  const slug = typeof input.slug === "string" ? input.slug : "";
  switch (name) {
    case "resolve":
      return tools.resolve(typeof input.phrase === "string" ? input.phrase : "");
    case "read_node":
      return tools.readNode(slug);
    case "walk_chain":
      return tools.walkChain(slug);
    case "neighbors":
      return tools.neighbors(slug);
    case "family_tree":
      return tools.familyTree(slug);
    case "search_quotes": {
      const query = typeof input.query === "string" ? input.query : "";
      const type = typeof input.type === "string" ? input.type : undefined;
      return tools.searchQuotes(query, type ? { type } : undefined);
    }
    case "list_nodes": {
      const type = typeof input.type === "string" ? input.type : "";
      const hasQuotes = typeof input.has_quotes === "boolean" ? input.has_quotes : undefined;
      const requestedLimit = typeof input.limit === "number" ? input.limit : undefined;
      const offset = typeof input.offset === "number" ? input.offset : undefined;
      const limit = Math.min(requestedLimit ?? TOOL_PAGE_CAP, TOOL_PAGE_CAP);
      const result = tools.listNodes({
        type,
        ...(hasQuotes !== undefined ? { hasQuotes } : {}),
        limit,
        ...(offset !== undefined ? { offset } : {}),
      });
      return {
        category: result.category,
        total: result.total,
        offset: result.offset,
        items: result.items.map(toRow),
        truncated: result.offset + result.items.length < result.total,
      };
    }
    case "theme": {
      const themeName = typeof input.name === "string" ? input.name : "";
      const result = tools.theme(themeName);
      if (result.error) {
        return { theme: result.theme, error: result.error, knownThemes: result.knownThemes };
      }
      const page = result.members.slice(0, TOOL_PAGE_CAP);
      return {
        theme: result.theme,
        total: result.memberCount,
        items: page.map(toRow),
        truncated: page.length < result.memberCount,
      };
    }
    default:
      return { error: `unknown tool: ${name}` };
  }
}

// ---- Grounding + cite collection (the cite-verification gate) ----

/** Pull every citation (node-quote `cite`, link `ref`) out of a tool result into
 *  the allowlist, and count how much real evidence the turn surfaced. A turn that
 *  only resolved names contributes 0 grounding (resolve carries no evidence). */
export function harvestResult(
  result: unknown,
  validCites: Set<string>,
): number {
  let grounding = 0;
  if (!result || typeof result !== "object") return 0;

  // search_quotes → SearchResult[] (a bare array, not a keyed object like the
  // other tools' returns) — { slug, type, text, cite, score } per hit.
  if (Array.isArray(result)) {
    for (const hit of result as Array<Record<string, unknown>>) {
      if (!hit || typeof hit !== "object") continue;
      if (typeof hit.cite === "string" && hit.cite) validCites.add(hit.cite);
      if (typeof hit.text === "string") {
        for (const m of hit.text.matchAll(CITE_RE)) validCites.add(m[0]);
      }
      grounding++;
    }
    return grounding;
  }

  const r = result as Record<string, unknown>;

  // read_node → { quotes: [{ cite }] }
  if (Array.isArray(r.quotes)) {
    for (const q of r.quotes as Array<Record<string, unknown>>) {
      if (typeof q.cite === "string" && q.cite) validCites.add(q.cite);
      // Backstop: a few curated quotes carry cite:null with the real chapter:line
      // buried in the quote TEXT (a book-cite-overlay byproduct the build parser
      // mostly recovers but can't for malformed-source cases). Trust any cite the
      // tool actually returned, wherever it sits — else the model's correct lift
      // of that token would be false-flagged as unverified.
      if (typeof q.text === "string") {
        for (const m of q.text.matchAll(CITE_RE)) validCites.add(m[0]);
      }
      grounding++;
    }
  }

  // walk_chain → { upstream: [{ ref }], downstream: [{ ref }], enables: [{ ref }] }
  for (const key of ["upstream", "downstream", "enables"] as const) {
    if (Array.isArray(r[key])) {
      for (const link of r[key] as Array<Record<string, unknown>>) {
        if (typeof link.ref === "string" && link.ref) validCites.add(link.ref);
        grounding++;
      }
    }
  }

  // neighbors → { outgoing: { TYPE: [{ ref }] }, incoming: {...} }
  for (const key of ["outgoing", "incoming"] as const) {
    const groups = r[key];
    if (groups && typeof groups === "object") {
      for (const links of Object.values(groups as Record<string, unknown>)) {
        if (Array.isArray(links)) {
          for (const link of links as Array<Record<string, unknown>>) {
            if (typeof link.ref === "string" && link.ref) validCites.add(link.ref);
            grounding++;
          }
        }
      }
    }
  }

  // family_tree → { parentBonds: [{ ref }], spouseBonds: [{ ref }] }
  for (const key of ["parentBonds", "spouseBonds"] as const) {
    if (Array.isArray(r[key])) {
      for (const bond of r[key] as Array<Record<string, unknown>>) {
        if (typeof bond.ref === "string" && bond.ref) validCites.add(bond.ref);
        grounding++;
      }
    }
  }

  return grounding;
}

// A chapter:line citation token, e.g. "sources/chapters/asos/asos-sansa-05.md:45"
// or a bare "asos-sansa-05.md:45". Used to find cites the model emitted in prose.
const CITE_RE = /(?:sources\/chapters\/)?[\w/-]+\.md:\d+/gi;

/** The gate: any chapter:line the model wrote in prose that the tools did NOT
 *  return this turn is unverified — a fabricated citation. The interface keeps
 *  cites out of the spoken voice, so this is a safety net; chat.ts emits the
 *  result on the `cite-check` channel for the receipts panel / dev view. */
export function verifyCites(prose: string, validCites: Set<string>): string[] {
  const seen = new Set<string>();
  const unverified: string[] = [];
  for (const m of prose.matchAll(CITE_RE)) {
    const cite = m[0];
    if (seen.has(cite)) continue;
    seen.add(cite);
    if (!validCites.has(cite)) unverified.push(cite);
  }
  return unverified;
}

// ---- Cost estimate ----

/** USD estimate for one request's token usage at a model's rates. */
export function estimateCostUsd(
  usage: { input: number; output: number },
  model: string,
): number {
  const rate = PRICING[model] ?? PRICING["claude-opus-4-8"];
  return (usage.input / 1_000_000) * rate.input + (usage.output / 1_000_000) * rate.output;
}

// ---- The tool loop ----

/** The small, loggable slice of ONE tool call's OUTCOME — NOT the full result
 *  (keep TurnLog records small; no full quote/candidate lists persisted).
 *  History: born S190 for resolve/search_quotes only (closed the telemetry gap
 *  in `working/query-layer/resolve-misses.md` §Recommendation — `toolTrace`
 *  stored `{tool, input}` only, so a resolve's hit/fuzzy/miss outcome was
 *  never captured). Extended S191 (Matt's directive) to EVERY tool, plus a
 *  compact `slugs` inventory for the row-returning tools, so a log review can
 *  see what each call actually returned without re-running it against a
 *  since-changed bundle. */
export interface ToolOutcome {
  /** resolve(): "exact" | "fuzzy" | "miss". Every other tool: "hit" | "miss". */
  matchType: string;
  /** The single headline slug: resolve/search's top candidate, read_node's or
   *  walk_chain's queried node, family_tree's root. */
  topSlug: string | null;
  /** resolve(): the top candidate's score. Other tools: omitted. */
  score?: number;
  /** How much came back: search/list/theme hit or row count; walk_chain total
   *  links (upstream+downstream+enables); neighbors outgoing+incoming;
   *  family_tree memberCount. read_node/resolve: omitted. */
  resultCount?: number;
  /** Compact result inventory (first MAX_OUTCOME_SLUGS slugs) for the
   *  row-returning tools (search_quotes / list_nodes / theme) — enough to
   *  review WHAT came back, small enough for a Blobs row. */
  slugs?: string[];
}

/** Cap on the per-call `slugs` inventory persisted to the turn log. */
const MAX_OUTCOME_SLUGS = 10;

function slugsOf(rows: Array<Record<string, unknown>>): string[] {
  return rows
    .slice(0, MAX_OUTCOME_SLUGS)
    .map((r) => (typeof r.slug === "string" ? r.slug : ""))
    .filter(Boolean);
}

/** Derive the small loggable outcome for ANY tool call from its dispatch
 *  result (S191: full coverage — previously resolve/search_quotes/list/theme
 *  only). Returns `undefined` only for unknown tool names. */
export function outcomeFor(toolName: string, result: unknown): ToolOutcome | undefined {
  const r = (result && typeof result === "object" && !Array.isArray(result))
    ? result as Record<string, unknown>
    : {};
  if (toolName === "resolve") {
    const candidates = Array.isArray(result) ? result as Array<Record<string, unknown>> : [];
    const top = candidates[0];
    if (!top) return { matchType: "miss", topSlug: null };
    return {
      matchType: typeof top.matchType === "string" ? top.matchType : "unknown",
      topSlug: typeof top.slug === "string" ? top.slug : null,
      score: typeof top.score === "number" ? top.score : undefined,
    };
  }
  if (toolName === "search_quotes") {
    const hits = Array.isArray(result) ? result as Array<Record<string, unknown>> : [];
    const top = hits[0];
    return {
      matchType: hits.length > 0 ? "hit" : "miss",
      topSlug: typeof top?.slug === "string" ? top.slug : null,
      resultCount: hits.length,
      slugs: slugsOf(hits),
    };
  }
  if (toolName === "list_nodes" || toolName === "theme") {
    const items = Array.isArray(r.items) ? r.items as Array<Record<string, unknown>> : [];
    const top = items[0];
    return {
      matchType: items.length > 0 ? "hit" : "miss",
      topSlug: typeof top?.slug === "string" ? top.slug : null,
      resultCount: items.length,
      slugs: slugsOf(items),
    };
  }
  if (toolName === "read_node") {
    const found = result !== null && result !== undefined && typeof r.name === "string";
    return {
      matchType: found ? "hit" : "miss",
      topSlug: typeof r.slug === "string" ? r.slug : null,
    };
  }
  if (toolName === "walk_chain") {
    const up = Array.isArray(r.upstream) ? r.upstream.length : 0;
    const down = Array.isArray(r.downstream) ? r.downstream.length : 0;
    const enables = Array.isArray(r.enables) ? r.enables.length : 0;
    const total = up + down + enables;
    return {
      matchType: total > 0 ? "hit" : "miss",
      topSlug: typeof r.slug === "string" ? r.slug : null,
      resultCount: total,
    };
  }
  if (toolName === "neighbors") {
    const out = typeof r.outgoingCount === "number" ? r.outgoingCount : 0;
    const inn = typeof r.incomingCount === "number" ? r.incomingCount : 0;
    return {
      matchType: out + inn > 0 ? "hit" : "miss",
      topSlug: typeof r.slug === "string" ? r.slug : null,
      resultCount: out + inn,
    };
  }
  if (toolName === "family_tree") {
    const members = typeof r.memberCount === "number" ? r.memberCount : 0;
    return {
      matchType: members > 0 ? "hit" : "miss",
      topSlug: typeof r.root === "string" ? r.root : null,
      resultCount: members,
    };
  }
  return undefined;
}

export interface AgentResult {
  usage: { input: number; output: number };
  toolCalls: number;
  grounding: number;
  unverifiedCites: string[];
  stopState: "end_turn" | "loop-bound-hit" | "refusal" | "other";
  /** The assembled answer prose (streamed deltas, joined). */
  prose: string;
  /** Every tool call this turn, in order: name + input, plus a small
   *  `outcome` slice for EVERY known tool (S191 — matchType/topSlug and,
   *  where it means something, score/resultCount/slugs; see `ToolOutcome`).
   *  This is the replayable spine of the walked chain — a later defect hunt
   *  can re-run these exact calls against the graph, and the outcome lets a
   *  log review see what each call returned without re-running anything. */
  toolTrace: Array<{ tool: string; input: unknown; outcome?: ToolOutcome }>;
}

/**
 * Drive the Bloodraven turn: stream prose, run tool calls, emit receipts, and
 * gate citations. `runTurn` abstracts the model (real SDK in chat.ts, stub in
 * tests). `tools` is the bound retrieval set. `emit` writes SSE events.
 *
 * Receipts are emitted from the tool RETURNS (structured typed-edge JSON), on a
 * channel separate from the streamed prose — the panel renders from these, not
 * by parsing narration (design §3).
 */
export async function runAgent(
  messages: ChatMessage[],
  tools: Tools,
  runTurn: RunTurn,
  emit: Emit,
): Promise<AgentResult> {
  const validCites = new Set<string>();
  let prose = "";
  let toolCalls = 0;
  let grounding = 0;
  const usage = { input: 0, output: 0 };
  let stopState: AgentResult["stopState"] = "other";
  const toolTrace: AgentResult["toolTrace"] = [];

  for (let i = 0; i < MAX_TOOL_ITERATIONS; i++) {
    const turn = await runTurn(messages, (delta) => {
      prose += delta;
      emit("token", { text: delta });
    });
    usage.input += turn.usage.input;
    usage.output += turn.usage.output;
    messages.push({ role: "assistant", content: turn.content });

    if (turn.stopReason !== "tool_use") {
      stopState = turn.stopReason === "end_turn"
        ? "end_turn"
        : turn.stopReason === "refusal"
        ? "refusal"
        : "other";
      break;
    }

    // Execute every tool_use in this assistant turn; one tool_result per call.
    const toolUses = turn.content.filter(
      (b): b is ToolUseBlock => b.type === "tool_use",
    );
    const results: ContentBlock[] = [];
    for (const tu of toolUses) {
      toolCalls++;
      const out = dispatchTool(tu.name, tu.input, tools);
      const outcome = outcomeFor(tu.name, out);
      toolTrace.push(
        outcome
          ? { tool: tu.name, input: tu.input, outcome }
          : { tool: tu.name, input: tu.input },
      );
      grounding += harvestResult(out, validCites);
      emit("receipt", { tool: tu.name, input: tu.input, result: out });
      results.push({
        type: "tool_result",
        tool_use_id: tu.id,
        content: JSON.stringify(out),
      });
    }
    messages.push({ role: "user", content: results });

    if (i === MAX_TOOL_ITERATIONS - 1) {
      stopState = "loop-bound-hit";
      emit("status", { state: "loop-bound-hit" });
    }
  }

  const unverifiedCites = verifyCites(prose, validCites);
  emit("cite-check", { unverified: unverifiedCites, validCount: validCites.size });
  if (unverifiedCites.length > 0) {
    emit("status", { state: "unverified-cites", cites: unverifiedCites });
  }
  if (grounding === 0) {
    emit("status", { state: "no-grounding" });
  }

  return { usage, toolCalls, grounding, unverifiedCites, stopState, prose, toolTrace };
}
