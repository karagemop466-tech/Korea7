"""Korea7 — GEMS Prize Challenge submission research package.

Modules
-------
metric    Vendored official DTI metric (verified against a literal transcription).
grid      Competition-grid I/O and format gates.
registry  The nine focus-site rasters: forensics, overlap and lane uniqueness.
external  Acquisition and warping of official free external layers.
screen    Single-feature screening (leakage canary) and spatial-blocked holdout.
emit      Marginal-credit emission from a continuous surface to dots.
"""

__all__ = ["metric", "grid", "registry", "external", "screen", "emit"]
