"""Block all EGS construction for baseline comparison runs."""

from pyomo.environ import Constraint


def define_components(m):
    def No_EGS_rule(m, p):
        if "Oahu_EGS" not in m.GENERATION_PROJECTS:
            return Constraint.Skip
        if ("Oahu_EGS", p) not in m.GEN_BLD_YRS:
            return Constraint.Skip
        return m.BuildGen["Oahu_EGS", p] == 0

    m.No_EGS = Constraint(m.PERIODS, rule=No_EGS_rule)
    print("EGS construction blocked (baseline scenario).")
