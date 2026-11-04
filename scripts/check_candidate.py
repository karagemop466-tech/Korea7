#!/usr/bin/env python3
"""Fail-closed format and lane screening, not a holdout evaluator or promotion system."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import rasterio
from scipy.ndimage import distance_transform_edt
from scipy.stats import rankdata

SITES = {f'GEMSDOE{x}' for x in (24, 25, 27, 28, 30, 31, 32, 33, 36)}


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read(path, grid=None):
    with rasterio.open(path) as src:
        if src.driver != 'GTiff' or src.count != 1 or src.crs is None:
            raise ValueError(f'{path}: expected a single-band GeoTIFF with a CRS')
        if not (src.read_masks(1) != 0).all():
            raise ValueError(f'{path}: masked or nodata pixels are not allowed')
        spec = (src.crs, src.width, src.height, src.transform)
        if grid is not None and spec != grid:
            raise ValueError(f'{path}: CRS, shape or transform mismatch')
        return src.read(1), spec


def rank_correlation(a, b):
    x, y = rankdata(a), rankdata(b)
    if np.ptp(x) == 0 or np.ptp(y) == 0:
        raise ValueError('rank correlation undefined for constant surface')
    rho = float(np.corrcoef(x, y)[0, 1])
    if not np.isfinite(rho):
        raise ValueError('rank correlation is not finite')
    return rho


def screen(candidate, surface, reference, footprint, manifest):
    result = {'status': 'BLOCKED', 'format': {}, 'comparisons': [], 'errors': [],
              'notice': 'Screening only: neither registry completeness nor holdout performance is established.'}
    try:
        template, grid = read(reference)
        del template
        pred, _ = read(candidate, grid)
        surf, _ = read(surface, grid)
        mask, _ = read(footprint, grid)
        if not np.all(np.isfinite(mask)) or not np.all(np.isin(mask, [0, 1])):
            raise ValueError('footprint must be an explicitly supplied finite binary 0/1 raster')
        inside = mask == 1
        if not inside.any():
            raise ValueError('empty footprint')
        result['sha256'] = sha256(candidate)
        result['format'] = {'single_band_crs_shape_transform_match': True,
                            'finite_inside': bool(np.isfinite(pred[inside]).all()),
                            'finite_all': bool(np.isfinite(pred).all()),
                            'all_values_in_0_1': bool(np.isfinite(pred).all() and ((pred >= 0) & (pred <= 1)).all())}
        if not all(result['format'].values()):
            raise ValueError('format check failed; all pixels must be finite and in [0,1]')
        if not np.isfinite(surf[inside]).all():
            raise ValueError('candidate surface has nonfinite footprint pixels')
        # A dot is an explicitly binary positive pixel; arbitrary continuous outputs are rejected.
        if not np.isin(pred, [0, 1]).all():
            raise ValueError('lane dot overlap requires a binary candidate raster')
        dots = (pred == 1) & inside
        if not dots.any():
            raise ValueError('candidate has no dots in footprint')
        items = json.loads(Path(manifest).read_text())
        if not isinstance(items, list) or not SITES.issubset({i['site'] for i in items}):
            raise ValueError('manifest must include each of the nine requested sites')
        for item in items:
            # Resolve manifest paths relative to the manifest, not the invoking directory.
            base = Path(manifest).resolve().parent
            sp, dp = base / item['surface'], base / item['dots']
            if sha256(sp) != item['surface_sha256'] or sha256(dp) != item['dots_sha256']:
                raise ValueError(f"{item['site']}: registry hash mismatch")
            rs, _ = read(sp, grid)
            rd, _ = read(dp, grid)
            if not np.isfinite(rs[inside]).all() or not np.isfinite(rd).all() or not np.isin(rd, [0, 1]).all():
                raise ValueError(f"{item['site']}: invalid registry surface or dots")
            refdots = (rd == 1) & inside
            if not refdots.any():
                raise ValueError(f"{item['site']}: empty registry dots")
            rho = rank_correlation(surf[inside], rs[inside])
            # Euclidean distance in pixel units, exactly <= 3 pixels.
            overlap = float((distance_transform_edt(~refdots)[dots] <= 3).mean())
            result['comparisons'].append({'site': item['site'], 'surface_sha256': item['surface_sha256'],
                                          'dots_sha256': item['dots_sha256'], 'spearman_rho': rho,
                                          'dot_overlap_3px': overlap, 'duplicate': rho > .90 or overlap > .70})
            if result['comparisons'][-1]['duplicate']:
                break
        if any(c['duplicate'] for c in result['comparisons']):
            result['errors'].append('Duplicate/lane drift threshold exceeded; stop.')
        else:
            result['status'] = 'SCREENED_NOT_APPROVED'
    except (OSError, ValueError, KeyError, TypeError, rasterio.errors.RasterioError) as e:
        result['errors'].append(str(e))
    return result


def screen_surface(surface, reference, footprint, manifest):
    """Screen surfaces before dot placement; not proof of a complete registry."""
    result = {'status': 'BLOCKED', 'comparisons': [], 'errors': [],
              'notice': 'Surface screening only; registry completeness is not established.'}
    try:
        _, grid = read(reference)
        values, _ = read(surface, grid)
        mask, _ = read(footprint, grid)
        if not np.isfinite(mask).all() or not np.isin(mask, [0, 1]).all() or not (mask == 1).any():
            raise ValueError('footprint must be a nonempty finite binary raster')
        inside = mask == 1
        if not np.isfinite(values[inside]).all():
            raise ValueError('candidate surface has nonfinite footprint pixels')
        items = json.loads(Path(manifest).read_text())
        if not isinstance(items, list) or not SITES.issubset({i['site'] for i in items}):
            raise ValueError('manifest must include each of the nine requested sites')
        for item in items:
            path = Path(manifest).resolve().parent / item['surface']
            if sha256(path) != item['surface_sha256']:
                raise ValueError(f"{item['site']}: registry hash mismatch")
            other, _ = read(path, grid)
            if not np.isfinite(other[inside]).all():
                raise ValueError(f"{item['site']}: invalid registry surface")
            rho = rank_correlation(values[inside], other[inside])
            result['comparisons'].append({'site': item['site'], 'surface_sha256': item['surface_sha256'],
                                          'spearman_rho': rho, 'duplicate': rho > .90})
            if rho > .90:
                break
        if any(item['duplicate'] for item in result['comparisons']):
            result['errors'].append('Duplicate/lane drift threshold exceeded; stop.')
        else:
            result['status'] = 'SURFACE_SCREENED_NOT_APPROVED'
    except (OSError, ValueError, KeyError, TypeError, rasterio.errors.RasterioError) as e:
        result['errors'].append(str(e))
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('surface', 'reference', 'footprint', 'manifest'):
        p.add_argument('--' + name, required=True)
    p.add_argument('--candidate', help='binary dot raster; omit for pre-placement surface screening')
    args = p.parse_args()
    kwargs = vars(args)
    candidate = kwargs.pop('candidate')
    r = screen(candidate=candidate, **kwargs) if candidate else screen_surface(**kwargs)
    print(json.dumps(r, indent=2, allow_nan=False))
    return 0 if r['status'] in ('SCREENED_NOT_APPROVED', 'SURFACE_SCREENED_NOT_APPROVED') else 1


if __name__ == '__main__':
    raise SystemExit(main())
