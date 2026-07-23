"""Force construction of 375 MW (3 x 125 MW) Oahu_JERA in 2030 period.

This is the smaller-plant LNG variant (vs the 500 MW assumption in
force_jera_2030.py). Per the JERA proposal, the firm-flexible role can be
served by a 375 MW H-class CCGT — sized below the 500 MW initial proposal.
Pairs with --force-lng-tier to require LNG dispatch when active.
"""
from pyomo.environ import Constraint


def define_components(m):
    m.Force_JERA_375_2030 = Constraint(
        rule=lambda m: m.BuildGen["Oahu_JERA", 2030] == 375
    )
    print("Forcing 375 MW (3x125) of Oahu_JERA to be built in 2030.")
