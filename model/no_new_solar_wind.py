"""Freeze solar and wind capacity at what already exists or is contracted.

The "procurement stops" counterfactual: no new solar (utility-scale or
distributed) and no new wind may be built beyond each project's
predetermined capacity. Everything else stays optimized — storage,
geothermal, biofuel, and the existing thermal fleet — so the resulting
system cost is a LOWER bound on what halting solar and wind procurement
would cost.

This is the analogue of Hawaiian Electric's IGP "Status Quo" scenario,
which carries the base rooftop/efficiency/EV forecast and the already
contracted Stage 1, Stage 2 and CBRE Phase 2 Tranche 1 projects, assumes
existing IPP contracts are renegotiated and continue, keeps most existing
thermal units running, and excludes every future resource the capacity
expansion model would have selected (IGP Report May 2023, Sections 8.1.3
and 8.2.3.1; vendored at sources/plan_mix/IGP_Report_May-2023.pdf).

Differences from that scenario, all stated so the comparison is not
oversold: our contracted-project list is the model's predetermined build,
not the utility's project roster; storage and geothermal remain free here
where the IGP scenario has neither; and we report system resource cost
where the IGP reports revenue requirement.

Use with --rps-deactivate: the clean-energy mandate cannot be met with
solar and wind frozen, so leaving the RPS active is infeasible.
"""
from pyomo.environ import Constraint

FROZEN_SOURCES = {"SUN", "WND"}


def define_components(m):
    # Cap total capacity at the predetermined level for every solar and wind
    # project. gen_pre_existing_capacity (hawaii.rps) is capacity in the first
    # period net of anything built in it, i.e. the contracted/legacy stock.
    m.No_New_Solar_Wind = Constraint(
        m.NEW_GEN_BLD_YRS,
        rule=lambda m, g, bld_yr: (
            m.GenCapacity[g, bld_yr] <= m.gen_pre_existing_capacity[g]
        )
        if m.gen_energy_source[g] in FROZEN_SOURCES
        else Constraint.Skip,
    )
