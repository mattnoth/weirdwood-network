#!/usr/bin/env python3
"""Scrape A Wiki of Ice and Fire (AWOIAF) using the MediaWiki API.

Produces structured markdown files in sources/wiki/ organized by entity type.
Raw API responses are cached in sources/wiki/_raw/ to avoid redundant requests.

Modes:
  --entity NAME          Scrape a single entity page
  --category NAME        Scrape all members of a wiki category
  --mode targeted        Scrape a predefined batch (--batch required)
  --mode categories      Crawl the category tree and produce discovery reports
  --mode all             Full crawl: scrape every page in the wiki (namespace 0)

Options:
  --limit N              (--mode all only) Stop after N pages — useful for smoke tests

Usage examples:
  python scripts/wiki-scraper.py --entity "Tyrion Lannister"
  python scripts/wiki-scraper.py --category "Characters from the North"
  python scripts/wiki-scraper.py --mode targeted --batch characters
  python scripts/wiki-scraper.py --mode categories
  python scripts/wiki-scraper.py --mode all
  python scripts/wiki-scraper.py --mode all --limit 10
  python scripts/wiki-scraper.py --entity "Tyrion Lannister" -v
  python scripts/wiki-scraper.py --entity "Tyrion Lannister" --no-cache

Full-crawl notes (--mode all):
  The wiki has ~10 000+ pages. At 1 request/sec the crawl takes several hours.
  Progress is appended to sources/wiki/_raw/.crawl-progress.log line-by-line so
  you can monitor it with: tail -f sources/wiki/_raw/.crawl-progress.log
  The page-title list is cached to sources/wiki/_raw/.all-pages.json; pass
  --no-cache to force a fresh enumeration.
  If Cloudflare blocks 3 consecutive requests the crawl exits with a clear
  message instructing you to re-run. Already-cached pages are never re-fetched,
  so re-running resumes where it left off.

Browser automation notes:
  Uses Playwright (Chromium) for requests, bypassing Cloudflare TLS fingerprinting.

  Setup:
    pip install playwright
    playwright install chromium

  Runs in headed mode by default (visible browser window). Pass --headless
  to run without a window (less reliable against Cloudflare).
"""

import argparse
import datetime
import html
import html.parser
import json
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ---------------------------------------------------------------------------
# Project paths (resolved relative to this script's location)
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
WIKI_DIR = PROJECT_ROOT / "sources" / "wiki"

RAW_DIR = WIKI_DIR / "_raw"
UNCATEGORIZED_DIR = WIKI_DIR / "_uncategorized"
CATEGORY_REPORTS_DIR = WIKI_DIR / "_category-reports"

ENTITY_DIRS = {
    "characters": WIKI_DIR / "characters",
    "locations": WIKI_DIR / "locations",
    "houses": WIKI_DIR / "houses",
    "events": WIKI_DIR / "events",
    "artifacts": WIKI_DIR / "artifacts",
}

# ---------------------------------------------------------------------------
# API constants
# ---------------------------------------------------------------------------
API_BASE = "https://awoiaf.westeros.org/api.php"
INDEX_BASE = "https://awoiaf.westeros.org/index.php"
RATE_LIMIT_SEC = 1.0  # minimum seconds between API requests

# User-Agent that is unlikely to be flagged — identify as a bot politely
USER_AGENT = (
    "WeirwoodNetwork/1.0 (ASOIAF knowledge graph project; "
    "uses MediaWiki API; https://github.com/weirwood-network)"
)

# ---------------------------------------------------------------------------
# Pre-defined entity batches for --mode targeted
# ---------------------------------------------------------------------------
BATCHES = {
    "characters": [
        "Jon Snow", "Daenerys Targaryen", "Tyrion Lannister",
        "Cersei Lannister", "Jaime Lannister", "Arya Stark",
        "Sansa Stark", "Bran Stark", "Eddard Stark", "Catelyn Stark",
        "Theon Greyjoy", "Davos Seaworth", "Samwell Tarly",
        "Brienne of Tarth", "Melisandre", "Barristan Selmy",
        "Victarion Greyjoy", "Arianne Martell", "Asha Greyjoy",
        "Areo Hotah", "Aeron Greyjoy", "Jon Connington",
        "Quentyn Martell", "Petyr Baelish", "Varys",
        "Tywin Lannister", "Stannis Baratheon", "Renly Baratheon",
        "Robb Stark", "Joffrey Baratheon", "Tommen Baratheon",
        "Robert I Baratheon", "Margaery Tyrell", "Olenna Tyrell",
        "Oberyn Martell", "Doran Martell", "Mance Rayder",
        "Jeor Mormont", "Jorah Mormont", "Sandor Clegane",
        "Gregor Clegane", "Roose Bolton", "Ramsay Bolton",
        "Walder Frey", "Euron Greyjoy", "Hodor",
        "Brynden Rivers", "Illyrio Mopatis",
    ],
    "locations": [
        "Winterfell", "King's Landing", "The Wall", "Castle Black",
        "Dragonstone", "The Eyrie", "Riverrun", "Casterly Rock",
        "Highgarden", "Sunspear", "Pyke", "The Twins", "Harrenhal",
        "Oldtown", "Braavos", "Pentos", "Meereen", "Astapor",
        "Yunkai", "Vaes Dothrak", "Asshai", "Valyria",
        "Tower of Joy", "The Citadel", "Dreadfort", "Moat Cailin",
        "Storm's End", "Horn Hill", "Greywater Watch",
        "Iron Throne",
    ],
    "houses": [
        "House Stark", "House Lannister", "House Baratheon",
        "House Targaryen", "House Greyjoy", "House Tyrell",
        "House Martell", "House Arryn", "House Tully",
        "House Bolton", "House Frey", "House Mormont",
        "House Clegane", "House Reed", "House Dayne",
        "House Hightower", "House Velaryon", "House Blackfyre",
        "House Manderly", "House Umber",
    ],
    "events": [
        "Robert's Rebellion", "Red Wedding",
        "Battle of the Blackwater", "Purple Wedding",
        "Doom of Valyria", "Dance of the Dragons",
        "War of the Five Kings", "Battle of Castle Black",
        "Sack of King's Landing", "Tower of Joy",
        "Greyjoy Rebellion", "Battle of the Trident",
        "Defiance of Duskendale", "Kingsmoot", "Field of Fire",
    ],
    "artifacts": [
        "Ice (Stark)", "Longclaw", "Dawn (sword)", "Lightbringer",
        "Valyrian steel", "Dragon eggs", "Iron Throne",
        "Dragonbinder", "Horn of Joramun", "Dark Sister",
        "Blackfyre (sword)", "Oathkeeper", "Widow's Wail",
        "Glass candle", "Catspaw assassin's blade",
    ],
}

