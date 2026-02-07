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


# Boss database — some attacks now carry status effects
def get_all_bosses():
    """Return a list of all available bosses."""
    return [
        # ── Easy ──
        Boss(
            name="Homework Pile",
            level=2,
            hp=40,
            attacks=[
                Attack("Paper Cut", 6, 90, description="Death by a thousand pages",
                       status_effect={"name": "poison", "chance": 15, "damage": 3, "turns": 2}),
                Attack("Overwhelm", 10, 70, description="It just keeps piling up..."),
            ],
        ),
        Boss(
            name="Alarm Clock",
            level=3,
            hp=60,
            attacks=[
                Attack("Snooze Trap", 8, 85, description="Just 5 more minutes...",
                       status_effect={"name": "stun", "chance": 20, "turns": 1}),
                Attack("Ear-Splitting Ring", 12, 90, description="BRRRING BRRRING!"),
            ],
        ),
        Boss(
            name="Monday Morning",
            level=5,
            hp=80,
            attacks=[
                Attack("Alarm Blare", 10, 90, description="BEEP BEEP BEEP",
                       status_effect={"name": "stun", "chance": 15, "turns": 1}),
                Attack("Snooze Temptation", 15, 70, description="Just 5 more minutes..."),
                Attack("Weekend Nostalgia", 12, 80, description="Remember Saturday?",
                       status_effect={"name": "weaken", "chance": 20, "reduction": 0.25, "turns": 2}),
            ],
        ),
        Boss(
            name="Pop Quiz",
            level=7,
            hp=90,
            attacks=[
                Attack("Surprise!", 14, 85, description="I didn't know we had a quiz!",
                       status_effect={"name": "stun", "chance": 25, "turns": 1}),
                Attack("Trick Answer", 18, 65, description="Wait, that's not even an option"),
                Attack("Time's Up", 10, 95, description="Pencils down!"),
            ],
        ),
        # ── Medium ──
        Boss(
            name="Alarm Clock II",
            level=10,
            hp=120,
            attacks=[
                Attack("Double Alarm", 16, 90, description="Two alarms, no mercy",
                       status_effect={"name": "stun", "chance": 20, "turns": 1}),
                Attack("Snooze Paradox", 22, 75, description="You snoozed... but at what cost?"),
                Attack("4 AM Wakeup", 18, 85, description="Why did you set this?"),
            ],
        ),
        Boss(
            name="Procrastination",
            level=12,
            hp=160,
            attacks=[
                Attack("Just One More Video", 20, 85, description="3 hours later...",
                       status_effect={"name": "poison", "chance": 30, "damage": 5, "turns": 3}),
                Attack("Infinite Scroll", 15, 95, description="You can't stop scrolling",
                       status_effect={"name": "stun", "chance": 20, "turns": 1}),
                Attack("Tomorrow's Problem", 28, 60, description="Future you can handle it"),
            ],
        ),
        Boss(
            name="Final Exam",
            level=15,
            hp=200,
            attacks=[
                Attack("Question You Didn't Study", 35, 80, description="This wasn't in the slides!"),
                Attack("Time Pressure", 20, 90, description="30 minutes remaining...",
                       status_effect={"name": "weaken", "chance": 25, "reduction": 0.3, "turns": 2}),
                Attack("Trick Question", 25, 60, description="All of the above?",
                       status_effect={"name": "stun", "chance": 20, "turns": 1}),
            ],
        ),
        Boss(
            name="Monday Morning II",
            level=16,
            hp=210,
            attacks=[
                Attack("Monday After Break", 25, 85, description="Back to reality..."),
                Attack("Rain Commute", 18, 90, description="Forgot your umbrella",
                       status_effect={"name": "poison", "chance": 20, "damage": 5, "turns": 3}),
                Attack("Broken Coffee Machine", 30, 65, description="NO. NOT TODAY.",
                       status_effect={"name": "weaken", "chance": 30, "reduction": 0.3, "turns": 2}),
            ],
        ),
        Boss(
            name="Deadline",
            level=18,
            hp=220,
            attacks=[
                Attack("Due Tomorrow", 30, 85, description="Why didn't you start earlier?"),
                Attack("Clock Tick", 15, 95, description="tick... tock... tick... tock...",
                       status_effect={"name": "poison", "chance": 25, "damage": 5, "turns": 3}),
                Attack("Late Penalty", 40, 50, description="-10% per day! SUBMIT NOW!",
                       status_effect={"name": "weaken", "chance": 30, "reduction": 0.3, "turns": 2}),
            ],
        ),
        # ── Hard ──
        Boss(
            name="Group Project",
            level=20,
            hp=250,
            attacks=[
                Attack("Ghost Member", 30, 85, description="Someone disappeared again",
                       status_effect={"name": "weaken", "chance": 25, "reduction": 0.3, "turns": 2}),
                Attack("Night-Before Panic", 40, 70, description="We present TOMORROW?!",
                       status_effect={"name": "stun", "chance": 15, "turns": 1}),
                Attack("Unequal Work", 20, 95, description="I did everything..."),
            ],
        ),
        Boss(
            name="Thesis",
            level=22,
            hp=280,
            attacks=[
                Attack("Writer's Block", 28, 90, description="The cursor just blinks...",
                       status_effect={"name": "stun", "chance": 25, "turns": 1}),
                Attack("Advisor Feedback", 35, 75, description="Needs major revisions",
                       status_effect={"name": "weaken", "chance": 20, "reduction": 0.3, "turns": 2}),
                Attack("Citation Needed", 22, 95, description="[citation needed] [citation needed]"),
            ],
        ),
        Boss(
            name="Final Exam II",
            level=25,
            hp=320,
            attacks=[
                Attack("Cumulative Final", 45, 80, description="Everything from day one",
                       status_effect={"name": "poison", "chance": 20, "damage": 8, "turns": 3}),
                Attack("Wrong Room", 30, 90, description="This isn't your exam",
                       status_effect={"name": "stun", "chance": 20, "turns": 1}),
                Attack("Essay Question", 50, 55, description="Explain everything in detail"),
            ],
        ),
        Boss(
            name="Deadline II",
            level=28,
            hp=350,
            attacks=[
                Attack("Multiple Deadlines", 40, 85, description="They're ALL due today",
                       status_effect={"name": "poison", "chance": 25, "damage": 7, "turns": 3}),
                Attack("Server Crash", 30, 90, description="Submission portal is down!",
                       status_effect={"name": "stun", "chance": 25, "turns": 1}),
                Attack("Late by 1 Minute", 55, 45, description="The system says 12:01 AM"),
            ],
        ),
        # ── Secret ──
        Boss(
            name="Job Interview",
            level=30,
            hp=400,
            attacks=[
                Attack("Tell Me About Yourself", 25, 90, description="*mind goes blank*",
                       status_effect={"name": "stun", "chance": 30, "turns": 1}),
                Attack("Behavioral Question", 35, 80, description="Give an example of a time..."),
                Attack("Salary Negotiation", 30, 75, description="What are your expectations?",
                       status_effect={"name": "weaken", "chance": 25, "reduction": 0.3, "turns": 2}),
                Attack("We'll Be In Touch", 50, 40, description="*silence for 3 weeks*",
                       status_effect={"name": "poison", "chance": 30, "damage": 8, "turns": 3}),
            ],
        ),
        Boss(
            name="Group Project II",
            level=32,
            hp=420,
            attacks=[
                Attack("Last-Minute Changes", 40, 85, description="Can we redo the whole thing?",
                       status_effect={"name": "weaken", "chance": 25, "reduction": 0.3, "turns": 2}),
                Attack("Conflicting Schedules", 25, 95, description="Nobody can meet"),
                Attack("Presentation Disaster", 50, 65, description="The slides won't load",
                       status_effect={"name": "stun", "chance": 20, "turns": 1}),
                Attack("Free Rider", 35, 80, description="I'll just put my name on it",
                       status_effect={"name": "poison", "chance": 20, "damage": 6, "turns": 3}),
            ],
        ),
        Boss(
            name="Student Loans",
            level=35,
            hp=500,
            attacks=[
                Attack("Interest Rate", 30, 95, description="It's compounding...",
                       status_effect={"name": "poison", "chance": 35, "damage": 10, "turns": 3}),
                Attack("Payment Due", 45, 80, description="Your balance is $..."),
                Attack("Deferment Denied", 40, 85, description="Request rejected",
                       status_effect={"name": "weaken", "chance": 30, "reduction": 0.3, "turns": 2}),
                Attack("Reality Check", 60, 40, description="This is what you owe",
                       status_effect={"name": "stun", "chance": 25, "turns": 1}),
            ],
        ),
    ]
