"""GEMS fault-prospectivity toolkit.

Modules
-------
metric    Distance-weighted Tversky index (DTI), reference and fast paths.
grid      The verified competition grid (EPSG:32611, 3730x3292, 100 m).
network   Synthetic fault-network generator, calibrated to published agreement.
emission  DTI-optimal emission: Dinkelbach thresholding + greedy coverage.
holdout   Buffered, segment-blocked spatial holdout + leakage canary.
estimate  Score estimation with confidence intervals, clearly provenance-tagged.
validate  Submission format validator (single-band GeoTIFF / zip).
registry  Registry-based uniqueness screening (rank correlation, dot overlap).
writer    GeoTIFF writer that can only emit validator-clean rasters.
"""

__all__ = ["metric", "grid", "network", "emission", "holdout", "estimate",
           "validate", "registry", "writer"]
__version__ = "1.0.0"
