"""Boss definitions and data structure."""

from attacks import Attack


class Boss:
    """Represents a boss enemy."""

    def __init__(self, name, level, hp, attacks, art="",
                 intro_quote="", defeat_quote=""):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.attacks = attacks
        self.art = art
        self.intro_quote = intro_quote
        self.defeat_quote = defeat_quote

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def __str__(self):
        return f"{self.name} (Lv.{self.level})"


# Boss database with intro and defeat quotes
def get_all_bosses():
    """Return a list of all available bosses."""
    return [
        # ── Easy ──
        Boss(
            name="Homework Pile",
            level=2,
            hp=40,
            attacks=[
                Attack("Paper Cut", 6, 90, description="Death by a thousand pages"),
                Attack("Overwhelm", 10, 70, description="It just keeps piling up..."),
            ],
            intro_quote="You thought you could ignore me?",
            defeat_quote="I'll be back... next semester.",
        ),
        Boss(
            name="Alarm Clock",
            level=3,
            hp=60,
            attacks=[
                Attack("Snooze Trap", 8, 85, description="Just 5 more minutes..."),
                Attack("Ear-Splitting Ring", 12, 90, description="BRRRING BRRRING!"),
            ],
            intro_quote="BRRRING! Time to suffer!",
            defeat_quote="Fine... sleep in. See what happens.",
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
            intro_quote="The weekend is OVER. Back to reality.",
            defeat_quote="You won this battle... but I'll see you in 7 days.",
        ),
        Boss(
            name="Pop Quiz",
            level=7,
            hp=90,
            attacks=[
                Attack("Surprise!", 14, 85, description="I didn't know we had a quiz!"),
                Attack("Trick Answer", 18, 65, description="Wait, that's not even an option"),
                Attack("Time's Up", 10, 95, description="Pencils down!"),
            ],
            intro_quote="SURPRISE! Did you study? Of course not.",
            defeat_quote="Lucky guess... but next time won't be so easy.",
        ),
        # ── Medium ──
        Boss(
            name="Alarm Clock II",
            level=10,
            hp=120,
            attacks=[
                Attack("Double Alarm", 16, 90, description="Two alarms, no mercy"),
                Attack("Snooze Paradox", 22, 75, description="You snoozed... but at what cost?"),
                Attack("4 AM Wakeup", 18, 85, description="Why did you set this?"),
            ],
            intro_quote="ONE alarm wasn't enough? Now face TWO!",
            defeat_quote="Broken but not forgotten... your phone has backup alarms.",
        ),
        Boss(
            name="Procrastination",
            level=12,
            hp=160,
            attacks=[
                Attack("Just One More Video", 20, 85, description="3 hours later..."),
                Attack("Infinite Scroll", 15, 95, description="You can't stop scrolling"),
                Attack("Tomorrow's Problem", 28, 60, description="Future you can handle it"),
            ],
            intro_quote="Why do today what you can put off forever?",
            defeat_quote="Fine, be productive... for now.",
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
            intro_quote="Hope you studied... just kidding, I know you didn't.",
            defeat_quote="Passed... barely. See you at retakes.",
        ),
        Boss(
            name="Monday Morning II",
            level=16,
            hp=210,
            attacks=[
                Attack("Monday After Break", 25, 85, description="Back to reality..."),
                Attack("Rain Commute", 18, 90, description="Forgot your umbrella"),
                Attack("Broken Coffee Machine", 30, 65, description="NO. NOT TODAY."),
            ],
            intro_quote="Back from break? Ha! The suffering doubles.",
            defeat_quote="Congratulations. Only 4 more days until Friday.",
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
            intro_quote="Tick tock... your time is running out.",
            defeat_quote="Submitted... one minute before midnight. Well played.",
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
            intro_quote="Welcome to teamwork... where YOU do all the work.",
            defeat_quote="Finally over. Never. Again.",
        ),
        Boss(
            name="Thesis",
            level=22,
            hp=280,
            attacks=[
                Attack("Writer's Block", 28, 90, description="The cursor just blinks..."),
                Attack("Advisor Feedback", 35, 75, description="Needs major revisions"),
                Attack("Citation Needed", 22, 95, description="[citation needed] [citation needed]"),
            ],
            intro_quote="Chapter 1... after 6 months? Impressive.",
            defeat_quote="Draft submitted. Only 47 revisions to go.",
        ),
        Boss(
            name="Final Exam II",
            level=25,
            hp=320,
            attacks=[
                Attack("Cumulative Final", 45, 80, description="Everything from day one"),
                Attack("Wrong Room", 30, 90, description="This isn't your exam"),
                Attack("Essay Question", 50, 55, description="Explain everything in detail"),
            ],
            intro_quote="Remember everything from the semester? No? Good luck.",
            defeat_quote="How did you... never mind. Graduation awaits.",
        ),
        Boss(
            name="Deadline II",
            level=28,
            hp=350,
            attacks=[
                Attack("Multiple Deadlines", 40, 85, description="They're ALL due today"),
                Attack("Server Crash", 30, 90, description="Submission portal is down!"),
                Attack("Late by 1 Minute", 55, 45, description="The system says 12:01 AM"),
            ],
            intro_quote="Not one deadline... ALL of them. Today.",
            defeat_quote="All submitted. Your calendar can breathe again.",
        ),
        # ── Secret ──
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
            intro_quote="Tell me about yourself. You have 30 seconds.",
            defeat_quote="We'll be in touch... actually, you're hired!",
        ),
        Boss(
            name="Group Project II",
            level=32,
            hp=420,
            attacks=[
                Attack("Last-Minute Changes", 40, 85, description="Can we redo the whole thing?"),
                Attack("Conflicting Schedules", 25, 95, description="Nobody can meet"),
                Attack("Presentation Disaster", 50, 65, description="The slides won't load"),
                Attack("Free Rider", 35, 80, description="I'll just put my name on it"),
            ],
            intro_quote="Remember your last group project? This is worse.",
            defeat_quote="Somehow, you all got A's. Don't ask how.",
        ),
        Boss(
            name="Student Loans",
            level=35,
            hp=500,
            attacks=[
                Attack("Interest Rate", 30, 95, description="It's compounding..."),
                Attack("Payment Due", 45, 80, description="Your balance is $..."),
                Attack("Deferment Denied", 40, 85, description="Request rejected"),
                Attack("Reality Check", 60, 40, description="This is what you owe"),
            ],
            intro_quote="You thought graduation was the end? I am eternal.",
            defeat_quote="Paid off... in 30 years. Freedom at last!",
        ),
    ]
