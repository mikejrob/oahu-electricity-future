"""Block all Oahu_Waiau_Repower construction (counterfactual to PUC approval).
Used in scenarios that test paths where the LSFO sister plant or alternative
fully replaces the simple-cycle Waiau Repower."""
from pyomo.environ import Constraint


def define_components(m):
    def No_Waiau_Repower_rule(m, p):
        if "Oahu_Waiau_Repower" not in m.GENERATION_PROJECTS:
            return Constraint.Skip
        if ("Oahu_Waiau_Repower", p) not in m.GEN_BLD_YRS:
            return Constraint.Skip
        return m.BuildGen["Oahu_Waiau_Repower", p] == 0

    m.Block_Waiau_Repower = Constraint(m.PERIODS, rule=No_Waiau_Repower_rule)
    print("Oahu_Waiau_Repower construction blocked.")
