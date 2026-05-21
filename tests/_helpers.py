"""Shared test helpers.

The Weirwood scripts/ tree uses hyphenated filenames (e.g.
`stage4-haiku-run.py`) which can't be imported as regular Python modules.
`load_script` loads them by file path via importlib so tests can reach
their functions without renaming the scripts.
"""

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"


def load_script(filename: str):
    """Load a script from scripts/ by filename and return the module object.

    Example: `runner = load_script("stage4-haiku-run.py")` then
    `runner.plan_batch_chunks(...)`.
    """
    path = SCRIPTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Script not found: {path}")
    # Module name: filename with hyphens → underscores, .py stripped.
    mod_name = filename.replace("-", "_").replace(".py", "")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    # Add to sys.modules so any internal `import` of this name resolves.
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod
