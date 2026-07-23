"""Block all Oahu_JERA construction. Used in scenarios that test paths
without LNG (and explicit JERA infrastructure)."""
from pyomo.environ import Constraint


def define_components(m):
    def No_JERA_rule(m, p):
        if "Oahu_JERA" not in m.GENERATION_PROJECTS:
            return Constraint.Skip
        if ("Oahu_JERA", p) not in m.GEN_BLD_YRS:
            return Constraint.Skip
        return m.BuildGen["Oahu_JERA", p] == 0

    m.Block_JERA = Constraint(m.PERIODS, rule=No_JERA_rule)
    print("Oahu_JERA construction blocked.")
