#!/usr/bin/env python3
"""Compare a folder of CHEPTA reruns (scripts/rerun_chepta_requests.py) with the source folder's answers.

For each run present in both folders: the outcome and error code before and after, and, when both are `ok`, how much
the numbers moved. Streams (value.streams): mass flow (relative), temperature (K), vapour fraction and every
component's mole fraction (absolute); block duties (value.blocks[*].duty_kW, relative to the largest duty of the run);
and every other number under `value` (relative, 1e-12 floor) as a catch-all. Verdicts:
  same      outcome unchanged and, when ok, streams within 5e-5 relative in flow, 0.005 K, 5e-6 in mole fraction,
            duties within 5e-5 of the largest duty (the README tables print 4-5 significant digits)
  changed   outcome unchanged (ok), numbers moved more than that (the largest moves are listed)
  now runs  the source run failed or was refused, the rerun is ok
  regressed the source run was ok, the rerun is not
  still fails / fails differently   neither is ok (same code / another code)
Writes <dst>/comparison-with-<src>.json and prints one line per run. No CHEPTA call.
  python3 scripts/compare_chepta_reruns.py --src cases/X/results-chepta-0.6.2 --dst cases/X/results-chepta-main-415da41
"""
import argparse
import json
from pathlib import Path

SKIP_KEYS = {"elapsed_ms", "id", "input_hash", "started_at", "run"}


