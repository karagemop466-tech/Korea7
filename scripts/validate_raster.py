#!/usr/bin/env python3
"""Conservative format preflight, not an organizer validator or promotion gate."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import rasterio


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def validate(candidate, reference):
    result = {'candidate': str(candidate), 'reference': str(reference),
              'format_preflight_passed': False, 'ready_to_submit': False,
              'note': 'Format preflight only; holdout, leakage and registry gates not assessed.'}
    try:
        result['sha256'] = sha256(candidate)
        with rasterio.open(reference) as ref, rasterio.open(candidate) as src:
            checks = {
                'geotiff': src.driver == 'GTiff',
                'single_band': src.count == 1,
                'float32': src.count == 1 and src.dtypes[0] == 'float32',
                'reference_has_crs': ref.crs is not None,
                'crs_match': src.crs is not None and src.crs == ref.crs,
                'shape_match': (src.height, src.width) == (ref.height, ref.width),
                'transform_match': tuple(src.transform) == tuple(ref.transform),
                # Deliberately stricter than a footprint-only check: the user has
                # encountered a range rejection and footprint rules are unverified.
                'all_pixels_finite': True,
                'all_pixels_in_range': True,
                'no_masked_pixels': True,
            }
            if src.count >= 1:
                for _, window in src.block_windows(1):
                    data = src.read(1, window=window, masked=False)
                    checks['all_pixels_finite'] &= bool(np.isfinite(data).all())
                    checks['all_pixels_in_range'] &= bool(((data >= 0) & (data <= 1)).all())
                    checks['no_masked_pixels'] &= bool((src.read_masks(1, window=window) != 0).all())
            else:
                checks['all_pixels_finite'] = checks['all_pixels_in_range'] = checks['no_masked_pixels'] = False
            result['checks'] = checks
            result['format_preflight_passed'] = all(checks.values())
    except (OSError, ValueError, TypeError, rasterio.errors.RasterioError) as exc:
        result['error'] = f'{type(exc).__name__}: {exc}'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', type=Path)
    parser.add_argument('reference', type=Path, help='official sample submission GeoTIFF')
    args = parser.parse_args()
    result = validate(args.candidate, args.reference)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result['format_preflight_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
