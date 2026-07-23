"""Force construction of 500 MW (4 x 125 MW) Oahu_LSFO_CCGT in 2030 period.
Upper-bound sizing for the LSFO sister plant — equivalent to the proposed
JERA LNG plant size.
"""
from pyomo.environ import Constraint


def define_components(m):
    m.Force_LSFO_CCGT_500_2030 = Constraint(
        rule=lambda m: m.BuildGen["Oahu_LSFO_CCGT", 2030] == 500
    )
    print("Forcing 500 MW (4x125) Oahu_LSFO_CCGT to be built in 2030.")
