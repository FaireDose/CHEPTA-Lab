#!/usr/bin/env python3
"""Send a case's saved CHEPTA request files again, UNCHANGED, to another CHEPTA build, and keep every answer.

Used to check an unreleased CHEPTA commit against the runs of a released version (for example CHEPTA main 415da41
against chepta 0.6.2). Each `<id>.request.json` of the source folder is copied byte for byte into the destination
folder and sent with `node <chepta_dir>/bin/chepta.mjs request --time-ms N <file>`, N being the time limit of the
source run (read from its manifest's command) unless overridden. Output, standard error and a manifest entry are
written for every run, refusals and failures included. The manifest records the CHEPTA commit sha, whether its
working tree was clean, the Node version, and the sha256 of each request (equal to the source's) and output.

  python3 scripts/rerun_chepta_requests.py --src cases/X/results-chepta-0.6.2 --dst cases/X/results-chepta-main-415da41 \
      --chepta-dir /path/to/CHEPTA-checkout [--jobs 4] [--only id1,id2] [--skip id3] [--time-ms id=600000,...] \
      [--extra-dir folder-with-new-request-files]

`--extra-dir`: request files written for this check (new runs, not in the source folder); they are sent the same way
and marked `"new": true` in the manifest. The manifest is merged when only some runs are made. No result is edited.
"""
import argparse
import concurrent.futures as cf
import datetime
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

EXIT = {-9: "stopped by Lab (wall time)", 0: "ok", 2: "invalid_input", 3: "missing_data", 4: "unsupported",
        5: "not_converged", 6: "cancelled", 7: "out_of_time", 8: "error", 1: "command line error"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(d, *a):
    return subprocess.run(["git", "-C", str(d), *a], capture_output=True, text=True).stdout.strip()


def summary(res):
    v = res.get("value") or {}
    q = res.get("qualifications") or {}
    ex = v.get("extrapolations") or []
    return {"extrapolations": [e.get("short") or e.get("message") for e in ex if isinstance(e, dict)],
            "estimated_pairs": q.get("estimated_pairs") or q.get("estimatedPairs") or [],
            "warnings": [w.get("code") if isinstance(w, dict) else w for w in (res.get("warnings") or v.get("warnings") or [])]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    ap.add_argument("--chepta-dir", required=True)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", default="")
    ap.add_argument("--skip", default="")
    ap.add_argument("--time-ms", default="", help="id=ms,... overrides")
    ap.add_argument("--default-time-ms", type=int, default=3000000)
    ap.add_argument("--extra-dir", default="")
    a = ap.parse_args()
    src, dst, cdir = Path(a.src).resolve(), Path(a.dst).resolve(), Path(a.chepta_dir).resolve()
    dst.mkdir(parents=True, exist_ok=True)
    commit = git(cdir, "rev-parse", "HEAD")
    clean = git(cdir, "status", "--porcelain") == ""
    node = subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip()
    cli_version = subprocess.run(["node", str(cdir / "bin/chepta.mjs"), "--version"], capture_output=True, text=True).stdout.strip()
    src_man = {}
    if (src / "run-manifest.json").exists():
        m = json.loads((src / "run-manifest.json").read_text())
        src_man = {r["id"]: r for r in (m["runs"] if isinstance(m, dict) else m)}
    overrides = dict(kv.split("=") for kv in a.time_ms.split(",") if kv)
    only = set(filter(None, a.only.split(",")))
    skip = set(filter(None, a.skip.split(",")))

    jobs = []
    for d, new in [(src, False)] + ([(Path(a.extra_dir).resolve(), True)] if a.extra_dir else []):
        for f in sorted(d.glob("*.request.json")):
            rid = f.name[: -len(".request.json")]
            if (only and rid not in only) or rid in skip:
                continue
            t = a.default_time_ms
            mm = re.search(r"--time-ms (\d+)", (src_man.get(rid) or {}).get("command", ""))
            if mm:
                t = int(mm.group(1))
            t = int(overrides.get(rid, t))
            jobs.append((rid, f, new, t))

    def one(job):
        rid, f, new, t = job
        body = f.read_bytes()
        rf = dst / f"{rid}.request.json"
        rf.write_bytes(body)
        t0 = datetime.datetime.now(datetime.timezone.utc)
        c0 = time.monotonic()
        try:
            p = subprocess.run(["node", str(cdir / "bin/chepta.mjs"), "request", "--time-ms", str(t), str(rf)],
                               capture_output=True, text=True, timeout=t / 1000 + 600)
        except subprocess.TimeoutExpired:
            p = subprocess.CompletedProcess([], -9, "", f"Stopped by Lab's runner after {t / 1000 + 600:.0f} s of wall time.\n")
        wall = time.monotonic() - c0
        (dst / f"{rid}.output.json").write_text(p.stdout)
        (dst / f"{rid}.stderr.txt").write_text(p.stderr)
        try:
            res = json.loads(p.stdout) if p.stdout.strip() else {}
        except json.JSONDecodeError:
            res = {}
        e = res.get("error") or {}
        src_r = src_man.get(rid) or {}
        rec = {"id": rid, "new": new,
               "command": f"node <chepta {commit[:7]}>/bin/chepta.mjs request --time-ms {t} {rf.name}",
               "chepta_commit": commit, "chepta_tree_clean": clean, "chepta_cli_version": cli_version,
               "started_at": t0.isoformat(), "wall_s": round(wall, 1), "exit_code": p.returncode,
               "exit_meaning": EXIT.get(p.returncode, "unknown"), "outcome": res.get("outcome"),
               "error": {"code": e.get("code"), "message": e.get("message")} if e else None,
               "chepta_run_id": (res.get("run") or {}).get("id"), "chepta_elapsed_ms": (res.get("run") or {}).get("elapsed_ms"),
               "request_file_sha256": sha(body), "output_file_sha256": sha(p.stdout.encode()),
               "request_same_as_source": (None if new else sha(body) == src_r.get("request_file_sha256")) if src_r else None,
               "source_outcome": src_r.get("outcome"), **summary(res)}
        print(f"{rid}: {rec['outcome']} {(e or {}).get('code') or ''} ({wall:.0f} s)", flush=True)
        return rec

    recs = []
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for r in ex.map(one, jobs):
            recs.append(r)
    mf = dst / "run-manifest.json"
    old = json.loads(mf.read_text())["runs"] if mf.exists() else []
    keep = {r["id"]: r for r in old}
    for r in recs:
        keep[r["id"]] = r
    man = {"what": f"The saved request files of {src.name}, sent again unchanged (and new runs marked new) to CHEPTA at commit "
                   f"{commit}, an unreleased build run from its source (bin/chepta.mjs; package.json still says {cli_version}).",
           "chepta_commit": commit, "chepta_repository": "https://github.com/FaireDose/CHEPTA", "chepta_tree_clean": clean,
           "node": node, "source_folder": src.name, "runner": "scripts/rerun_chepta_requests.py",
           "runs": sorted(keep.values(), key=lambda r: r["id"])}
    mf.write_text(json.dumps(man, indent=1) + "\n")


if __name__ == "__main__":
    sys.exit(main())