def leaves(x, path=""):
    if isinstance(x, bool) or x is None:
        return
    if isinstance(x, (int, float)):
        yield path, float(x)
    elif isinstance(x, dict):
        for k, v in x.items():
            if k not in SKIP_KEYS:
                yield from leaves(v, f"{path}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, f"{path}[{i}]")


def stream_moves(a, b):
    out = {"flow_rel": (0.0, None), "T_K": (0.0, None), "z_abs": (0.0, None), "VF_abs": (0.0, None)}
    for sid, s in (a.get("streams") or {}).items():
        t = (b.get("streams") or {}).get(sid)
        if not t or not isinstance(s, dict):
            continue
        def upd(k, v):
            if v > out[k][0]:
                out[k] = (v, sid)
        fa, fb = s.get("mass_kg_h") or s.get("F_kmol_h") or 0, t.get("mass_kg_h") or t.get("F_kmol_h") or 0
        upd("flow_rel", abs(fb - fa) / max(abs(fa), 1e-9) if (fa or fb) else 0.0)
        if s.get("T_K") is not None and t.get("T_K") is not None:
            upd("T_K", abs(t["T_K"] - s["T_K"]))
        if s.get("VF") is not None and t.get("VF") is not None:
            upd("VF_abs", abs(t["VF"] - s["VF"]))
        for za, zb in zip(s.get("z") or [], t.get("z") or []):
            upd("z_abs", abs(zb - za))
    return {k: {"value": v[0], "where": v[1]} for k, v in out.items()}


def duty_moves(a, b):
    ba, bb = a.get("blocks") or {}, b.get("blocks") or {}
    scale = max([abs(v.get("duty_kW") or 0) for v in ba.values() if isinstance(v, dict)] + [1e-9])
    worst = (0.0, None)
    for k, v in ba.items():
        if isinstance(v, dict) and k in bb and isinstance(bb[k], dict) and v.get("duty_kW") is not None and bb[k].get("duty_kW") is not None:
            d = abs(bb[k]["duty_kW"] - v["duty_kW"]) / scale
            if d > worst[0]:
                worst = (d, k)
    return {"rel_to_largest": worst[0], "where": worst[1]}


def other_moves(a, b, n=5):
    la, lb = dict(leaves(a)), dict(leaves(b))
    diffs = []
    for k, v in la.items():
        if k in lb:
            d = abs(lb[k] - v) / max(abs(v), abs(lb[k]), 1e-12)
            if d > 1e-9:
                diffs.append((d, k, v, lb[k]))
    diffs.sort(reverse=True)
    return {"numbers_compared": len(set(la) & set(lb)), "numbers_moved_1e-9": len(diffs),
            "only_in_source": len(set(la) - set(lb)), "only_in_rerun": len(set(lb) - set(la)),
            "largest": [{"path": k, "source": v, "rerun": w, "rel": d} for d, k, v, w in diffs[:n]]}


def warning_codes(x, inside=False, acc=None):
    """Every warning code (or text) found in any `warnings` list of an answer, with the number of times seen."""
    acc = {} if acc is None else acc
    if isinstance(x, dict):
        for k, v in x.items():
            warning_codes(v, inside or k == "warnings", acc)
        if inside and x.get("code"):
            acc[x["code"]] = acc.get(x["code"], 0) + 1
    elif isinstance(x, list):
        for v in x:
            if inside and isinstance(v, str):
                acc[v[:80]] = acc.get(v[:80], 0) + 1
            else:
                warning_codes(v, inside, acc)
    return acc


def load(p):
    try:
        return json.loads(p.read_text()) if p.exists() and p.read_text().strip() else {}
    except json.JSONDecodeError:
        return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    a = ap.parse_args()
    src, dst = Path(a.src), Path(a.dst)
    man = json.loads((dst / "run-manifest.json").read_text())
    rows = []
    for r in man["runs"]:
        rid = r["id"]
        o1, o2 = load(src / f"{rid}.output.json"), load(dst / f"{rid}.output.json")
        e1, e2 = o1.get("error") or {}, o2.get("error") or {}
        row = {"id": rid, "new": r.get("new", False), "source_outcome": o1.get("outcome"), "source_code": e1.get("code"),
               "rerun_outcome": o2.get("outcome"), "rerun_code": e2.get("code"), "rerun_message": e2.get("message"),
               "wall_s": r.get("wall_s"), "source_warnings": warning_codes(o1), "rerun_warnings": warning_codes(o2)}
        if r.get("new") or not o1:
            row["verdict"] = "new run"
        elif o1.get("outcome") == "ok" and o2.get("outcome") == "ok":
            v1, v2 = o1.get("value") or {}, o2.get("value") or {}
            sm, dm = stream_moves(v1, v2), duty_moves(v1, v2)
            om = other_moves(v1, v2)
            row.update({"streams": sm, "duties": dm, "all_numbers": om})
            if sm["flow_rel"]["value"] or sm["T_K"]["value"] or dm["where"]:
                same = (sm["flow_rel"]["value"] <= 5e-5 and sm["T_K"]["value"] <= 5e-3 and sm["z_abs"]["value"] <= 5e-6
                        and sm["VF_abs"]["value"] <= 5e-6 and dm["rel_to_largest"] <= 5e-5)
            else:
                same = all(x["rel"] <= 5e-5 for x in om["largest"])
            row["verdict"] = "same" if same else "changed"
        elif o1.get("outcome") == "ok":
            row["verdict"] = "regressed"
        elif o2.get("outcome") == "ok":
            row["verdict"] = "now runs"
        else:
            row["verdict"] = "still fails" if (o1.get("outcome"), e1.get("code")) == (o2.get("outcome"), e2.get("code")) else "fails differently"
        rows.append(row)
        extra = ""
        if "streams" in row:
            extra = (f" flow {row['streams']['flow_rel']['value']:.1e} T {row['streams']['T_K']['value']:.1e} K "
                     f"z {row['streams']['z_abs']['value']:.1e} duty {row['duties']['rel_to_largest']:.1e}")
        print(f"{row['verdict']:<17} {rid}: {row['source_outcome']}/{row['source_code']} -> {row['rerun_outcome']}/{row['rerun_code']}{extra}")
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    out = {"method": __doc__.split("\n\n")[0] + " See the script's docstring for the thresholds.",
           "source": src.name, "rerun": dst.name, "chepta_commit": man.get("chepta_commit"), "counts": counts, "runs": rows}
    (dst / f"comparison-with-{src.name}.json").write_text(json.dumps(out, indent=1) + "\n")
    print(counts)


if __name__ == "__main__":
    main()
