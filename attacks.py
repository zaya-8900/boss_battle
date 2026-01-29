"""Attack definitions and data structure."""


class Attack:
    """Represents a single attack move."""

    def __init__(self, name, power, accuracy, energy_cost=0, sanity_cost=0, description=""):
        self.name = name
        self.power = power
        self.accuracy = accuracy       # 0-100 percent chance to hit
        self.energy_cost = energy_cost
        self.sanity_cost = sanity_cost
        self.description = description

    def __str__(self):
        return f"{self.name} (Pwr:{self.power} Acc:{self.accuracy}%)"


# Player attacks
PLAYER_ATTACKS = [
    Attack(
        name="Educated Guess",
        power=15,
        accuracy=40,
        description="Sometimes you get lucky",
    ),
    Attack(
        name="Actually Study",
        power=45,
        accuracy=85,
        energy_cost=20,
        description="Knowledge is power",
    ),
    Attack(
        name="Caffeine Rush",
        power=30,
        accuracy=70,
        energy_cost=-10,  # negative cost = restores energy
        sanity_cost=5,
        description="+10 Energy, -5 Sanity",
    ),
    Attack(
        name="Cry",
        power=5,
        accuracy=100,
        sanity_cost=-10,  # negative cost = restores sanity
        description="Heals 10 Sanity, low damage",
    ),
    Attack(
        name="Procrastinate",
        power=0,
        accuracy=100,
        energy_cost=-30,  # restores 30 energy
        sanity_cost=10,
        description="Skip turn, +30 Energy, -10 Sanity",
    ),
    Attack(
        name="All-Nighter",
        power=80,
        accuracy=60,
        energy_cost=50,
        sanity_cost=20,
        description="Massive damage but drains everything",
    ),
]