# ---------------------------------------------------------------------------
# Category → entity type mapping
# Used to classify pages into output directories.
# Order matters — more specific categories should come first.
# ---------------------------------------------------------------------------
CATEGORY_TYPE_MAP = [
    # Characters: various "Characters from X" categories plus general
    (re.compile(r"^Characters", re.I), "characters"),
    (re.compile(r"\bPeople\b", re.I), "characters"),
    (re.compile(r"POV characters", re.I), "characters"),
    # Houses / factions (before locations so "Houses of the North" beats "North")
    (re.compile(r"^Noble houses", re.I), "houses"),
    (re.compile(r"^Houses\b", re.I), "houses"),
    (re.compile(r"\borganizations\b", re.I), "houses"),
    # Locations
    (re.compile(r"^(Castles|Cities|Regions|Settlements|Locations|Towns|Villages|Holdfasts|Keeps|Islands|Mountains|Rivers|Seas|Bays|Forests|Ruins|Towers)\b", re.I), "locations"),
    (re.compile(r"\b(castle|city|region|location|settlement|town|village)\b", re.I), "locations"),
    # Events
    (re.compile(r"^(Battles|Wars|Tournaments|Events|Rebellions|Sieges|Campaigns)\b", re.I), "events"),
    (re.compile(r"\b(battle|war|tournament|rebellion|siege)\b", re.I), "events"),
    # Artifacts
    (re.compile(r"^(Valyrian steel swords|Items|Weapons|Ships|Objects|Artifacts)\b", re.I), "artifacts"),
    (re.compile(r"^(Swords|Books and scrolls)\b", re.I), "artifacts"),
    (re.compile(r"\b(sword|weapon|artifact|scroll)\b", re.I), "artifacts"),
]

# ---------------------------------------------------------------------------
# Browser lifecycle management (Playwright)
# ---------------------------------------------------------------------------

_playwright = None
_browser = None
_browser_page = None


def _launch_browser(headless=False):
    """Launch a Playwright Chromium browser and create a page."""
    global _playwright, _browser, _browser_page
    _playwright = sync_playwright().start()
    _browser = _playwright.chromium.launch(headless=headless)
    context = _browser.new_context(
        user_agent=USER_AGENT,
        viewport={"width": 1280, "height": 800},
    )
    _browser_page = context.new_page()


def _close_browser():
    """Close the Playwright browser and stop the Playwright instance."""
    global _playwright, _browser, _browser_page
    if _browser:
        _browser.close()
        _browser = None
    if _playwright:
        _playwright.stop()
        _playwright = None
    _browser_page = None


