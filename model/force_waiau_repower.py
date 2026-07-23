"""Force construction of 252 MW (6 x 42 MW) Waiau Repower in 2030 period."""

from pyomo.environ import Constraint


def define_components(m):
    m.Force_Waiau_Repower_2030 = Constraint(
        rule=lambda m: m.BuildGen["Oahu_Waiau_Repower", 2030] == 252
    )
    print("Forcing 252 MW (6x42) Waiau Repower to be built in 2030.")
