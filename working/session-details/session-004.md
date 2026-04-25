# Session 4 — Playwright Migration for Wiki Scraper

**Date:** 2026-04-13

---

## What Triggered This Session

Session 3 ended with a successful 5-page smoke test of the wiki scraper and a runbook for the full 17,952-page crawl. The plan was simple: follow the runbook, kick off `--mode all`, let it run overnight. That plan lasted about thirty seconds.

## What Happened

The session opened by attempting the full crawl per runbook. It failed immediately. The `cf_clearance` cookie exported from the browser in Session 3 had already expired — Cloudflare rotates these aggressively. Grabbed a fresh cookie from the browser. That failed too.

This kicked off a diagnosis cycle. The cookie was valid (confirmed by pasting it into browser DevTools and seeing the wiki load), but every request from `urllib` got blocked. The working hypothesis shifted from "cookie expired" to something deeper: Cloudflare wasn't just checking cookies — it was fingerprinting the TLS connection itself. Python's `urllib` and `curl` both use OpenSSL, which has a different TLS handshake signature than a real browser's BoringSSL. No amount of cookie manipulation would fix this. The HTTP layer itself was the problem.

This meant the entire network stack in `wiki-scraper.py` needed to be replaced. The options were:

1. **TLS fingerprint spoofing** (libraries like `curl_cffi` or `tls-client`) — fragile, cat-and-mouse game with Cloudflare
2. **Browser automation** (Playwright, Selenium, Puppeteer) — heavy but fundamentally correct; uses an actual browser, so TLS fingerprinting is a non-issue

Playwright was the choice. It's the modern option, has good Python bindings, and handles browser lifecycle cleanly.

The migration was surgical. The scraper had clean separation between its network layer (fetch a URL, get HTML back) and its processing layer (parse HTML, classify entities, write markdown). Only the network layer needed replacing:

**Removed:** `ssl`, `urllib.request`, `urllib.error` imports; the `_build_ssl_context()` function that configured custom SSL settings; `load_cookies_from_file()` and its associated `COOKIES_FILE`, `_COOKIES`, `_SSL_CONTEXT` module-level variables; the `--cookies` CLI argument.

**Added:** Playwright browser lifecycle management (`_launch_browser`, `_close_browser`), a Cloudflare warmup routine (`_warmup_cloudflare`) that loads a page and polls for the Turnstile challenge to clear, and a `--headless` CLI flag that defaults to headed mode (important — headless browsers are more detectable by Cloudflare).

All parsing, classification, caching, and markdown-writing code was untouched. The `script-builder` subagent handled the actual code changes.

Then came the bug. After the migration, the scraper would pass the Cloudflare warmup (Turnstile cleared, `cf_clearance` cookie set in the browser context), but subsequent page navigations would get blocked again. The cookie was *in* the browser's cookie jar — you could see it in `context.cookies()` — but Chromium wasn't *sending* it on subsequent requests.

This turned out to be a known-ish Chromium/Playwright interaction issue. The `cf_clearance` cookie has `httpOnly` and `sameSite=None` attributes. Under certain conditions, Chromium stores these cookies in the context but doesn't attach them to outgoing request headers. The workaround: a Playwright route interceptor that manually reads the cookie from the context and injects it as a `Cookie` header on every outgoing request. Ugly but effective — it completely sidesteps whatever internal cookie-dispatch logic Chromium was failing at.

Smoke tests passed cleanly. `--entity "Tyrion Lannister"` fetched and processed successfully (1/1). `--mode all --limit 10` processed 10 pages with a 100% success rate, including 3 pages that had previously failed with the `urllib` approach. The runbook was updated to reflect the new workflow: no more cookie files, a browser window opens during the crawl, and one manual Turnstile click might be needed on the warmup page.

New dependency chain: `pip3 install playwright && playwright install chromium` (Chromium binary is ~91 MB, lives in `~/.cache/ms-playwright/`).

## Key Decisions and Why

**Playwright over TLS fingerprint spoofing.** TLS spoofing libraries try to make Python look like a browser at the network level. This is a cat-and-mouse game — Cloudflare updates their detection, the library has to update their fingerprints. Playwright uses an actual Chromium browser, so there's nothing to spoof. More overhead, but fundamentally correct.

**Headed mode as default.** Cloudflare can detect headless browsers through various signals (missing GPU renderer, specific JavaScript API differences). Running headed is less convenient (a browser window sits open during the crawl) but more reliable. The `--headless` flag exists for environments without a display, but the runbook recommends headed.

**Cookie file approach abandoned.** Session 3's approach of exporting cookies from a browser and feeding them to `urllib` was always a workaround. It required manual browser interaction every time, cookies expired within hours, and it didn't solve the TLS fingerprinting problem anyway. With Playwright managing its own browser session, cookies are handled natively and transparently.

**Route-based cookie injection.** This is a workaround for a Chromium bug, not a design choice. If Playwright/Chromium fixes the cookie dispatch behavior, the route interceptor could be removed. But it works, it's isolated, and it doesn't affect the rest of the scraper's logic.

## What Was Left Open

- The full 17,952-page crawl was still unexecuted — the entire session was consumed by the migration. Scheduled for next session.
- The 7 failed pages from smoke testing weren't investigated (likely redirect or special-character edge cases in the wiki URL structure).
- Whether Cloudflare would trigger additional challenges during a sustained multi-hour crawl was unknown. The warmup routine handles the initial challenge, but would the session stay valid for hours?
