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
        (final / ".confirmed_p001").touch()
        continue
    rcost = float(rtc.read_text().strip())
    fcost = float((final / "total_cost.txt").read_text().strip())
    if rcost <= fcost:
        bak = REPO / f"outputs_p0015bak_{name}"
        final.rename(bak)
        retry.rename(final)
        (final / ".confirmed_p001").touch()
        actions.append(f"PROMOTE {name}: retry {rcost:.0f} <= prior {fcost:.0f}")
    else:
        marker.touch()
        actions.append(f"CERTIFY {name}: keep prior {fcost:.0f} (better); retry bound {rcost:.0f} proves <=0.1%")

for a in actions:
    print(a)
if not actions:
    print("no retry dirs found")
