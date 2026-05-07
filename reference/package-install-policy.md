# Package Selection and Global-Install Policy

**Audience:** Every code-writing agent in the fleet (`script-builder`, `frontend-developer`, `backend-developer`, `deployment-engineer`, `embedding-refresh-runner`, etc.) must respect this policy.

**Purpose:** The cost of a malicious or unreliable dependency is high (supply-chain compromise, system pollution, hard-to-undo state changes). The cost of asking before installing is low. This policy makes the asymmetry the default.

For the broader design framing this policy sits inside, see `reference/design-philosophy.md`.

---

## Rules

**1. No global installs without explicit user approval.**
Never run any of: `npm install -g`, `yarn global add`, `pip install --user`, `pip install --break-system-packages`, `pipx install` outside a documented project tool, `brew install`, `gem install` system-wide, `cargo install` to system path, or any equivalent that modifies the host's global package state. If a global tool is genuinely needed, file a question to `working/wiki-pass2/questions-for-matt.jsonl` of type `package-global-install-request` with: tool name, why needed, the exact command proposed, what alternatives were considered. User approves explicitly before the command runs.

**2. Project-local installs only.**
- Python: always inside a virtual environment (`python3 -m venv venv`, then `source venv/bin/activate`). Pin in `requirements.txt` or `pyproject.toml`.
- Node: project-local `node_modules`, pinned in `package.json` + `package-lock.json` / `pnpm-lock.yaml` / `bun.lockb`. Never `-g`.
- Rust: project-local `Cargo.toml`. No system-wide cargo install.

**3. Reliable packages only.**
Before adding ANY dependency, the agent confirms ALL of:

- High download volume (npm: >100k weekly downloads; PyPI: comparable established tier)
- Recent maintenance (last commit within ~12 months)
- Recognizable maintainer (named individual, established org, foundation — not "random GitHub account with 0 followers")
- Package name matches its homepage / repo (no typosquat suspicion — `requests` not `requestz`, `numpy` not `nump`, etc.)
- For each package category, prefer the canonical recommended choice rather than a flashy newcomer:
  - **LLM SDK:** `anthropic` (official) — and ONLY `anthropic` for Claude calls
  - **Vector DB:** `chromadb`, `lancedb`, or `sqlite-vec` (these have been vetted by the Anthropic ecosystem)
  - **Embedding:** Voyage AI's official SDK, OpenAI's official SDK, or local `sentence-transformers`/`nomic-embed`
  - **HTTP / API:** `requests` (Python), `httpx` (Python async), `fetch` (Node native — no axios/got/etc. unless specifically justified)
  - **Markdown rendering:** `marked` (Node) or `markdown-it`, `python-markdown` or `mistune` (Python). Mature and audited.
  - **CSS scoping:** scoped class names or CSS Modules. No new CSS-in-JS framework unless the consuming project is already using one.

**4. Always state the package + alternatives.**
When proposing a new dependency, the agent's commit message / PR description / output report includes:
- Package name + version + source (npm / PyPI / GitHub releases)
- Homepage URL
- Why this package over the alternatives it considered (one-line each)
- Whether this is a hard requirement or "nice-to-have"

User can override with a different package without penalty.

**5. Settings updates require user-visible diffs.**
When an agent proposes changes to `.claude/settings.json` or `.claude/settings.local.json` (using the `update-config` skill or otherwise):
- Show the proposed diff to the user first
- Don't add `*` permission grants (too broad)
- Don't disable security-sensitive defaults
- Hooks that auto-execute commands need EXTRA scrutiny — describe what the hook does, when it fires, what it can read/write
- Default to least-privilege; ask before broadening

**6. Codify the policy in `.claude/settings.json` deny-rules.**
The project's settings file should explicitly deny global-install bash commands at the harness level. Belt-and-suspenders alongside the prompt-level rule. Suggested deny patterns:
- `npm install -g *`
- `yarn global *`
- `pip install --user *`
- `pip install --break-system-packages *`
- `brew install *`
- `gem install *`
- `cargo install *`

When these are denied by the harness, an agent attempting them gets a permission prompt — Matt approves manually if the install is genuinely needed.

---

## Why this policy

- **Supply-chain attacks are real.** Typosquats, dependency confusion, and post-install scripts have shipped malware in npm, PyPI, and other registries. An agent moving fast on a feature is exactly the wrong context for casual `npm install random-package`.
- **Global installs are hard to undo.** Project-local installs delete with the project directory. Global installs leave artifacts that survive. If something turns out to be malicious, project-local containment limits the blast radius.
- **Settings drift compounds.** A permissive settings.json over time accumulates broad permissions that the user can't easily audit. Diff-before-apply keeps the project's threat model legible.

---

## When this policy bites (and that's the point)

If an agent proposes installing `chromadb` (recognized, reliable) the policy passes silently — nothing to ask Matt about, install proceeds in the venv. If an agent proposes installing `chrome-vector-db-fast` (looks like chromadb but isn't) the policy catches it: agent has to justify, alternatives considered, Matt approves explicitly. The friction is the feature.