def _warmup_cloudflare(verbose=False):
    """Navigate to wiki homepage to clear any initial Cloudflare challenge.

    After the challenge is resolved (or if none appeared), installs a route
    handler that injects the cf_clearance cookie into every outgoing request.
    Chromium sometimes fails to send this cookie on subsequent navigations
    despite it being present in the cookie jar — the route handler works around
    this.
    """
    if verbose:
        print("Warming up browser (Cloudflare check)...")
    _browser_page.goto("https://awoiaf.westeros.org/", timeout=60000, wait_until="domcontentloaded")
    _browser_page.wait_for_timeout(3000)
    content = _browser_page.content()
    if "Just a moment" in content:
        if verbose:
            print("  Cloudflare challenge detected — waiting for resolution...")
            print("  If you see a 'Verify you are human' button in the browser, please click it.")
        # Poll for up to 120 seconds
        for _ in range(120):
            _browser_page.wait_for_timeout(1000)
            if "Just a moment" not in _browser_page.content():
                if verbose:
                    print("  Cloudflare challenge passed.")
                break
        else:
            raise RuntimeError("Cloudflare challenge did not resolve within 120 seconds")
    elif verbose:
        print("  Browser ready — no challenge.")

    # Extract cf_clearance and install a route handler to inject it on every
    # request.  Chromium/Playwright sometimes drops httpOnly + sameSite=None
    # cookies on cross-navigation requests; this ensures they are always sent.
    context = _browser_page.context
    cookies = context.cookies()
    cf = [c for c in cookies if c["name"] == "cf_clearance"]
    if cf:
        cf_value = cf[0]["value"]
        if verbose:
            print(f"  Installing cf_clearance cookie injector.")

        def _inject_cookie(route):
            headers = {**route.request.headers}
            existing = headers.get("cookie", "")
            if "cf_clearance" not in existing:
                sep = "; " if existing else ""
                headers["cookie"] = f"{existing}{sep}cf_clearance={cf_value}"
            route.continue_(headers=headers)

        _browser_page.route("**/*", _inject_cookie)
    elif verbose:
        print("  WARNING: No cf_clearance cookie found after warmup.")


def _is_cloudflare_challenge(content):
    """Return True if the response body is a Cloudflare JS challenge page."""
    if isinstance(content, str):
        content = content.encode("utf-8", errors="replace")
    return b"cf-mitigated" in content or b"cf_chl_opt" in content or b"Just a moment" in content


# ---------------------------------------------------------------------------
# HTML parsing utilities (no third-party packages)
# ---------------------------------------------------------------------------

