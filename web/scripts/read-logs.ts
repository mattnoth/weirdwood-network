// web/scripts/read-logs.ts — read back usage logs (S186). LOCAL only, NOT shipped.
//
// Each live turn writes a `log/YYYY-MM-DD/<uuid>` blob (see chat.ts logTurn).
// At portfolio scale (single-digit turns/day) just eyeball them.
//
//   NETLIFY_SITE_ID=… NETLIFY_AUTH_TOKEN=… \
//     ~/.deno/bin/deno run -A --node-modules-dir=auto scripts/read-logs.ts [YYYY-MM-DD]
//
// With no date arg, lists every `log/` blob. With a date, filters to that day.
// The token is a personal access token (app.netlify.com → User settings → Applications).
import { getStore } from "npm:@netlify/blobs@8";

const siteID = Deno.env.get("NETLIFY_SITE_ID");
const token = Deno.env.get("NETLIFY_AUTH_TOKEN");
if (!siteID || !token) {
  console.error("Set NETLIFY_SITE_ID and NETLIFY_AUTH_TOKEN (personal access token).");
  Deno.exit(1);
}

const day = Deno.args[0]; // optional YYYY-MM-DD
const prefix = day ? `log/${day}/` : "log/";
const store = getStore({ name: "weirwood-chat", siteID, token });

const { blobs } = await store.list({ prefix });
blobs.sort((a, b) => a.key.localeCompare(b.key));
console.log(`${blobs.length} turn(s) under ${prefix}\n`);

for (const { key } of blobs) {
  const raw = await store.get(key);
  if (!raw) continue;
  const r = JSON.parse(raw);
  const trace = Array.isArray(r.toolTrace)
    ? r.toolTrace.map((t: { tool: string }) => t.tool).join(" → ")
    : "";
  console.log(`── ${key}`);
  console.log(`   ${r.timestamp}  $${r.costUsd}  stop=${r.stopState}  grounding=${r.grounding}`);
  console.log(`   Q: ${r.question}`);
  console.log(`   chain: ${trace}`);
  if (Array.isArray(r.unverifiedCites) && r.unverifiedCites.length) {
    console.log(`   ⚠ unverified cites: ${r.unverifiedCites.join(", ")}`);
  }
  console.log(`   A: ${String(r.prose).slice(0, 280)}${String(r.prose).length > 280 ? "…" : ""}\n`);
}
