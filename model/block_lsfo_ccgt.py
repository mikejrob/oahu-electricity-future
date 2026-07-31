"""Block all Oahu_LSFO_CCGT construction. Used in scenarios that test paths
without the LSFO sister-plant option."""
from pyomo.environ import Constraint


def define_components(m):
    def No_LSFO_CCGT_rule(m, p):
        if "Oahu_LSFO_CCGT" not in m.GENERATION_PROJECTS:
            return Constraint.Skip
        if ("Oahu_LSFO_CCGT", p) not in m.GEN_BLD_YRS:
            return Constraint.Skip
        return m.BuildGen["Oahu_LSFO_CCGT", p] == 0

    m.Block_LSFO_CCGT = Constraint(m.PERIODS, rule=No_LSFO_CCGT_rule)
    print("LSFO_CCGT construction blocked.")
