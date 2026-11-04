#!/usr/bin/env python3
"""Conservative format preflight; it does not establish novelty or predictive skill."""
import argparse
import hashlib
import json
import sys

import numpy as np
import rasterio


def validate(candidate, reference):
    result = {'candidate': str(candidate), 'reference': str(reference), 'format_pass': False,
              'ready_to_submit': False, 'errors': [], 'checks': {}}
    errors, checks = result['errors'], result['checks']
    try:
        digest = hashlib.sha256()
        with open(candidate, 'rb') as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b''):
                digest.update(chunk)
        result['sha256'] = digest.hexdigest()
        with rasterio.open(reference) as ref, rasterio.open(candidate) as src:
            checks['reference_geotiff'] = ref.driver == 'GTiff'
            checks['reference_single_band'] = ref.count == 1
            checks['geotiff'] = src.driver == 'GTiff'
            checks['single_band'] = src.count == 1
            checks['float32'] = src.count == 1 and src.dtypes[0] == 'float32'
            checks['crs_match'] = ref.crs is not None and src.crs == ref.crs
            checks['shape_match'] = (src.height, src.width) == (ref.height, ref.width)
            checks['transform_match'] = tuple(src.transform) == tuple(ref.transform)
            # Deliberately stricter than a footprint-only test: no NaN, nodata,
            # infinity or out-of-range value anywhere, including outside footprint.
            finite = in_range = unmasked = True
            for _, window in src.block_windows(1):
                values = src.read(1, window=window, masked=False)
                finite &= bool(np.isfinite(values).all())
                in_range &= bool(((values >= 0) & (values <= 1)).all())
                unmasked &= bool((src.read_masks(1, window=window) != 0).all())
            checks['all_pixels_finite'] = finite
            checks['all_pixels_in_range'] = in_range
            checks['no_masked_or_nodata_pixels'] = unmasked
            errors.extend(k for k, value in checks.items() if not value)
    except (OSError, ValueError, rasterio.errors.RasterioError) as exc:
        errors.append(f'{type(exc).__name__}: {exc}')
    result['format_pass'] = not errors and bool(checks)
    result['limitations'] = ('Strict all-pixel preflight only; no official footprint, holdout, '
                             'leakage, registry uniqueness, or organizer acceptance checked.')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate')
    parser.add_argument('reference', help='official sample submission')
    args = parser.parse_args()
    report = validate(args.candidate, args.reference)
    print(json.dumps(report, indent=2, allow_nan=False))
    return 0 if report['format_pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
