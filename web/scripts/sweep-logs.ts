// web/scripts/sweep-logs.ts — 30-day retention sweep (S186). LOCAL only, NOT shipped.
//
// Date-prefixed keys (`log/YYYY-MM-DD/<uuid>`) make retention a trivial list+delete.
// Run occasionally by hand; nothing automated depends on it.
//
//   NETLIFY_SITE_ID=… NETLIFY_AUTH_TOKEN=… \
//     ~/.deno/bin/deno run -A --node-modules-dir=auto scripts/sweep-logs.ts [--apply] [DAYS]
//
// Dry-run by default (lists what WOULD be deleted). Pass --apply to delete.
// DAYS defaults to 30. Cutoff is compared lexically on the YYYY-MM-DD in the key.
import { getStore } from "npm:@netlify/blobs@8";

const siteID = Deno.env.get("NETLIFY_SITE_ID");
const token = Deno.env.get("NETLIFY_AUTH_TOKEN");
if (!siteID || !token) {
  console.error("Set NETLIFY_SITE_ID and NETLIFY_AUTH_TOKEN (personal access token).");
  Deno.exit(1);
}

const apply = Deno.args.includes("--apply");
const days = Number(Deno.args.find((a) => /^\d+$/.test(a)) ?? 30);

// Cutoff = today minus `days`, as a YYYY-MM-DD string for lexical comparison.
const cutoffMs = Date.now() - days * 86_400_000;
const cutoff = new Date(cutoffMs).toISOString().slice(0, 10);

const store = getStore({ name: "weirwood-chat", siteID, token });
const { blobs } = await store.list({ prefix: "log/" });

// key shape: log/YYYY-MM-DD/uuid → keep if its date >= cutoff.
const stale = blobs.filter((b) => {
  const date = b.key.split("/")[1] ?? "";
  return date && date < cutoff;
});

console.log(`cutoff=${cutoff} (${days}d)  total=${blobs.length}  stale=${stale.length}`);
for (const b of stale) {
  if (apply) {
    await store.delete(b.key);
    console.log(`deleted ${b.key}`);
  } else {
    console.log(`would delete ${b.key}`);
  }
}
if (!apply && stale.length) console.log("\nDry run. Re-run with --apply to delete.");
