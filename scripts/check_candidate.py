#!/usr/bin/env python3
"""Deprecated shim: use ``python -m gems.registry`` (or scripts/validate_submission.py).

Kept so older invocations keep working.  The screening rules are unchanged:
rank correlation above 0.90 or more than 70% of dots within 3 px of a registry
raster blocks the candidate, and an incomplete registry yields UNKNOWN rather
than a pass.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gems.registry import main  # noqa: E402

if __name__ == "__main__":
    print("note: scripts/check_candidate.py is superseded by gems/registry.py",
          file=sys.stderr)
    raise SystemExit(main())