class _TextExtractor(html.parser.HTMLParser):
    """Extract clean text from MediaWiki HTML, preserving paragraph breaks."""

    # Tags whose content should be skipped entirely
    SKIP_TAGS = {"script", "style", "sup", "table", "tr", "td", "th", "caption"}
    # Tags that produce a paragraph break
    BLOCK_TAGS = {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
                  "li", "br", "blockquote", "pre"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._parts = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
        if tag in self.BLOCK_TAGS and not self._skip_depth:
            self._parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
        if tag in self.BLOCK_TAGS and not self._skip_depth:
            self._parts.append("\n")

    def handle_data(self, data):
        if not self._skip_depth:
            self._parts.append(data)

    def get_text(self):
        raw = "".join(self._parts)
        # Remove citation markers like [1], [2], [note 1]
        raw = re.sub(r"\[\d+\]", "", raw)
        raw = re.sub(r"\[note\s+\d+\]", "", raw, flags=re.I)
        # Collapse multiple blank lines to at most one
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip()


def html_to_text(html_str):
    """Strip HTML and return cleaned plain text."""
    parser = _TextExtractor()
    parser.feed(html_str)
    return parser.get_text()


class _InfoboxParser(html.parser.HTMLParser):
    """Extract key-value pairs from a MediaWiki infobox table."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.data = {}
        self._in_infobox = False
        self._key = None
        self._collecting_key = False
        self._collecting_val = False
        self._key_buf = []
        self._val_buf = []
        self._depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get("class", "")
        elem_id = attrs_dict.get("id", "")

        # Detect infobox by class or id
        if tag == "table" and ("infobox" in cls or "infobox" in elem_id):
            self._in_infobox = True
            self._depth = 0

        if not self._in_infobox:
            return

        if tag == "table":
            self._depth += 1

        if tag == "th":
            self._collecting_key = True
            self._key_buf = []

        if tag == "td":
            self._collecting_val = True
            self._val_buf = []

        if tag in {"sup", "br"} and self._collecting_val:
            self._val_buf.append(" ")

    def handle_endtag(self, tag):
        if not self._in_infobox:
            return

        if tag == "th":
            self._collecting_key = False
            self._key = " ".join("".join(self._key_buf).split())

        if tag == "td":
            self._collecting_val = False
            if self._key:
                val = " ".join("".join(self._val_buf).split())
                val = re.sub(r"\[\d+\]", "", val).strip()
                if val:
                    self.data[self._key] = val
            self._key = None

        if tag == "table":
            if self._depth <= 0:
                self._in_infobox = False
            else:
                self._depth -= 1

    def handle_data(self, data):
        if not self._in_infobox:
            return
        if self._collecting_key:
            self._key_buf.append(data)
        elif self._collecting_val:
            self._val_buf.append(data)


def extract_infobox(html_str):
    """Return dict of infobox key→value pairs from parsed HTML."""
    parser = _InfoboxParser()
    parser.feed(html_str)
    return parser.data


def extract_first_paragraph(html_str):
    """Return the first substantial paragraph of text from parsed HTML."""
    para_pattern = re.compile(r"<p[^>]*>(.*?)</p>", re.DOTALL | re.I)
    for match in para_pattern.finditer(html_str):
        text = html_to_text(match.group(1)).strip()
        if len(text) > 60:
            text = re.sub(r"\[\d+\]", "", text).strip()
            return text
    return ""


def extract_section_headings(html_str):
    """Return list of section heading texts (h2/h3 only, cleaned)."""
    heading_pattern = re.compile(
        r"<h[23][^>]*>.*?<span[^>]*class=\"[^\"]*mw-headline[^\"]*\"[^>]*>(.*?)</span>",
        re.DOTALL | re.I,
    )
    headings = []
    for match in heading_pattern.finditer(html_str):
        text = html_to_text(match.group(1)).strip()
        if text:
            headings.append(text)
    return headings


def extract_categories(html_str):
    """Return list of category names from the page's category links."""
    catlinks_match = re.search(
        r'id="mw-normal-catlinks"[^>]*>(.*?)</div>', html_str, re.DOTALL | re.I
    )
    if not catlinks_match:
        return []

    cats_html = catlinks_match.group(1)
    link_pattern = re.compile(r'href="[^"]*Category:[^"]*"[^>]*>(.*?)</a>', re.DOTALL | re.I)
    categories = []
    for m in link_pattern.finditer(cats_html):
        cat = html_to_text(m.group(1)).strip()
        if cat and cat.lower() != "categories":
            categories.append(cat)
    return categories


# ---------------------------------------------------------------------------
# API interaction
# ---------------------------------------------------------------------------

_last_request_time = 0.0


def _throttle():
    """Sleep if needed to enforce the rate limit."""
    global _last_request_time
    elapsed = time.monotonic() - _last_request_time
    if elapsed < RATE_LIMIT_SEC:
        time.sleep(RATE_LIMIT_SEC - elapsed)
    _last_request_time = time.monotonic()


def api_get(params, verbose=False):
    """Execute a MediaWiki API call and return the parsed JSON response.

    Returns None on any network or parse error, or if a Cloudflare challenge
    is detected (in which case a clear diagnostic message is printed).
    """
    params["format"] = "json"
    query_str = urllib.parse.urlencode(params)
    url = f"{API_BASE}?{query_str}"

    if verbose:
        print(f"    GET {url}")

    _throttle()

    try:
        response = _browser_page.goto(url, timeout=30000, wait_until="domcontentloaded")
    except PlaywrightTimeout:
        print(f"  WARNING: Timeout for {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  WARNING: Navigation error for {url}: {e}", file=sys.stderr)
        return None

    if response is None or response.status >= 400:
        status = response.status if response else "no response"
        body_html = _browser_page.content()
        if _is_cloudflare_challenge(body_html.encode("utf-8", errors="replace")):
            _print_cloudflare_error()
        else:
            print(f"  WARNING: HTTP {status} for {url}", file=sys.stderr)
        return None

    try:
        body = _browser_page.inner_text("body")
        return json.loads(body)
    except json.JSONDecodeError as e:
        print(f"  WARNING: JSON decode error for {url}: {e}", file=sys.stderr)
        return None


def _print_cloudflare_error():
    """Print a clear diagnostic when Cloudflare blocks access."""
    print(
        "\n"
        "ERROR: Cloudflare challenge detected that the browser could not solve.\n"
        "\n"
        "If running with --headless, try without it so you can see the browser.\n"
        "If a 'Verify you are human' button appears, click it manually.\n"
        "The crawl will resume automatically once the challenge is passed.\n",
        file=sys.stderr,
    )


def page_name_to_cache_key(page_name):
    """Convert a wiki page name to a safe filesystem key."""
    safe = re.sub(r'[<>:"/\\|?*]', "_", page_name)
    safe = safe.replace(" ", "_")
    return safe


def fetch_page_html(page_name, use_cache=True, verbose=False):
    """Fetch and return the parsed HTML for a wiki page.

    Uses cache unless use_cache=False. Returns (html_str, from_cache) or
    (None, False) if the page cannot be retrieved.
    """
    cache_key = page_name_to_cache_key(page_name)
    cache_path = RAW_DIR / f"{cache_key}.json"

    if use_cache and cache_path.exists():
        if verbose:
            print(f"    [cache hit] {page_name}")
        with open(cache_path, "r", encoding="utf-8") as f:
            cached = json.load(f)
        return cached.get("html"), True

    if verbose:
        print(f"    [fetching] {page_name}")

    data = api_get({"action": "parse", "page": page_name, "prop": "text|categories"}, verbose)

    if data is None:
        return None, False

    if "error" in data:
        err = data["error"]
        print(f"  WARNING: API error for page '{page_name}': {err.get('info', err)}", file=sys.stderr)
        return None, False

    parse = data.get("parse", {})
    html_str = parse.get("text", {}).get("*", "")

    if not html_str:
        print(f"  WARNING: Empty HTML returned for page '{page_name}'", file=sys.stderr)
        return None, False

    # Cache the raw response
    cache_payload = {
        "page": page_name,
        "html": html_str,
        "fetched": datetime.date.today().isoformat(),
    }
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache_payload, f, ensure_ascii=False, indent=2)

    return html_str, False


