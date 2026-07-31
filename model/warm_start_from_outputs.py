"""Seed integer/binary variables from a previously solved scenario's output dir
so CPLEX can use them as a MIP start.

Usage in scenarios.txt:
    --include-modules warm_start_from_outputs --warmstart-from outputs_1.2x_<name>

Files read (when present), with index columns -> Var name:
  BuildGen.csv                 (GEN_BLD_YRS_1, GEN_BLD_YRS_2)        -> BuildGen
  BuildUnits.csv               (DISCRETE_GEN_BLD_YRS_1, _2)          -> BuildUnits
  BuildStorageEnergy.csv       (STORAGE_GEN_BLD_YRS_1, _2)           -> BuildStorageEnergy
  BuildMinGenCap.csv           (NEW_GEN_WITH_MIN_BUILD_YEARS_1, _2)  -> BuildMinGenCap
  CommitGenUnits.csv           (DISCRETE_GEN_TPS_1, _2)              -> CommitGenUnits
  GenIsCommitted.csv           (varies)                              -> GenIsCommitted
  RFMBuildSupplyTier.csv       (varies)                              -> RFMBuildSupplyTier
  BuildAnyLiquidHydrogenTank.csv                                     -> BuildAnyLiquidHydrogenTank

For the cplexamp / NL-file interface, MIP start is consumed via the
initial variable values that Pyomo's NL writer writes into the .nl file.
CPLEX-AMPL reads them when its `mipstart` option is enabled (default: auto).
No warmstart=True kwarg is needed (and would be rejected by ProblemWriter_nl).
"""
import csv
import os


def define_arguments(argparser):
    argparser.add_argument(
        "--warmstart-from",
        dest="warmstart_from",
        default=None,
        help="Path to outputs dir of a prior solve to use as MIP start.",
    )


# (csv filename, var attribute, n_index_cols)
SEED_FILES = [
    ("BuildGen.csv",                   "BuildGen",                   2),
    ("BuildUnits.csv",                 "BuildUnits",                 2),
    ("BuildStorageEnergy.csv",         "BuildStorageEnergy",         2),
    ("BuildMinGenCap.csv",             "BuildMinGenCap",             2),
    ("CommitGenUnits.csv",             "CommitGenUnits",             2),
    ("GenIsCommitted.csv",             "GenIsCommitted",             2),
    ("RFMBuildSupplyTier.csv",         "RFMBuildSupplyTier",         3),
    ("BuildAnyLiquidHydrogenTank.csv", "BuildAnyLiquidHydrogenTank", 2),
]


def _coerce_key(parts):
    """Try int first (years, timepoints), fall back to original string."""
    out = []
    for p in parts:
        try:
            out.append(int(p))
        except ValueError:
            out.append(p)
    return tuple(out) if len(out) > 1 else out[0]


def _seed_var(m, csv_path, var_name, n_index_cols):
    var = getattr(m, var_name, None)
    if var is None:
        return 0, 0
    if not os.path.exists(csv_path):
        return 0, 0
    set_n = 0
    skip_n = 0
    with open(csv_path) as f:
        reader = csv.reader(f)
        header = next(reader)
        # Last column is the value
        for row in reader:
            if not row or len(row) < n_index_cols + 1:
                continue
            key = _coerce_key(row[:n_index_cols])
            try:
                val = float(row[-1])
            except ValueError:
                skip_n += 1
                continue
            try:
                v = var[key]
            except KeyError:
                skip_n += 1
                continue
            try:
                v.set_value(val, skip_validation=True)
                set_n += 1
            except Exception:
                skip_n += 1
    return set_n, skip_n


def pre_solve(m):
    src = getattr(m.options, "warmstart_from", None)
    if not src:
        return
    if not os.path.isdir(src):
        print(f"[warm_start] WARNING: --warmstart-from {src!r} not found; skipping.")
        return

    print(f"[warm_start] Seeding initial values from {src}")
    total_set = 0
    total_skip = 0
    for fname, vname, ncols in SEED_FILES:
        path = os.path.join(src, fname)
        s, k = _seed_var(m, path, vname, ncols)
        if s or k:
            print(f"[warm_start]   {vname:30s}  set={s:6d}  skipped={k}")
        total_set += s
        total_skip += k

    print(f"[warm_start] Total values set: {total_set}  (skipped: {total_skip})")
    print("[warm_start] Initial values will be written into .nl file; "
          "cplexamp consumes them as MIP start when mipstart!=0.")
