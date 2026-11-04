import json
from pathlib import Path
import sys
import numpy as np
import rasterio
from rasterio.transform import from_origin

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_candidate import SITES, screen, sha256


def write(path, data, transform=None, dtype='float32'):
    with rasterio.open(path, 'w', driver='GTiff', height=data.shape[0], width=data.shape[1],
                       count=1, dtype=dtype, crs='EPSG:32611',
                       transform=transform or from_origin(0, 100, 1, 1)) as dst:
        dst.write(data.astype(dtype), 1)


def fixtures(tmp_path):
    rng = np.random.default_rng(7)
    a = rng.random((12, 12)); b = rng.random((12, 12))
    dot = np.zeros((12, 12)); dot[0, 0] = 1
    other = np.zeros((12, 12)); other[11, 11] = 1
    for name, arr in [('ref', a), ('mask', np.ones_like(a)), ('surface', a),
                      ('candidate', dot), ('rs', b), ('rd', other)]:
        write(tmp_path / (name + '.tif'), arr)
    items = [{'site': s, 'surface': 'rs.tif', 'dots': 'rd.tif',
              'surface_sha256': sha256(tmp_path / 'rs.tif'),
              'dots_sha256': sha256(tmp_path / 'rd.tif')} for s in SITES]
    (tmp_path / 'registry.json').write_text(json.dumps(items))
    return {k: tmp_path / (v + '.tif') for k, v in [('candidate','candidate'), ('surface','surface'), ('reference','ref'), ('footprint','mask')]} | {'manifest': tmp_path / 'registry.json'}


def test_screen_is_not_approval(tmp_path):
    args = fixtures(tmp_path)
    assert screen(**args)['status'] == 'SCREENED_NOT_APPROVED'


def test_non_float32_candidate_blocks(tmp_path):
    args = fixtures(tmp_path)
    with rasterio.open(args['candidate']) as src:
        data = src.read(1)
        transform = src.transform
    write(args['candidate'], data, transform, dtype='float64')
    result = screen(**args)
    assert result['status'] == 'BLOCKED'
    assert result['format']['float32'] is False


def test_out_of_range_and_nan_block(tmp_path):
    args = fixtures(tmp_path)
    for val in (1.2, np.nan, -9999):
        a = np.zeros((12, 12)); a[0, 0] = 1; a[1, 1] = val
        write(args['candidate'], a)
        assert screen(**args)['status'] == 'BLOCKED'


def test_duplicate_and_missing_registry_block(tmp_path):
    args = fixtures(tmp_path)
    write(tmp_path / 'rd.tif', rasterio.open(args['candidate']).read(1))
    items = json.loads(args['manifest'].read_text())
    for i in items: i['dots_sha256'] = sha256(tmp_path / 'rd.tif')
    args['manifest'].write_text(json.dumps(items))
    assert screen(**args)['status'] == 'BLOCKED'
    args['manifest'].write_text(json.dumps(items[:-1]))
    assert screen(**args)['status'] == 'BLOCKED'


def test_wrong_transform_and_hash_block(tmp_path):
    args = fixtures(tmp_path)
    write(args['candidate'], np.zeros((12, 12)), from_origin(1,100,1,1))
    assert screen(**args)['status'] == 'BLOCKED'
    args = fixtures(tmp_path)
    write(tmp_path / 'rs.tif', np.ones((12, 12)))
    assert screen(**args)['status'] == 'BLOCKED'


def test_surface_duplicate_and_constant_block(tmp_path):
    args = fixtures(tmp_path)
    with rasterio.open(args['surface']) as src:
        a = src.read(1)
    write(tmp_path / 'rs.tif', a)
    items = json.loads(args['manifest'].read_text())
    for i in items: i['surface_sha256'] = sha256(tmp_path / 'rs.tif')
    args['manifest'].write_text(json.dumps(items))
    result = screen(**args)
    assert result['status'] == 'BLOCKED' and result['comparisons'][0]['duplicate']
    write(args['surface'], np.ones((12, 12)))
    assert 'undefined' in screen(**args)['errors'][0]


def test_dot_distance_threshold_is_inclusive(tmp_path):
    args = fixtures(tmp_path)
    a = np.zeros((12, 12)); a[0, 3] = 1
    write(tmp_path / 'rd.tif', a)
    items = json.loads(args['manifest'].read_text())
    for i in items: i['dots_sha256'] = sha256(tmp_path / 'rd.tif')
    args['manifest'].write_text(json.dumps(items))
    result = screen(**args)
    assert result['comparisons'][0]['dot_overlap_3px'] == 1.0
    assert result['status'] == 'BLOCKED'
