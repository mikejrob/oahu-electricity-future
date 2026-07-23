"""Force construction of 250 MW (2 x 125 MW) Oahu_LSFO_CCGT in 2030 period.
This is the central-case sizing for the LSFO sister plant per the v2 report.
"""
from pyomo.environ import Constraint


def define_components(m):
    m.Force_LSFO_CCGT_250_2030 = Constraint(
        rule=lambda m: m.BuildGen["Oahu_LSFO_CCGT", 2030] == 250
    )
    print("Forcing 250 MW (2x125) Oahu_LSFO_CCGT to be built in 2030.")
