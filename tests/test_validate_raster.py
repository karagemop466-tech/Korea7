import importlib.util
import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin

spec = importlib.util.spec_from_file_location('validator', 'scripts/validate_raster.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def write(path, data, **overrides):
    opts = dict(driver='GTiff', height=3, width=4, count=1, dtype='float32',
                crs='EPSG:32611', transform=from_origin(100, 200, 10, 10))
    opts.update(overrides)
    with rasterio.open(path, 'w', **opts) as dst:
        for band in range(1, opts['count'] + 1):
            dst.write(np.asarray(data, dtype='float32'), band)


def test_good_is_not_promotion(tmp_path):
    ref, candidate = tmp_path/'ref.tif', tmp_path/'candidate.tif'
    write(ref, np.zeros((3, 4)))
    write(candidate, np.full((3, 4), .5))
    result = v.validate(candidate, ref)
    assert result['format_preflight_passed']
    assert not result['ready_to_submit']
    assert len(result['sha256']) == 64


@pytest.mark.parametrize('value', [float('nan'), float('inf'), -0.001, 1.001])
def test_bad_values(tmp_path, value):
    ref, candidate = tmp_path/'ref.tif', tmp_path/'candidate.tif'
    write(ref, np.zeros((3, 4)))
    data = np.zeros((3, 4)); data[0, 0] = value
    write(candidate, data)
    assert not v.validate(candidate, ref)['format_preflight_passed']


@pytest.mark.parametrize('options', [dict(count=2), dict(crs='EPSG:4326'),
                                      dict(transform=from_origin(101, 200, 10, 10)),
                                      dict(nodata=0)])
def test_bad_metadata_or_mask(tmp_path, options):
    ref, candidate = tmp_path/'ref.tif', tmp_path/'candidate.tif'
    write(ref, np.zeros((3, 4)))
    write(candidate, np.zeros((3, 4)), **options)
    assert not v.validate(candidate, ref)['format_preflight_passed']


def test_shape_and_missing_file(tmp_path):
    ref, candidate = tmp_path/'ref.tif', tmp_path/'candidate.tif'
    write(ref, np.zeros((3, 4)))
    write(candidate, np.zeros((2, 4)), height=2)
    assert not v.validate(candidate, ref)['format_preflight_passed']
    assert not v.validate(tmp_path/'missing.tif', ref)['format_preflight_passed']
