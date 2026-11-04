#!/usr/bin/env python3
"""Pre-placement lane screen. Passing is not approval or proof of registry completeness."""
import argparse
import json
from pathlib import Path

import numpy as np
import rasterio

from check_candidate import SITES, rank_correlation, read, sha256


def screen_surface(surface, reference, footprint, manifest):
    result = {'status': 'BLOCKED', 'comparisons': [], 'errors': [],
              'notice': 'Pre-placement screening only; registry completeness is not established.'}
    try:
        _, grid = read(reference)
        values, _ = read(surface, grid)
        mask, _ = read(footprint, grid)
        with rasterio.open(footprint) as src:
            if not (src.read_masks(1) != 0).all():
                raise ValueError('footprint contains masked pixels')
        if not np.isfinite(mask).all() or not np.isin(mask, [0, 1]).all() or not (mask == 1).any():
            raise ValueError('footprint must be nonempty and binary')
        inside = mask == 1
        with rasterio.open(surface) as src:
            if not (src.read_masks(1)[inside] != 0).all():
                raise ValueError('surface has masked footprint pixels')
        if not np.isfinite(values[inside]).all():
            raise ValueError('surface has nonfinite footprint pixels')
        items = json.loads(Path(manifest).read_text())
        if not isinstance(items, list) or not SITES.issubset({i['site'] for i in items}):
            raise ValueError('manifest must include each of the nine requested sites')
        for item in items:
            path = Path(manifest).resolve().parent / item['surface']
            if sha256(path) != item['surface_sha256']:
                raise ValueError(f"{item['site']}: registry surface hash mismatch")
            prior, _ = read(path, grid)
            with rasterio.open(path) as src:
                if not (src.read_masks(1)[inside] != 0).all():
                    raise ValueError(f'{path}: masked footprint pixels')
            if not np.isfinite(prior[inside]).all():
                raise ValueError(f'{path}: nonfinite footprint pixels')
            rho = rank_correlation(values[inside], prior[inside])
            result['comparisons'].append({'site': item['site'], 'surface_sha256': item['surface_sha256'],
                                          'spearman_rho': rho, 'duplicate': rho > .90})
            if rho > .90:
                result['errors'].append('Duplicate/lane drift threshold exceeded; stop.')
                return result
        result['status'] = 'SCREENED_NOT_APPROVED'
    except (OSError, ValueError, KeyError, TypeError, rasterio.errors.RasterioError) as exc:
        result['errors'].append(str(exc))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('surface', 'reference', 'footprint', 'manifest'):
        parser.add_argument('--' + name, required=True)
    result = screen_surface(**vars(parser.parse_args()))
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result['status'] == 'SCREENED_NOT_APPROVED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
