#!/usr/bin/env python3
"""promote_retries.py — fold finished 0.1% retries into the final output set.

Mechanical rule, applied per cell with a completed retry (outputs_p001retry_X
containing total_cost.txt):

  - retry objective <= existing objective  ->  PROMOTE: the existing dir is
    renamed to outputs_p0015bak_X (kept as the 0.15% archive) and the retry
    dir takes its place. Marker .confirmed_p001 is written.
  - retry objective  > existing objective  ->  CERTIFY: the retry's proven
    0.1% bound also certifies the existing (better) incumbent, since a bound
    that puts the retry's worse objective within 0.1% puts any lower objective
    within 0.1% of the same bound. Keep the existing dir, write the marker,
    leave the retry dir in place for the record.

Idempotent: cells whose marker already exists are skipped. Run any time;
safe while other retries are still solving (their dirs lack total_cost.txt
until Switch finishes post-solve output).
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def manifest():
    """outputs_dir -> solve-evidence row from results/SOLVE_MANIFEST.csv."""
    import csv
    p = REPO / "results" / "SOLVE_MANIFEST.csv"
    if not p.exists():
        return {}
    if not hasattr(manifest, "_cache"):
        manifest._cache = {r["outputs_dir"]: r for r in csv.DictReader(open(p))}
    return manifest._cache


actions = []
for retry in sorted(REPO.glob("outputs_p001retry_*")):
    name = retry.name.replace("outputs_p001retry_", "")
    rtc = retry / "total_cost.txt"
    if not rtc.exists():
        actions.append(f"SKIP    {name}: retry still solving")
        continue
    final = REPO / f"outputs_p001_{name}"
    marker = final / ".confirmed_p001"
    if marker.exists():
        actions.append(f"SKIP    {name}: already confirmed")
        continue
    if not (final / "total_cost.txt").exists():
        actions.append(f"WARN    {name}: no existing p001 result; promoting retry outright")
        retry.rename(final)
        ev = manifest().get("outputs_p001retry_" + name, {})
        if ev.get("relmipgap_achieved") and float(ev["relmipgap_achieved"]) <= 0.001:
            (final / ".confirmed_p001").touch()
        continue
    rcost = float(rtc.read_text().strip())
    fcost = float((final / "total_cost.txt").read_text().strip())
    if rcost <= fcost:
        bak = REPO / f"outputs_p0015bak_{name}"
        final.rename(bak)
        retry.rename(final)
        ev = manifest().get("outputs_p001retry_" + name, {})
        if ev.get("relmipgap_achieved") and float(ev["relmipgap_achieved"]) <= 0.001:
            (final / ".confirmed_p001").touch()
        actions.append(f"PROMOTE {name}: retry {rcost:.0f} <= prior {fcost:.0f}")
    else:
        # The certification argument (prior incumbent <= retry incumbent,
        # retry proved a bound within 0.1%, hence prior is within 0.1%) is
        # valid only if the retry actually PROVED that bound. A finished
        # total_cost.txt is not proof — a time-limited retry writes one too
        # (external-audit finding 5). Require log evidence from the solve
        # manifest; run solve/build_solve_manifest.py after retry logs land.
        ev = manifest().get(retry.name, {})
        g = ev.get("relmipgap_achieved", "")
        if g and float(g) <= 0.001 and "time limit" not in ev.get("phrase", ""):
            marker.touch()
            actions.append(f"CERTIFY {name}: keep prior {fcost:.0f} (better); "
                           f"retry proved gap {float(g):.5f} <= 0.1%")
        else:
            actions.append(f"HOLD    {name}: prior {fcost:.0f} better, but no "
                           f"proven <=0.1% bound in the manifest (achieved: "
                           f"{g or 'no evidence'}) — not certifying")

for a in actions:
    print(a)
if not actions:
    print("no retry dirs found")
