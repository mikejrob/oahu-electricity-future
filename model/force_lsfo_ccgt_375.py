"""Force construction of 375 MW (3 x 125 MW) Oahu_LSFO_CCGT in 2030 period.

Used in scenarios that test the LSFO sister-plant alternative to LNG: a 375 MW
F-class CCGT burning HECO's existing LSFO supply (with biodiesel and diesel as
secondary fuels), avoiding the LNG terminal infrastructure and contract risk.
See LSFO_INVESTIGATION.md for technical detail and cost basis.
"""
from pyomo.environ import Constraint


def define_components(m):
    m.Force_LSFO_CCGT_2030 = Constraint(
        rule=lambda m: m.BuildGen["Oahu_LSFO_CCGT", 2030] == 375
    )
    print("Forcing 375 MW (3x125) Oahu_LSFO_CCGT to be built in 2030.")
