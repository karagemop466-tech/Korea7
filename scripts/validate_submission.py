#!/usr/bin/env python3
"""Fail-closed format + uniqueness validator for a GEMS submission TIF."""
import argparse, hashlib, json, zipfile
from pathlib import Path
import numpy as np, rasterio
from scipy.ndimage import distance_transform_edt
ROOT=Path(__file__).resolve().parents[1]
FOCUS=[f'GEMSDOE{x}' for x in (24,25,27,28,30,31,32,33,36)]
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''): h.update(c)
    return h.hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--tif',required=True); ap.add_argument('--out',default=None); args=ap.parse_args()
    tif=Path(args.tif); res={'tif':str(tif),'sha256':sha(tif),'checks':{},'errors':[]}
    with rasterio.open(ROOT/'data/sample_submission.tif') as s:
        foot=np.isfinite(s.read(1)); ref=(s.shape,s.transform,s.crs)
    with rasterio.open(tif) as s:
        a=s.read(1); m=s.read_masks(1)>0
        res['checks'].update({'single_band':s.count==1,'float32':s.dtypes[0]=='float32','crs':str(s.crs)=='EPSG:32611',
            'shape':tuple(s.shape)==ref[0],'transform':tuple(round(v,6) for v in s.transform.to_gdal())==tuple(round(v,6) for v in ref[1].to_gdal()),
            'mask_band':bool((s.mask_flag_enums[0]!=[rasterio.enums.MaskFlags.all_valid]))})
    vals=a[np.isfinite(a)]
    res['checks'].update({'all_values_in_0_1':bool(vals.size and vals.min()>=0 and vals.max()<=1),
        'binary':bool(np.isin(np.unique(vals),[0.0,1.0]).all()),'no_nan_inside':bool(np.isfinite(a[foot]).all()),
        'nulls_outside':bool((not m[~foot].any()) and m[foot].all())})
    dots=(a==1)&foot
    res['n_dots']=int(dots.sum()); res['checks'].update({'dots_inside':bool((a[~foot]==0).all()),'has_dots':bool(dots.any())})
    # uniqueness vs nine focus sites (3px)
    ov={}
    for site in FOCUS:
        p=[q for q in sorted((ROOT/'data/registry').glob('*.tif')) if q.name.startswith(site+'-')]
        if not p: continue
        with rasterio.open(p[0]) as s: d=s.read(1)
        d=(d>0)&foot
        ov[site]=float((distance_transform_edt(~d)[dots]<=3).mean())
    res['overlap_vs_focus']=ov; res['worst_overlap']=max(ov.values()) if ov else None
    res['checks']['unique_vs_focus_under_0p70']=bool(ov and max(ov.values())<=0.70)
    # zip
    zp=tif.with_name(tif.name+'.zip'); res['zip']=str(zp) if zp.exists() else None
    if zp.exists():
        with zipfile.ZipFile(zp) as zf:
            names=zf.namelist(); res['checks'].update({'zip_single_member':len(names)==1,'zip_member':names==[tif.name],'zip_bytes':zf.read(names[0])==tif.read_bytes()})
    res['ok']=all(res['checks'].values()) and not res['errors']
    if args.out: Path(args.out).write_text(json.dumps(res,indent=1)+'\n')
    print(json.dumps(res,indent=1)); return 0 if res['ok'] else 1
if __name__=='__main__': raise SystemExit(main())
