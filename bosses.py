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
        # ── Easy ──
        Boss(
            name="Alarm Clock",
            level=3,
            hp=60,
            attacks=[
                Attack("Snooze Trap", 8, 85, description="Just 5 more minutes..."),
                Attack("Ear-Splitting Ring", 12, 90, description="BRRRING BRRRING!"),
            ],
        ),
        Boss(
            name="Monday Morning",
            level=5,
            hp=80,
            attacks=[
                Attack("Alarm Blare", 10, 90, description="BEEP BEEP BEEP"),
                Attack("Snooze Temptation", 15, 70, description="Just 5 more minutes..."),
                Attack("Weekend Nostalgia", 12, 80, description="Remember Saturday?"),
            ],
        ),
        # ── Medium ──
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
            name="Deadline",
            level=18,
            hp=220,
            attacks=[
                Attack("Due Tomorrow", 30, 85, description="Why didn't you start earlier?"),
                Attack("Clock Tick", 15, 95, description="tick... tock... tick... tock..."),
                Attack("Late Penalty", 40, 50, description="-10% per day! SUBMIT NOW!"),
            ],
        ),
        # ── Hard ──
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
        # ── Secret Boss ──
        Boss(
            name="Job Interview",
            level=30,
            hp=400,
            attacks=[
                Attack("Tell Me About Yourself", 25, 90, description="*mind goes blank*"),
                Attack("Behavioral Question", 35, 80, description="Give an example of a time..."),
                Attack("Salary Negotiation", 30, 75, description="What are your expectations?"),
                Attack("We'll Be In Touch", 50, 40, description="*silence for 3 weeks*"),
            ],
        ),
    ]
