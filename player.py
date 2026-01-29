"""Player data structure and stats management."""


class Player:
    """Represents the player character."""

    def __init__(self, name="Student"):
        self.name = name
        self.level = 1
        self.xp = 0
        self.max_hp = 100
        self.hp = 100
        self.max_energy = 100
        self.energy = 100
        self.max_sanity = 100
        self.sanity = 100
        self.wins = 0
        self.losses = 0

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def use_energy(self, amount):
        """Use energy. Negative amount restores energy."""
        self.energy = max(0, min(self.max_energy, self.energy - amount))

    def use_sanity(self, amount):
        """Use sanity. Negative amount restores sanity."""
        self.sanity = max(0, min(self.max_sanity, self.sanity - amount))

    def restore_for_battle(self):
        """Restore HP, energy, and sanity before a new battle."""
        self.hp = self.max_hp
        self.energy = self.max_energy
        self.sanity = self.max_sanity

    def __str__(self):
        return f"{self.name} (Lv.{self.level})"
