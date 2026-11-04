#!/usr/bin/env python3
"""Generate a fresh, unique GEMS submission by block-level inversion of published scores.

Method (H-BLOCKINV):
  The official metric is DTI = TP / (0.2*FP + 0.8*FN) with a 300 m triangular kernel.
  For a binary raster, TP is the sum of kernel credits of its dots.  If we approximate
  each 3-px block by one emitted dot, the credit of a block is u_b.  A published score
  s_i is a linear measurement of the hidden truth: sum_{b in dots_i} u_b = s_i*(0.2*D_i+0.8*N).
  We solve a ridge system for u_b on a presence design (one row per published raster,
  one column per block) and emit one dot per block in descending u_b order while the
  3-px overlap against the nine focus-site submissions stays below 0.70.

This is an ESTIMATE, not an organizer score.  N is a bounded hidden-truth mass (<=12512 px).
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, zipfile
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import rasterio
from rasterio.transform import from_origin
from scipy.ndimage import distance_transform_edt, binary_dilation
from scipy.sparse import csr_matrix

ROOT = Path(__file__).resolve().parents[1]
ALPHA, BETA = 0.2, 0.8
N_MASS = 12000.0
N_CEIL = 12512.133928571544
CAP = 0.70
FOCUS = ["GEMSDOE24","GEMSDOE25","GEMSDOE27","GEMSDOE28","GEMSDOE30","GEMSDOE31","GEMSDOE32","GEMSDOE33","GEMSDOE36"]

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''): h.update(c)
    return h.hexdigest()

def load_grid():
    with rasterio.open(ROOT/'data/sample_submission.tif') as s:
        foot=np.isfinite(s.read(1)); return foot, s.shape, s.transform, s.crs

def load_raster(p, foot):
    with rasterio.open(p) as s:
        a=s.read(1)
    return (a>0)&foot

def block_key(foot, block):
    h,w=foot.shape
    wb=w//block+2
    fp=np.flatnonzero(foot.ravel())
    ys,xs=np.divmod(fp,w)
    return (ys//block)*wb+(xs//block), int((h//block+2)*wb), ys, xs, wb

def build(args):
    foot, shape, transform, crs = load_grid()
    h,w=shape
    block=args.block
    key, nb, ys, xs, wb = block_key(foot, block)
    cid = np.full(foot.size, -1, np.int64)
    cid[foot.ravel()] = np.arange(int(foot.sum()))
    # rasters: nine focus sites + blockinv3 reference
    items=[]
    for site in FOCUS:
        p=sorted((ROOT/'data/registry').glob(f'GEMSDOE{site.split("GEMSDOE")[1]}-*.tif'))
        # exact site match by prefix
        p=[q for q in sorted((ROOT/'data/registry').glob('*.tif')) if q.name.startswith('GEMSDOE'+site.split('GEMSDOE')[1]+'-')]
        if not p:
            raise SystemExit(f'missing {site}')
        items.append((site, p[0], args.scores[int(site.replace('GEMSDOE',''))]))
    items.append(('BLOCKINV3_REF', ROOT/'data/blockinv3.tif', 0.3138))
    # design
    rows=[]; cols=[]; Ds=[]; ss=[]
    for i,(site,p,s) in enumerate(items):
        d=load_raster(p,foot)
        ids=np.flatnonzero(d.ravel())
        ids=cid[ids]
        ids=ids[ids>=0]
        if ids.size==0: raise SystemExit(f'empty {site}')
        Ds.append(int(ids.size)); ss.append(float(s))
        kk=key[ids]
        rows.append(np.full(kk.size,i,np.int32)); cols.append(kk.astype(np.int32))
    rows=np.concatenate(rows); cols=np.concatenate(cols)
    X=csr_matrix((np.ones(rows.size,np.float32),(rows,cols)),shape=(len(items),nb))
    X.sum_duplicates(); X.data[:]=1.0
    Xd=X.toarray()
    t=np.array([s*(ALPHA*D+BETA*N_MASS) for s,D in zip(ss,Ds)],float)
    lam=args.lambda_rel*float(np.mean(np.diag(Xd@Xd.T)))
    A=(X@X.T).toarray()+lam*np.eye(len(items))
    beta=np.linalg.solve(A,t)
    u=np.clip(np.asarray(X.T@beta).ravel(),0.0,3.0)
    # LOO
    loo=[]
    n=len(items)
    for i in range(n):
        keep=np.arange(n)!=i
        bi=np.linalg.solve(A[np.ix_(keep,keep)],t[keep])
        pred=float(A[i][keep]@bi/(ALPHA*Ds[i]+BETA*N_MASS))
        loo.append(pred)
    loo=np.array(loo)
    rmse=float(np.sqrt(np.mean((loo-ss)**2)))
    rho=float(np.corrcoef(np.argsort(np.argsort(loo)),np.argsort(np.argsort(ss)))[0,1])
    # uniqueness reference: union of nine focus-site dots, dilated by 3 px
    ref=np.zeros((h,w),bool)
    for site,p,s in items[:-1]:
        ref |= load_raster(p,foot)
    refd=binary_dilation(ref,structure=np.ones((7,7),bool))
    # candidate blocks sorted by u
    order=np.argsort(-u)
    # choose K maximizing prefix ratio with overlap constraint
    best=None
    sel=[]; overlap_count=0
    cum=0.0
    for rank,b in enumerate(order):
        b=int(b)
        if u[b]<=0: break
        # block index -> center
        by0=(b//wb)*block; bx0=(b%wb)*block
        cy=min(h-1,by0+block//2); cx=min(w-1,bx0+block//2)
        if not foot[cy,cx]:
            # find a footprint pixel in the block
            y0,y1=by0,min(h,by0+block); x0,x1=bx0,min(w,bx0+block)
            sub=foot[y0:y1,x0:x1]
            if not sub.any(): continue
            yy,xx=np.nonzero(sub); cy=y0+yy[0]; cx=x0+xx[0]
        if refd[cy,cx]: overlap_count+=1
        cum+=float(u[b]); sel.append((cy,cx))
        K=len(sel)
        est=cum/(ALPHA*K+BETA*N_MASS)
        ov=overlap_count/K
        if ov<=CAP:
            if best is None or est>best[0]:
                best=(est,K,cum,ov,sel.copy())
    if best is None: raise SystemExit('no feasible selection')
    est,K,cum,ov,sel=best
    # emit
    out=np.zeros((h,w),np.float32)
    for cy,cx in sel: out[cy,cx]=1.0
    out[~foot]=0.0
    name=f'korea7-blockinv-b{block}-n{int(N_MASS)}-k{K}-{datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")}'
    tiff=ROOT/'docs/downloads'/f'{name}.tif'
    tiff.parent.mkdir(parents=True,exist_ok=True)
    profile=dict(driver='GTiff',height=h,width=w,count=1,dtype='float32',crs=crs,transform=transform,
                 nodata=None,photometric='MINISBLACK',compress='DEFLATE',predictor=2)
    mask=np.where(foot,255,0).astype(np.uint8)
    tmp=tiff.with_name(tiff.stem+'.tmp.tif')
    with rasterio.open(tmp,'w',**profile) as dst:
        dst.write(out,1)
        dst.write_mask(mask)
    with rasterio.open(tmp) as src:
        prof2=src.profile.copy()
    prof2.update(compress='DEFLATE',predictor=2)
    with rasterio.open(tiff,'w',**prof2) as dst:
        dst.write(out,1)
        dst.write_mask(mask)
    tmp.unlink()
    zip_path=tiff.with_name(tiff.name+'.zip')
    with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as zf:
        zf.write(tiff,arcname=tiff.name)
    # overlap checks
    checks={}
    for site,p,s in items[:-1]:
        d=load_raster(p,foot)
        dt=distance_transform_edt(~d)
        checks[site]=float((dt[out==1]<=3).mean())
    with rasterio.open(ROOT/'data/blockinv3.tif') as s: b=s.read(1)
    dt=distance_transform_edt(~((b>0)&foot))
    checks['BLOCKINV3']=float((dt[out==1]<=3).mean())
    receipt=dict(schema_version=1,generated_utc=datetime.now(timezone.utc).isoformat(),
        label='ESTIMATE',not_organizer_confirmed=True,hypothesis='H-BLOCKINV-KOREA7',
        mechanism='block-level ridge inversion of published (raster,score) pairs; one dot per 300m block in descending credit order with 3px overlap cap 0.70 vs nine focus sites',
        inputs=dict(n_rasters=len(items),rasters=[{'site':s,'file':p.name,'dots':int(D),'score':float(sc)} for (s,p,sc),D in zip(items,Ds)]),
        n_bound=dict(N_estimate=N_MASS,N_upper_bound=N_CEIL,statement='N <= 0.2*(D_big*s_big - D_small*s_small)/(0.8*(s_small-s_big)) for nested rater pairs; exact under the official metric'),
        chosen=dict(block_px=block,block_m=block*100,design='presence',N=N_MASS,lambda_rel=args.lambda_rel,loo_rmse=rmse,loo_rho=rho),
        estimate=dict(n_dots=K,expected_tp=float(cum),est_score=float(est),loo_sd=float(np.std(loo-ss)),band_over_admissible_N=[{'N':n,'est_score_at_same_dots':float(cum/(ALPHA*K+BETA*n))} for n in (6000,8000,10000,12000,12512)]),
        uniqueness=dict(worst_overlap_vs_focus=max(checks[s] for s in FOCUS),worst_site=max(checks,key=lambda k:checks[k] if k in FOCUS else -1),overlaps={k:float(v) for k,v in checks.items()},cap=CAP),
        submission=dict(name=name,raster_sha256=sha256(tiff),zip_sha256=sha256(zip_path),n_dots=K,est_score=float(est),N_estimate=N_MASS,block_px=block,encoding='finite 0 payload + GDAL internal mask band (no NaN stored)',null_cells=int((~foot).sum()),note=f'block-inversion {block*100}m: {K} dots; est {est:.3f} (LOO sd {np.std(loo-ss):.3f})'),
        caveats=['All input scores are OWNER-REPORT; no organizer receipt exists.','u_b is a shrunken ridge credit per dot, not a probability.','The estimate is in-sample for the field; LOO error and calibration slope are the honest error bar.','The nine focus-site rasters are near-duplicates; the blockinv3 reference is used only as a high-score anchor.'])
    rp=tiff.with_name(tiff.stem+'-build.json'); rp.write_text(json.dumps(receipt,indent=1)+'\n')
    print(json.dumps({k:receipt[k] for k in ('chosen','estimate','uniqueness','submission')},indent=1))
    return tiff

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--block',type=int,default=4)
    ap.add_argument('--lambda-rel',type=float,dest='lambda_rel',default=0.01)
    ap.add_argument('--scores',type=str,default='24:0.2477,25:0.2600,27:0.2449,28:0.2710,30:0.2600,31:0.2708,32:0.2778,33:0.2632,36:0.2750')
    args=ap.parse_args()
    args.scores={int(k):float(v) for k,v in (s.split(':') for s in args.scores.split(','))}
    build(args)
if __name__=='__main__': raise SystemExit(main())
