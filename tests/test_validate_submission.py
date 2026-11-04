import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_submission import validate


def raster(path, values, *, crs='EPSG:32611', transform=None, nodata=None, count=1, dtype='float32'):
    values = np.asarray(values, dtype=dtype)
    with rasterio.open(path, 'w', driver='GTiff', height=values.shape[0], width=values.shape[1],
                       count=count, dtype=dtype, crs=crs,
                       transform=transform or from_origin(0, 100, 10, 10), nodata=nodata) as f:
        for i in range(1, count + 1):
            f.write(values, i)


def test_valid_is_not_promoted(tmp_path):
    ref, candidate = tmp_path / 'ref.tif', tmp_path / 'candidate.tif'
    raster(ref, [[0, 1], [0, 0]])
    raster(candidate, [[0, 1], [.5, 0]])
    r = validate(candidate, ref)
    assert r['format_pass'] and not r['ready_to_submit'] and len(r['sha256']) == 64


def test_bad_pixels_and_mask(tmp_path):
    ref, candidate = tmp_path / 'ref.tif', tmp_path / 'candidate.tif'
    raster(ref, [[0, 1], [0, 0]])
    for value in (float('nan'), float('inf'), -0.0001, 1.0001):
        raster(candidate, [[value, 1], [0, 0]])
        assert not validate(candidate, ref)['format_pass']
    raster(candidate, [[0, 1], [0, 0]], nodata=0)
    assert not validate(candidate, ref)['checks']['no_masked_or_nodata_pixels']


def test_grid_and_count(tmp_path):
    ref, candidate = tmp_path / 'ref.tif', tmp_path / 'candidate.tif'
    raster(ref, [[0, 1], [0, 0]])
    for kwargs in ({'crs': 'EPSG:4326'}, {'transform': from_origin(1, 100, 10, 10)}, {'count': 2}, {'dtype': 'float64'}):
        raster(candidate, [[0, 1], [0, 0]], **kwargs)
        assert not validate(candidate, ref)['format_pass']
    raster(candidate, [[0]])
    assert not validate(candidate, ref)['checks']['shape_match']
    assert not validate(tmp_path / 'missing', ref)['format_pass']
    assert not validate(candidate, tmp_path / 'missing')['format_pass']