def fetch_category_members(category_name, use_cache=True, verbose=False):
    """Return list of page titles that are members of the given category.

    Handles API continuation to retrieve more than 500 members.
    """
    cache_key = f"CAT_{page_name_to_cache_key(category_name)}"
    cache_path = RAW_DIR / f"{cache_key}.json"

    if use_cache and cache_path.exists():
        if verbose:
            print(f"    [cache hit] Category:{category_name}")
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f).get("members", [])

    members = []
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category_name}",
        "cmlimit": "500",
        "cmtype": "page",
    }

    while True:
        data = api_get(params, verbose)
        if data is None:
            break
        if "error" in data:
            print(
                f"  WARNING: API error for Category:{category_name}: "
                f"{data['error'].get('info', data['error'])}",
                file=sys.stderr,
            )
            break

        batch = data.get("query", {}).get("categorymembers", [])
        members.extend(m["title"] for m in batch)

        if "continue" not in data:
            break
        params.update(data["continue"])

    # Cache results
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "category": category_name,
                "members": members,
                "fetched": datetime.date.today().isoformat(),
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    if verbose:
        print(f"    Found {len(members)} members in Category:{category_name}")

    return members


def fetch_top_level_categories(use_cache=True, verbose=False):
    """Return all categories that have at least one page member."""
    cache_key = "ALL_CATEGORIES"
    cache_path = RAW_DIR / f"{cache_key}.json"

    if use_cache and cache_path.exists():
        if verbose:
            print("    [cache hit] all categories list")
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f).get("categories", [])

    categories = []
    params = {
        "action": "query",
        "list": "allcategories",
        "aclimit": "500",
        "acminsize": "1",
    }

    while True:
        data = api_get(params, verbose)
        if data is None:
            break
        if "error" in data:
            print(
                f"  WARNING: API error fetching categories: "
                f"{data['error'].get('info', data['error'])}",
                file=sys.stderr,
            )
            break

        batch = data.get("query", {}).get("allcategories", [])
        categories.extend(c["*"] for c in batch)

        if "continue" not in data:
            break
        params.update(data["continue"])

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(
            {"categories": categories, "fetched": datetime.date.today().isoformat()},
            f,
            ensure_ascii=False,
            indent=2,
        )

    return categories


# Namespace prefixes to filter out defensively (apnamespace=0 should already
# exclude these, but belt-and-suspenders).
_NAMESPACE_PREFIXES = (
    "Category:", "File:", "Template:", "User:", "Talk:",
    "MediaWiki:", "Help:", "Wikipedia:",
)


def fetch_all_page_titles(use_cache=True, verbose=False):
    """Return a list of all page title strings in the wiki (namespace 0).

    Uses the MediaWiki allpages API with pagination.  Results are cached to
    RAW_DIR / ".all-pages.json" as {"titles": [...], "fetched": "<date>"}.
    Pass use_cache=False to force a fresh enumeration.
    """
    cache_path = RAW_DIR / ".all-pages.json"

    if use_cache and cache_path.exists():
        if verbose:
            print("    [cache hit] full page list (.all-pages.json)")
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f).get("titles", [])

    if verbose:
        print("    Fetching full page list from API (apnamespace=0) ...")

    titles = []
    params = {
        "action": "query",
        "list": "allpages",
        "apnamespace": "0",
        "aplimit": "500",
    }

    while True:
        data = api_get(params, verbose)
        if data is None:
            break
        if "error" in data:
            print(
                f"  WARNING: API error fetching allpages: "
                f"{data['error'].get('info', data['error'])}",
                file=sys.stderr,
            )
            break

        batch = data.get("query", {}).get("allpages", [])
        titles.extend(p["title"] for p in batch)

        if "continue" not in data:
            break
        params.update(data["continue"])

    # Belt-and-suspenders: remove any non-article titles that slipped through
    titles = [t for t in titles if not any(t.startswith(pfx) for pfx in _NAMESPACE_PREFIXES)]

    # Cache the result
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(
            {"titles": titles, "fetched": datetime.date.today().isoformat()},
            f,
            ensure_ascii=False,
            indent=2,
        )

    if verbose:
        print(f"    Fetched {len(titles)} page titles")

    return titles


# ---------------------------------------------------------------------------
# Entity type classification
# ---------------------------------------------------------------------------

def classify_entity(page_name, categories):
    """Return the entity type string based on page name and wiki categories.

    Returns one of: "characters", "locations", "houses", "events",
    "artifacts", or None (→ _uncategorized).
    """
    # Name-based heuristics (fast path, no network required)
    if page_name.startswith("House "):
        return "houses"

    # Category-based classification — first match in CATEGORY_TYPE_MAP wins
    for cat in categories:
        for pattern, entity_type in CATEGORY_TYPE_MAP:
            if pattern.search(cat):
                return entity_type

    return None  # uncategorized


# ---------------------------------------------------------------------------
# Frontmatter / output generation
# ---------------------------------------------------------------------------
TODAY = datetime.date.today().isoformat()


