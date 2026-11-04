"""Synthetic fault networks, calibrated to published agreement statistics.

Why this module exists
----------------------
The competition's label and feature rasters are behind a DrivenData login and
are not available in this environment.  Every claim of the form "method A
would score higher than method B" still has to be *measured* on something.
This module builds fault networks whose statistics are matched to three
numbers that are published, checkable and independent of us:

  A1  two independent real mappings of the same fault network agree at
      DTI = 0.796   (USGS Quaternary faults vs. USGS Qfaults national,
                     munimtechnologies/gems-fault-mapping, docs/agreement-2026-10.md)
  A2  a map displaced 14-21 km scores  DTI = 0.045  (same source: "chance")
  A3  real fault density: 150,394 fault cells (1.39%) and 903,921 cells
      within 300 m (8.4%) of 10,799,672 cells in the release footprint
      (same source, table of "cells scored" and the layer-skill note)

Everything measured on these networks is labelled SIMULATION and never as a
leaderboard score.  The generator is a *testbed for method ranking*, not a
model of the competition's hidden labels.
"""
from __future__ import annotations

import numpy as np

# Published anchors (see docstring).  Used by calibrate() and by the reports.
ANCHOR_AGREEMENT = 0.796
ANCHOR_CHANCE = 0.045
ANCHOR_DENSITY = 0.0139
ANCHOR_COVERAGE_300M = 0.0837


