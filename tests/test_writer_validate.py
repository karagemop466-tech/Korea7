import numpy as np
import pytest
import rasterio

from gems import validate, writer


def small(tmp_path, arr=None, h=40, w=50, epsg=32611, name="cand.tif"):
    p = tmp_path / name
    prof = writer.make_profile(height=h, width=w, epsg=epsg)
    a = np.zeros((h, w), np.float32) if arr is None else arr
    if arr is not None and (not np.isfinite(arr).all() or arr.min() < 0 or arr.max() > 1):
        # bypass the writer's own guard to build a deliberately bad file
        with rasterio.open(p, "w", **prof) as dst:
            dst.write(a, 1)
        return p
    writer.write_submission(p, a, profile=prof)
    return p


def test_valid_roundtrip(tmp_path):
    p = small(tmp_path)
    ref = small(tmp_path, name="ref.tif")
    rep = validate.validate(p, reference=ref)
    assert rep["status"] == "PASS", rep


def test_writer_refuses_nan(tmp_path):
    with pytest.raises(ValueError, match="non-finite"):
        writer.write_submission(tmp_path / "x.tif",
                                np.full((10, 10), np.nan, np.float32),
                                profile=writer.make_profile(height=10, width=10))


def test_writer_refuses_out_of_range(tmp_path):
    with pytest.raises(ValueError, match="outside"):
        writer.write_submission(tmp_path / "x.tif",
                                np.full((10, 10), 1.5, np.float32),
                                profile=writer.make_profile(height=10, width=10))


def test_validator_rejects_nan_file(tmp_path):
    a = np.zeros((40, 50), np.float32)
    a[2, 2] = np.nan
    ref = small(tmp_path, name="ref.tif")
    rep = validate.validate(small(tmp_path, a), reference=ref)
    assert rep["status"] == "FAIL"
    assert "finite_all" in rep["errors"] or "in_0_1" in rep["errors"]


def test_validator_rejects_out_of_range_file(tmp_path):
    a = np.zeros((40, 50), np.float32)
    a[2, 2] = 1.2
    ref = small(tmp_path, name="ref.tif")
    rep = validate.validate(small(tmp_path, a), reference=ref)
    assert rep["status"] == "FAIL"
    assert "in_0_1" in rep["errors"]


def test_validator_rejects_wrong_shape(tmp_path):
    p = small(tmp_path)
    ref = small(tmp_path, h=41, w=50, name="ref.tif")
    rep = validate.validate(p, reference=ref)
    assert rep["status"] == "FAIL"
    assert "shape_match" in rep["errors"]


def test_validator_rejects_wrong_crs(tmp_path):
    p = small(tmp_path)
    ref = small(tmp_path, epsg=32612, name="ref.tif")
    rep = validate.validate(p, reference=ref)
    assert rep["status"] == "FAIL"
    assert "crs_match" in rep["errors"]


def test_zip_with_one_member_passes(tmp_path):
    import zipfile
    p = small(tmp_path)
    ref = small(tmp_path, name="ref.tif")
    z = tmp_path / "sub.zip"
    with zipfile.ZipFile(z, "w") as f:
        f.write(p, "cand.tif")
    assert validate.validate(z, reference=ref)["status"] == "PASS"


def test_zip_with_two_members_fails(tmp_path):
    import zipfile
    p = small(tmp_path)
    ref = small(tmp_path, name="ref.tif")
    z = tmp_path / "two.zip"
    with zipfile.ZipFile(z, "w") as f:
        f.write(p, "a.tif")
        f.write(p, "b.tif")
    rep = validate.validate(z, reference=ref)
    assert rep["status"] == "FAIL"