def page_name_to_slug(name):
    """Convert a wiki page name to a kebab-case filename slug."""
    slug = name.lower()
    # Replace parenthetical disambiguation: "Ice (Stark)" → "ice-stark"
    slug = re.sub(r"\s*\(([^)]+)\)", r"-\1", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    return slug.strip("-")


def wiki_url(page_name):
    """Return the canonical AWOIAF URL for a page."""
    safe = urllib.parse.quote(page_name.replace(" ", "_"), safe="/:@!$&'()*+,;=")
    return f"{INDEX_BASE}/{safe}"


def infobox_to_aliases(infobox):
    """Extract aliases / also-known-as values from infobox data."""
    alias_keys = {"alias", "aliases", "also known as", "also called", "epithet", "epithets"}
    aliases = []
    for k, v in infobox.items():
        if k.lower() in alias_keys:
            for part in re.split(r"[,\n]+", v):
                part = part.strip()
                if part:
                    aliases.append(part)
    return aliases


def build_frontmatter(page_name, entity_type, categories, infobox, proposed=False):
    """Return a YAML frontmatter string for the entity."""
    url = wiki_url(page_name)
    aliases = infobox_to_aliases(infobox)

    lines = ["---"]
    lines.append(f"name: {page_name}")

    if proposed:
        proposed_type = entity_type or "unknown"
        lines.append(f"proposed_type: {proposed_type}")
    else:
        lines.append(f"type: {entity_type}")

    lines.append(f"wiki_url: {url}")

    if aliases:
        alias_items = []
        for a in aliases:
            # Quote values that contain commas to avoid YAML ambiguity
            alias_items.append(f'"{a}"' if "," in a else a)
        lines.append(f"aliases: [{', '.join(alias_items)}]")

    # first_available is required by architecture but must be filled by an extraction agent
    lines.append("first_available: ''  # to be filled by extraction agent")
    lines.append(f"scraped_date: {TODAY}")

    if proposed:
        if categories:
            cat_str = ", ".join(categories)
            lines.append(f"wiki_categories: [{cat_str}]")
        lines.append('note: "Does not fit current node types. Candidate for review."')

    lines.append("---")
    return "\n".join(lines)


def build_infobox_section(infobox):
    """Return a markdown section with infobox data, or empty string."""
    if not infobox:
        return ""
    lines = ["## Infobox Data", ""]
    for k, v in infobox.items():
        lines.append(f"**{k}:** {v}  ")
    lines.append("")
    return "\n".join(lines)


def build_section_headings_section(headings):
    """Return a markdown section listing article headings."""
    if not headings:
        return ""
    lines = ["## Article Sections", ""]
    for h in headings:
        lines.append(f"- {h}")
    lines.append("")
    return "\n".join(lines)


def build_categories_section(categories):
    """Return a markdown section listing wiki categories."""
    if not categories:
        return ""
    lines = ["## Wiki Categories", ""]
    for c in categories:
        lines.append(f"- {c}")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Core scrape-and-save logic
# ---------------------------------------------------------------------------

def scrape_entity(page_name, use_cache=True, verbose=False, dry_run=False):
    """Scrape a single wiki page and write its output file.

    Returns a dict with keys: page_name, entity_type, output_path, skipped, error.
    """
    result = {
        "page_name": page_name,
        "entity_type": None,
        "output_path": None,
        "skipped": False,
        "error": None,
    }

    if verbose:
        print(f"  Scraping: {page_name}")

    html_str, from_cache = fetch_page_html(page_name, use_cache=use_cache, verbose=verbose)

    if html_str is None:
        result["error"] = "Page not found or fetch failed"
        print(f"  WARNING: Could not fetch '{page_name}' — skipping", file=sys.stderr)
        return result

    # --- Extract structured data ---
    infobox = extract_infobox(html_str)
    first_para = extract_first_paragraph(html_str)
    headings = extract_section_headings(html_str)
    categories = extract_categories(html_str)

    if verbose:
        print(f"    Infobox keys: {list(infobox.keys())}")
        print(f"    Categories: {categories}")
        print(f"    Headings: {headings}")

    # --- Classify entity ---
    entity_type = classify_entity(page_name, categories)

    if verbose:
        print(f"    Classified as: {entity_type or '_uncategorized'}")

    # --- Determine output directory and path ---
    if entity_type in ENTITY_DIRS:
        out_dir = ENTITY_DIRS[entity_type]
    else:
        out_dir = UNCATEGORIZED_DIR

    slug = page_name_to_slug(page_name)
    out_path = out_dir / f"{slug}.md"

    result["entity_type"] = entity_type or "_uncategorized"
    result["output_path"] = str(out_path)

    if dry_run:
        print(f"    [dry-run] Would write to {out_path}")
        return result

    # --- Build output content ---
    proposed = entity_type is None
    frontmatter = build_frontmatter(page_name, entity_type, categories, infobox, proposed=proposed)

    body_parts = [frontmatter, ""]

    if first_para:
        body_parts.append("## Summary")
        body_parts.append("")
        body_parts.append(first_para)
        body_parts.append("")

    if infobox:
        body_parts.append(build_infobox_section(infobox))

    if headings:
        body_parts.append(build_section_headings_section(headings))

    # Full cleaned article text
    full_text = html_to_text(html_str).strip()
    if full_text:
        body_parts.append("## Full Text")
        body_parts.append("")
        body_parts.append(full_text)
        body_parts.append("")

    if categories:
        body_parts.append(build_categories_section(categories))

    content = "\n".join(body_parts)

    # --- Write file ---
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    if verbose:
        print(f"    Written: {out_path}")

    return result


def scrape_category(category_name, use_cache=True, verbose=False):
    """Scrape all member pages of a wiki category.

    Returns list of result dicts from scrape_entity().
    """
    print(f"Fetching members of Category:{category_name} ...")
    members = fetch_category_members(category_name, use_cache=use_cache, verbose=verbose)
    print(f"  Found {len(members)} members")

    results = []
    for i, page_name in enumerate(members, 1):
        if verbose:
            print(f"  [{i}/{len(members)}]", end=" ")
        r = scrape_entity(page_name, use_cache=use_cache, verbose=verbose)
        results.append(r)

    return results


# ---------------------------------------------------------------------------
# Category discovery mode
# ---------------------------------------------------------------------------

DISCOVERY_CATEGORIES = [
    # Characters
    "Characters",
    "POV characters",
    "Major characters",
    "Characters from the North",
    "Characters from the Westerlands",
    "Characters from the Stormlands",
    "Characters from the Reach",
    "Characters from Dorne",
    "Characters from the Iron Islands",
    "Characters from the Vale",
    "Characters from the Riverlands",
    "Characters from King's Landing",
    "Characters from Essos",
    # Locations
    "Castles",
    "Cities",
    "Regions",
    "Locations",
    "Settlements",
    "Rivers",
    "Mountains",
    "Islands",
    # Houses
    "Noble houses",
    "Houses of the North",
    "Houses of the Westerlands",
    "Houses of the Stormlands",
    "Houses of the Reach",
    "Houses of Dorne",
    "Houses of the Iron Islands",
    "Houses of the Vale",
    "Houses of the Riverlands",
    # Events
    "Battles",
    "Wars",
    "Tournaments",
    "Events",
    # Artifacts / items
    "Valyrian steel swords",
    "Items",
    "Books (in-universe)",
    # Other
    "Magic",
    "Religions",
    "Organizations",
]


def run_category_discovery(use_cache=True, verbose=False):
    """Crawl curated categories, produce report files in _category-reports/."""
    CATEGORY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Running category discovery ({len(DISCOVERY_CATEGORIES)} categories) ...")

    summary_rows = []

    for cat_name in DISCOVERY_CATEGORIES:
        print(f"\n  Category: {cat_name}")
        members = fetch_category_members(cat_name, use_cache=use_cache, verbose=verbose)

        if not members:
            print("    (empty or not found — skipping)")
            continue

        print(f"    {len(members)} members")

        # Classify each member by name only (no page fetch needed for discovery)
        rows = []
        type_counts = {}

        for page_name in members:
            proposed = classify_entity(page_name, [cat_name])
            label = proposed or "_uncategorized"
            type_counts[label] = type_counts.get(label, 0) + 1
            url = wiki_url(page_name)
            rows.append((page_name, url, label))

        # Write report markdown
        report_slug = page_name_to_slug(cat_name)
        report_path = CATEGORY_REPORTS_DIR / f"{report_slug}.md"

        report_lines = [
            f"# Category: {cat_name}",
            f"Scraped: {TODAY}",
            "",
            f"## Members ({len(members)} pages)",
            "",
            "| Entity | Wiki URL | Proposed Type |",
            "|---|---|---|",
        ]
        for page_name, url, label in rows:
            report_lines.append(f"| {page_name} | {url} | {label} |")

        report_lines += [
            "",
            "## Type Distribution",
            "",
        ]
        for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            report_lines.append(f"- **{t}:** {count}")

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
            f.write("\n")

        print(f"    Report written: {report_path}")
        summary_rows.append((cat_name, len(members), type_counts))

    # Write master summary
    summary_path = CATEGORY_REPORTS_DIR / "_summary.md"
    summary_lines = [
        "# Category Discovery Summary",
        f"Scraped: {TODAY}",
        "",
        "| Category | Members | Top Type |",
        "|---|---|---|",
    ]
    for cat_name, count, type_counts in summary_rows:
        top = max(type_counts, key=type_counts.get) if type_counts else "n/a"
        summary_lines.append(f"| {cat_name} | {count} | {top} |")

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))
        f.write("\n")

    print(f"\nSummary written: {summary_path}")
    return summary_rows


