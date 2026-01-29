"""Player data structure, stats management, and save/load persistence."""

import json
import os

SAVE_PATH = os.path.join(os.path.dirname(__file__), "data", "save.json")


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
        self.bosses_defeated = []  # list of boss names defeated

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

    def xp_to_next_level(self):
        """XP needed to reach the next level."""
        return self.level * 100

    def gain_xp(self, amount):
        """Add XP and check for level ups. Returns True if leveled up."""
        self.xp += amount
        leveled_up = False

        while self.xp >= self.xp_to_next_level():
            self.xp -= self.xp_to_next_level()
            self.level += 1
            self.max_hp += 10
            self.max_energy += 5
            self.max_sanity += 5
            leveled_up = True

        return leveled_up

    def record_victory(self, boss_name):
        """Record a boss defeat."""
        if boss_name not in self.bosses_defeated:
            self.bosses_defeated.append(boss_name)

    # ── Save / Load ──────────────────────────────────────────

    def save(self):
        """Save player data to JSON file."""
        data = {
            "name": self.name,
            "level": self.level,
            "xp": self.xp,
            "max_hp": self.max_hp,
            "max_energy": self.max_energy,
            "max_sanity": self.max_sanity,
            "wins": self.wins,
            "losses": self.losses,
            "bosses_defeated": self.bosses_defeated,
        }
        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
        with open(SAVE_PATH, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, name):
        """Load player data from JSON. Returns existing player or new one."""
        if not os.path.exists(SAVE_PATH):
            return cls(name)

        try:
            with open(SAVE_PATH, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError):
            return cls(name)

        # Only load if the save matches the player name
        if not data or data.get("name") != name:
            return cls(name)

        player = cls(data["name"])
        player.level = data.get("level", 1)
        player.xp = data.get("xp", 0)
        player.max_hp = data.get("max_hp", 100)
        player.max_energy = data.get("max_energy", 100)
        player.max_sanity = data.get("max_sanity", 100)
        player.wins = data.get("wins", 0)
        player.losses = data.get("losses", 0)
        player.bosses_defeated = data.get("bosses_defeated", [])

        # Restore full stats for the session
        player.restore_for_battle()
        return player

    def __str__(self):
        return f"{self.name} (Lv.{self.level})"