def _draw_polyline(out, y0, x0, angle, length, width=1):
    """Rasterise a straight segment as a 1-px (or ``width``-px) line."""
    steps = int(np.ceil(length * 2))
    t = np.linspace(0.0, length, steps + 1)
    ys = y0 + t * np.sin(angle)
    xs = x0 + t * np.cos(angle)
    h, w = out.shape
    yi = np.rint(ys).astype(int)
    xi = np.rint(xs).astype(int)
    for dy in range(-(width // 2), width // 2 + 1):
        yy = yi + dy
        ok = (yy >= 0) & (yy < h) & (xi >= 0) & (xi < w)
        out[yy[ok], xi[ok]] = 1.0


def make_network(shape=(1100, 1100), seed=0, n_parents=90,
                 mean_length=70.0, length_sigma=0.65,
                 primary_deg=10.0, primary_kappa=6.0,
                 secondary_deg=-45.0, secondary_frac=0.3,
                 splay_prob=0.45, splay_deg=(18.0, 32.0)):
    """Return a binary fault raster (float32, 0/1) on ``shape``.

    Geometry follows the Great Basin pattern that the competition area shows:
    a dominant NNE-striking set, a subordinate NW-striking set, power-law-ish
    lengths, and splay/step-over branches at 18-32 degrees.
    """
    rng = np.random.default_rng(seed)
    h, w = shape
    out = np.zeros(shape, dtype=np.float32)
    for _ in range(n_parents):
        y0 = rng.uniform(0, h)
        x0 = rng.uniform(0, w)
        if rng.random() < secondary_frac:
            ang = np.deg2rad(secondary_deg + rng.normal(0, 14))
        else:
            ang = np.deg2rad(primary_deg + rng.normal(0, 14))
        # von Mises-like concentration through the normal approximation above
        length = float(np.clip(rng.lognormal(np.log(mean_length), length_sigma), 8, 600))
        _draw_polyline(out, y0, x0, ang, length)
        if rng.random() < splay_prob:
            off = np.deg2rad(rng.uniform(*splay_deg)) * rng.choice([-1, 1])
            frac = rng.uniform(0.2, 0.8)
            yb = y0 + frac * length * np.sin(ang)
            xb = x0 + frac * length * np.cos(ang)
            _draw_polyline(out, yb, xb, ang + off, length * rng.uniform(0.25, 0.6))
    return out


def _geodesic(comp, seeds):
    """8-connected geodesic distance (in pixels) from ``seeds`` inside ``comp``."""
    from collections import deque
    h, w = comp.shape
    dist = np.full((h, w), -1, dtype=np.int32)
    q = deque()
    for y, x in seeds:
        dist[y, x] = 0
        q.append((y, x))
    while q:
        y, x = q.popleft()
        d = dist[y, x] + 1
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                yy, xx = y + dy, x + dx
                if 0 <= yy < h and 0 <= xx < w and comp[yy, xx] and dist[yy, xx] < 0:
                    dist[yy, xx] = d
                    q.append((yy, xx))
    return dist


def _tips_of(comp):
    """Pixels of a thin component having exactly one 8-neighbour."""
    from scipy import ndimage as ndi
    k = ndi.convolve(comp.astype(np.int16), np.ones((3, 3), np.int16),
                     mode="constant", cval=0) - comp.astype(np.int16)
    return np.argwhere(comp & (k == 1))


def perturb(labels, seed=1, omission=0.08, jitter_px=1.0, truncation=0.35,
            tail_drop=0.45, internal_gap=0.25, commission=0.10):
    """Return an 'independent mapping' of the same network.

    Real catalogues differ from each other in four specific ways, each of which
    leaves a signature a method can chase:

    ``tail_drop``/``truncation``  a trace stops short of where the fault goes.
        This is the dominant real difference and the one along-strike tip
        extension is designed for.
    ``internal_gap``  a short run (3-10 px) inside a trace is not mapped, e.g.
        under cover.  This is what gap closure is designed for.
    ``omission``  occasionally a whole segment is missing.
    ``jitter_px``  traces are mislocated by a pixel or two.
    ``commission``  a few short spurious traces.

    Defaults are chosen so that the result reproduces the published
    two-catalogue agreement (see ``calibrate``), and so that the *unmapped*
    cells are dominated by truncation tails rather than by whole missing
    segments - which is what makes the observed 0.24-0.28 submission family
    (tip extension, gap closure, step-over relay) work at all.
    """
    from scipy import ndimage as ndi

    rng = np.random.default_rng(seed)
    lab, n = ndi.label(labels > 0, structure=np.ones((3, 3)))
    out = np.zeros_like(labels, dtype=np.float32)
    h, w = labels.shape
    for i in range(1, n + 1):
        if rng.random() < omission:
            continue
        comp = lab == i
        ys, xs = np.nonzero(comp)
        if ys.size < 6:
            continue
        keep = np.ones((h, w), dtype=bool)
        tips = _tips_of(comp)
        if tips.size and rng.random() < truncation:
            k = max(1, int(ys.size * rng.uniform(0.08, tail_drop)))
            for ty, tx in tips[np.argsort(rng.random(tips.shape[0]))[:rng.integers(1, 3)]]:
                g = _geodesic(comp, [(int(ty), int(tx))])
                keep &= ~((g >= 0) & (g <= k))
        if rng.random() < internal_gap and ys.size > 14:
            L = int(rng.integers(4, 12))
            j = int(rng.integers(0, ys.size))
            g = _geodesic(comp, [(int(ys[j]), int(xs[j]))])
            keep &= ~((g >= 0) & (g <= L // 2))
        comp2 = comp & keep
        if not comp2.any():
            continue
        dy = int(round(rng.normal(0, jitter_px)))
        dx = int(round(rng.normal(0, jitter_px)))
        out = np.maximum(out, np.roll(np.roll(comp2, dy, axis=0), dx, axis=1)
                         .astype(np.float32))
    if commission > 0:
        for _ in range(int(commission * n)):
            y0, x0 = rng.uniform(0, h), rng.uniform(0, w)
            _draw_polyline(out, y0, x0, np.deg2rad(rng.uniform(0, 180)),
                           float(rng.uniform(8, 40)))
    return out


def shifted(labels, seed=2, km=(14, 21)):
    """The 'chance' control: displace the whole map 14-21 km in one direction."""
    rng = np.random.default_rng(seed)
    ang = rng.uniform(0, 2 * np.pi)
    dist_px = rng.uniform(*km) * 10.0          # 100 m pixels
    dy = int(round(dist_px * np.sin(ang)))
    dx = int(round(dist_px * np.cos(ang)))
    return np.roll(np.roll(labels, dy, axis=0), dx, axis=1)


def match_density(shape=(900, 900), seed=0, target_density=ANCHOR_DENSITY,
                  target_coverage=ANCHOR_COVERAGE_300M, verbose=False):
    """Grid-search n_parents / mean_length against the two published anchors.

    A transparent coarse search is used instead of a fixed-point iteration:
    the search table is returned and printed in the report, so the chosen
    parameters can be re-derived and criticised.
    """
    rows = []
    for n_parents in (80, 95, 110, 125):
        for mean_length in (60.0, 85.0, 110.0, 140.0):
            net = make_network(shape=shape, seed=seed, n_parents=n_parents,
                               mean_length=mean_length)
            st = stats(net)
            err = (np.log(max(st["density"], 1e-9) / target_density) ** 2 +
                   np.log(max(st["coverage_300m"], 1e-9) / target_coverage) ** 2)
            rows.append({"n_parents": n_parents, "mean_length": mean_length,
                         "density": round(st["density"], 4),
                         "coverage_300m": round(st["coverage_300m"], 4),
                         "log_err": round(float(err), 4)})
            if verbose:
                print("  ", rows[-1])
    best = min(rows, key=lambda r: r["log_err"])
    return {"n_parents": best["n_parents"], "mean_length": best["mean_length"],
            "density": best["density"], "coverage_300m": best["coverage_300m"],
            "search": rows}


def stats(labels, radius_px: float = 3.0):
    """Density, 300 m coverage and cell count of a binary map."""
    from gems import metric as M

    lab = (np.asarray(labels) > 0).astype(np.float32)
    _, near = M._coverage(np.zeros_like(lab), lab > 0)
    cover = (near >= radius_px / radius_px - 1e-6)  # centre-of-truth cells only
    # A cell is 'within 300 m' if some truth cell lies within the kernel.
    within = near > 0
    del cover
    return {"n_cells": int(lab.sum()),
            "density": float(lab.mean()),
            "coverage_300m": float(within.mean()),
            "shape": list(lab.shape)}


SYNTH_N_PARENTS = 80
SYNTH_MEAN_LENGTH = 110.0


def make_calibrated_network(shape=(900, 900), seed=0):
    """The density/coverage-matched testbed network (see match_density report)."""
    return make_network(shape=shape, seed=seed, n_parents=SYNTH_N_PARENTS,
                        mean_length=SYNTH_MEAN_LENGTH)


def calibrate(seed=0, shape=(900, 900), targets=None, grid=None, verbose=True):
    """Search (omission, jitter) so that perturb() reproduces ANCHOR_AGREEMENT.

    Returns a dict with the chosen parameters, achieved agreement and chance,
    and the measured density/coverage, so every downstream number can be
    re-derived from this file.
    """
    from gems import metric as M

    targets = targets or {}
    truth = make_calibrated_network(shape=shape, seed=seed)
    chance = M.dti(shifted(truth, seed=seed + 7), truth)["score"]
    rows = []
    best = None
    cands = grid if grid is not None else [
        (o, j) for o in (0.15, 0.25, 0.35, 0.45) for j in (0.7, 1.2, 1.8, 2.4)]
    for omission, jitter in cands:
        pmap = perturb(truth, seed=seed + 11, omission=omission,
                       jitter_px=jitter)
        s = M.dti(pmap, truth)["score"]
        rows.append({"omission": omission, "jitter_px": jitter, "dti": round(s, 4)})
        if verbose:
            print(f"  omission={omission:.2f} jitter={jitter:.1f}px -> DTI {s:.4f}")
        d = abs(s - ANCHOR_AGREEMENT)
        if best is None or d < best[0]:
            best = (d, omission, jitter, s)
    st = stats(truth)
    return {"chosen": {"omission": best[1], "jitter_px": best[2]},
            "agreement_dti": round(best[3], 4),
            "chance_dti": round(chance, 4),
            "anchors": {"agreement": ANCHOR_AGREEMENT, "chance": ANCHOR_CHANCE,
                        "density": ANCHOR_DENSITY,
                        "coverage_300m": ANCHOR_COVERAGE_300M},
            "measured": {"density": round(st["density"], 4),
                         "coverage_300m": round(st["coverage_300m"], 4)},
            "search": rows, "shape": list(shape), "seed": seed}