# ---------------------------------------------------------------------------
# Summary printing
# ---------------------------------------------------------------------------

def print_results_summary(results, label=""):
    """Print a summary table of scrape results."""
    if label:
        print(f"\n{'=' * 60}")
        print(f"Results: {label}")

    success = [r for r in results if r["output_path"] and not r["error"]]
    failed = [r for r in results if r["error"]]
    skipped = [r for r in results if r["skipped"]]

    type_counts = {}
    for r in success:
        t = r["entity_type"] or "_uncategorized"
        type_counts[t] = type_counts.get(t, 0) + 1

    print(f"\nTotal pages processed: {len(results)}")
    print(f"  Successful:  {len(success)}")
    print(f"  Failed:      {len(failed)}")
    print(f"  Skipped:     {len(skipped)}")

    if type_counts:
        print("\nBy entity type:")
        for t, count in sorted(type_counts.items()):
            dir_path = ENTITY_DIRS.get(t, UNCATEGORIZED_DIR)
            print(f"  {t:<20} {count:>4}  ->  {dir_path}")

    if failed:
        print(f"\nFailed pages ({len(failed)}):")
        for r in failed:
            print(f"  {r['page_name']}: {r['error']}")

    print("")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Scrape A Wiki of Ice and Fire using the MediaWiki API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # What to scrape
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--entity",
        metavar="PAGE_NAME",
        help="Scrape a single wiki page by its exact page name",
    )
    group.add_argument(
        "--category",
        metavar="CATEGORY_NAME",
        help="Scrape all members of a wiki category",
    )
    group.add_argument(
        "--mode",
        choices=["targeted", "categories", "all"],
        help="'targeted' scrapes a batch; 'categories' runs discovery; 'all' crawls every page",
    )

    # Targeted mode options
    parser.add_argument(
        "--batch",
        choices=list(BATCHES.keys()),
        help="Batch name for --mode targeted (characters, locations, houses, events, artifacts)",
    )

    # Full-crawl options
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="(--mode all only) Stop after scraping N pages — useful for smoke tests",
    )

    # Browser options
    parser.add_argument(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode (default: headed, more reliable against Cloudflare)",
    )

    # Behavior flags
    parser.add_argument(
        "--no-cache",
        action="store_true",
        default=False,
        help="Ignore cached API responses and re-fetch everything",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Print detailed progress information",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Show what would be written without actually writing files",
    )

    args = parser.parse_args()

    use_cache = not args.no_cache

    # Ensure output directories exist
    for d in [RAW_DIR, UNCATEGORIZED_DIR, CATEGORY_REPORTS_DIR] + list(ENTITY_DIRS.values()):
        d.mkdir(parents=True, exist_ok=True)

    _launch_browser(headless=args.headless)
    _warmup_cloudflare(verbose=args.verbose)
    try:
        # --- Dispatch ---
        if args.entity:
            print(f"Scraping entity: {args.entity}")
            result = scrape_entity(
                args.entity,
                use_cache=use_cache,
                verbose=args.verbose,
                dry_run=args.dry_run,
            )
            print_results_summary([result], label=args.entity)

        elif args.category:
            results = scrape_category(args.category, use_cache=use_cache, verbose=args.verbose)
            print_results_summary(results, label=f"Category:{args.category}")

        elif args.mode == "targeted":
            if not args.batch:
                parser.error(
                    "--mode targeted requires --batch "
                    "(characters, locations, houses, events, artifacts)"
                )

            entities = BATCHES[args.batch]
            print(f"Targeted scrape: batch '{args.batch}' ({len(entities)} entities)")
            results = []
            for i, page_name in enumerate(entities, 1):
                print(f"  [{i}/{len(entities)}] {page_name}")
                r = scrape_entity(
                    page_name,
                    use_cache=use_cache,
                    verbose=args.verbose,
                    dry_run=args.dry_run,
                )
                results.append(r)

            print_results_summary(results, label=f"batch:{args.batch}")

        elif args.mode == "categories":
            summary = run_category_discovery(use_cache=use_cache, verbose=args.verbose)
            print(f"\nCategory discovery complete. {len(summary)} categories processed.")
            print(f"Reports written to: {CATEGORY_REPORTS_DIR}")

        elif args.mode == "all":
            print("Fetching full page list...")
            titles = fetch_all_page_titles(use_cache=use_cache, verbose=args.verbose)

            if args.limit is not None:
                titles = titles[: args.limit]
                print(f"Limited to {args.limit} pages (smoke test)")

            print(f"Total pages to scrape: {len(titles)}")

            progress_log = RAW_DIR / ".crawl-progress.log"
            RAW_DIR.mkdir(parents=True, exist_ok=True)

            results = []
            consecutive_failures = 0

            for i, page_name in enumerate(titles, 1):
                print(f"  [{i}/{len(titles)}] {page_name}")
                r = scrape_entity(
                    page_name,
                    use_cache=use_cache,
                    verbose=args.verbose,
                    dry_run=args.dry_run,
                )
                results.append(r)

                # Append a progress line so `tail -f .crawl-progress.log` works
                status = "ok" if not r["error"] else f"error:{r['error']}"
                ts = datetime.datetime.now().isoformat(timespec="seconds")
                with open(progress_log, "a", encoding="utf-8") as pf:
                    pf.write(f"{ts}\t{i}/{len(titles)}\t{page_name}\t{status}\n")

                # Track consecutive failures for Cloudflare detection
                if r["error"]:
                    consecutive_failures += 1
                else:
                    consecutive_failures = 0

                if consecutive_failures >= 3:
                    print(
                        "\nERROR: 3 consecutive page failures detected.\n"
                        "\n"
                        "Possible causes:\n"
                        "  - Cloudflare is requiring interactive verification\n"
                        "  - Network connectivity issues\n"
                        "  - The wiki is down or rate-limiting\n"
                        "\n"
                        "To resume:\n"
                        "  Re-run the same command — cached pages are skipped.\n"
                        "  If running with --headless, try without it.\n",
                        file=sys.stderr,
                    )
                    print_results_summary(results, label="all pages (aborted — Cloudflare)")
                    sys.exit(1)

            print_results_summary(results, label="all pages")

        else:
            parser.print_help()
            sys.exit(1)
    finally:
        _close_browser()


if __name__ == "__main__":
    main()
