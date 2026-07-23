from pyomo.environ import Constraint

# Force construction of exactly 500 MW of Oahu_JERA in the 2030 period.
# Oahu_JERA has gen_unit_size=125 MW, so this equals 4 discrete units.
# Also force at least 1 of those 4 units to run on LNG and dispatch >= 125 MW
# at each timepoint where the LNG supply tier is active.

def define_components(m):
    m.Force_JERA_2030 = Constraint(
        rule=lambda m: m.BuildGen["Oahu_JERA", 2030] == 500
    )
    print("Forcing 500 MW of Oahu_JERA to be built in 2030.")

    # def _jera_lng_active(m, t):
    #     """Return True if the LNG tier is forced on for timepoint t's period."""
    #     opt = m.options.force_lng_tier
    #     if opt is None or opt[0].lower() == "none":
    #         return False
    #     lng_start = float(opt[1]) if len(opt) > 1 else m.PERIODS.first()
    #     lng_end = float(opt[2]) if len(opt) > 2 else m.PERIODS.last()
    #     return lng_start <= m.tp_period[t] <= lng_end

    # # Require that at least 1 of 4 JERA units uses LNG at each timepoint where the
    # # LNG supply tier is active. The active period range is read from --force-lng-tier
    # # (e.g. "bulk_15 2030 2044"); if no range is specified, defaults to all periods.
    # # Expressed as: LNG fuel use rate >= 1/4 of total fuel use rate across all fuels.
    # # LNG_GEN_TIMEPOINTS is defined by switch_model.hawaii.lng_conversion.
    # def Min_JERA_LNG_rule(m, g, t):
    #     if g != "Oahu_JERA" or not _jera_lng_active(m, t):
    #         return Constraint.Skip
    #     return (
    #         4 * m.GenFuelUseRate[g, t, "LNG"]
    #         >= sum(m.GenFuelUseRate[g, t, f] for f in m.FUELS_FOR_GEN[g])
    #     )

    # m.Min_JERA_LNG = Constraint(m.LNG_GEN_TIMEPOINTS, rule=Min_JERA_LNG_rule)
    # print("Forcing at least 1 of 4 Oahu_JERA units to run on LNG at each operating timepoint.")

    # # Require JERA to dispatch at least 1/4 of its installed capacity (125 MW = 1 unit)
    # # at each timepoint where the LNG supply tier is active.
    # def Min_JERA_Dispatch_rule(m, t):
    #     if ("Oahu_JERA", t) not in m.GEN_TPS or not _jera_lng_active(m, t):
    #         return Constraint.Skip
    #     return m.DispatchGen["Oahu_JERA", t] >= m.gen_unit_size["Oahu_JERA"]

    # m.Min_JERA_Dispatch = Constraint(m.TIMEPOINTS, rule=Min_JERA_Dispatch_rule)
    # print("Forcing Oahu_JERA to dispatch at least 125 MW (1 unit) at each operating timepoint.")
