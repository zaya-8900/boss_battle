"""Boss definitions and data structure."""

from attacks import Attack


class Boss:
    """Represents a boss enemy."""

    def __init__(self, name, level, hp, attacks, art=""):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.attacks = attacks
        self.art = art

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def __str__(self):
        return f"{self.name} (Lv.{self.level})"


# Boss database
def get_all_bosses():
    """Return a list of all available bosses."""
    return [
        Boss(
            name="Monday Morning",
            level=5,
            hp=80,
            attacks=[
                Attack("Alarm Blare", 10, 90, description="BEEP BEEP BEEP"),
                Attack("Snooze Temptation", 15, 70, description="Just 5 more minutes..."),
            ],
        ),
        Boss(
            name="Final Exam",
            level=15,
            hp=200,
            attacks=[
                Attack("Question You Didn't Study", 35, 80, description="This wasn't in the slides!"),
                Attack("Time Pressure", 20, 90, description="30 minutes remaining..."),
                Attack("Trick Question", 25, 60, description="All of the above?"),
            ],
        ),
        Boss(
            name="Group Project",
            level=20,
            hp=250,
            attacks=[
                Attack("Ghost Member", 30, 85, description="Someone disappeared again"),
                Attack("Night-Before Panic", 40, 70, description="We present TOMORROW?!"),
                Attack("Unequal Work", 20, 95, description="I did everything..."),
            ],
        ),
    ]
