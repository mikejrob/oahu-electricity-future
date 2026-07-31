"""
Enhanced Geothermal System (EGS) module for Switch-Hawaii.

This module makes Enhanced Geothermal System resources available to the
Switch capacity-expansion model as a baseload, non-fuel, low-marginal-cost
generation option. EGS extracts heat from hot dry rock using engineered
fluid pathways. Unlike conventional geothermal, EGS does not require
naturally permeable reservoirs — it creates them by hydraulic stimulation
or thermal cracking. This makes EGS feasible in places (like Oahu) where
conventional geothermal isn't.

The EGS project (Oahu_EGS) is defined in `generation_projects_info.csv`
with the following key fields:

  - gen_tech: EGS
  - gen_energy_source: Geothermal (in `non_fuel_energy_sources.csv`)
  - gen_is_baseload: 1            (operates at constant output when committed)
  - gen_is_variable: 0            (not weather-dependent)
  - gen_capacity_limit_mw: 100    (conservative Oahu EGS potential per NREL reV)
  - gen_unit_size: 25 MW          (modular EGS plant — typical commercial unit)
  - gen_max_age: 30
  - gen_scheduled_outage_rate: 0.05  (well maintenance ~3 weeks/year)
  - gen_forced_outage_rate: 0.02

Three cost scenarios are supplied via `--input-alias`:

  - gen_build_costs.csv             (Reference / Moderate, ATB 2024)
  - gen_build_costs_egs_low.csv     (Advanced / Low, DOE GeoVision targets met)
  - gen_build_costs_egs_high.csv    (Conservative / High, today's tech)

Cost data is taken from NREL ATB 2024 NF-EGS Binary and Deep EGS Binary
categories, in 2027 USD (the model's base financial year). Hawaii-specific
Fixed O&M ($270–333/kW-yr) reflects island isolation costs (mainland EGS
typically $135–200/kW-yr). Resource assessment uses NREL's reV model: 11
developable EGS sites on Oahu totaling 104.2 MW at 2.5 km depth, capped
to 100 MW in the model.

Why EGS deserves explicit modeling here:
  Conventional capacity-expansion treatment of "generic geothermal" is
  inadequate for Oahu because (a) commercial Oahu EGS is at the
  technology-demonstration stage; the cost trajectory matters, (b) the
  resource is bounded (~100 MW), so saturation behavior is important to
  the model's substitution decisions, and (c) EGS capital is highly
  uncertain — the user may want to run scenarios where EGS is forced
  available at different cost levels.

References:
  - NREL ATB 2024 (geothermal): https://atb.nrel.gov/electricity/2024/geothermal
  - NREL GDR EGS Hawaii data: https://gdr.openei.org/submissions/1702
  - DOE GeoVision Report (2019): https://www.energy.gov/eere/geothermal/geovision

Module behavior:
  This module imposes no constraints by default. The EGS project, costs,
  and outage rates are all carried by the standard Switch input files.
  The module exists to:
    1. Provide CLI arguments that let the user override capacity or
       earliest-build-period without editing input CSVs.
    2. Centralize EGS-specific assumptions and references for
       reproducibility.
    3. Serve as the natural place to add future EGS-specific
       constraints (e.g., ramp limits, flexible vs baseload modes,
       site-specific capacity, well-decline schedules).
"""

from pyomo.environ import Constraint


def define_arguments(argparser):
    """
    --egs-max-capacity:
        Override the maximum installed Oahu EGS capacity (MW). If unset,
        the model uses gen_capacity_limit_mw from
        generation_projects_info.csv (100 MW). Useful for scenarios that
        test sensitivity to the conservative 104.2 MW NREL reV resource
        estimate.

    --egs-earliest-period:
        Earliest investment period in which EGS can be built. If unset,
        EGS may be built in any period (subject to the standard
        gen_build_predetermined.csv predetermined-build constraints).
        Useful for scenarios that delay EGS until commercial demonstration
        is mature (e.g., 2035 instead of 2027).
    """
    argparser.add_argument(
        "--egs-max-capacity",
        type=float,
        default=None,
        help="Override the maximum Oahu_EGS capacity (MW). Defaults to "
        "gen_capacity_limit_mw in generation_projects_info.csv (100 MW).",
    )
    argparser.add_argument(
        "--egs-earliest-period",
        type=int,
        default=None,
        help="Earliest investment period in which Oahu_EGS can be built "
        "(integer year, e.g. 2035). Defaults to allowing builds in any period.",
    )


def define_components(m):
    """
    Apply optional Oahu_EGS sizing and timing constraints when the
    corresponding command-line arguments are supplied. Otherwise the
    module is a no-op and EGS is governed entirely by the standard
    Switch generation-project inputs.

    Both constraints `Constraint.Skip` if Oahu_EGS is not in
    GENERATION_PROJECTS (e.g., when running a scenario that omits the
    EGS project from the input files).
    """

    if m.options.egs_max_capacity is not None:
        # Override capacity ceiling. The default
        # gen_capacity_limit_mw=100 in gen_info.csv already binds; this
        # provides a way to study tighter or looser caps without editing
        # the input file.
        limit = m.options.egs_max_capacity

        def EGS_Capacity_Limit_rule(m, p):
            if "Oahu_EGS" not in m.GENERATION_PROJECTS:
                return Constraint.Skip
            if ("Oahu_EGS", p) not in m.GEN_BLD_YRS:
                return Constraint.Skip
            return m.GenCapacity["Oahu_EGS", p] <= limit

        m.EGS_Capacity_Limit = Constraint(m.PERIODS, rule=EGS_Capacity_Limit_rule)
        print(f"EGS capacity limited to {limit} MW via --egs-max-capacity")

    if m.options.egs_earliest_period is not None:
        # Force BuildGen[Oahu_EGS, p] = 0 for periods before the
        # specified year. Useful for delayed-commercialization scenarios.
        earliest = m.options.egs_earliest_period

        def No_Early_EGS_rule(m, p):
            if "Oahu_EGS" not in m.GENERATION_PROJECTS:
                return Constraint.Skip
            if ("Oahu_EGS", p) not in m.GEN_BLD_YRS:
                return Constraint.Skip
            if p < earliest:
                return m.BuildGen["Oahu_EGS", p] == 0
            return Constraint.Skip

        m.No_Early_EGS = Constraint(m.PERIODS, rule=No_Early_EGS_rule)
        print(f"EGS construction blocked before period {earliest}")
