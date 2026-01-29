"""Display helpers for formatting, ASCII art, and UI boxes."""

import time


def draw_box(title, lines):
    """Draw a bordered box with a title and content lines."""
    width = 60
    border = "=" * width
    print(f"\n╔{border}╗")
    print(f"║{title:^{width}}║")
    print(f"╠{border}╣")
    for line in lines:
        print(f"║  {line:<{width - 2}}║")
    print(f"╚{border}╝")


def draw_hp_bar(current, maximum, length=20):
    """Return an HP bar string like: ████████░░░░ 80/100"""
    filled = int((current / maximum) * length) if maximum > 0 else 0
    empty = length - filled
    bar = "█" * filled + "░" * empty
    return f"{bar} {current}/{maximum}"


def draw_title_screen():
    """Display the game title screen."""
    print()
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                                                              ║")
    print("║      ⚔️  BOSS BATTLE SIMULATOR: LIFE EDITION ⚔️               ║")
    print("║                                                              ║")
    print("║               ╔═══════════════════════╗                      ║")
    print("║               ║   _____               ║                      ║")
    print("║               ║  |     |  FIGHT YOUR  ║                      ║")
    print("║               ║  | x_x |  DAILY       ║                      ║")
    print("║               ║  |_____|  DEMONS       ║                      ║")
    print("║               ╚═══════════════════════╝                      ║")
    print("║                                                              ║")
    print("║            [ Press ENTER to begin your fate ]                ║")
    print("║                                                              ║")
    print("╚════════════════════════════════════════════════════════════════╝")


def draw_victory():
    """Display the victory screen."""
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║                                        ║")
    print("  ║     ★  ★  ★  ★  ★  ★  ★  ★  ★        ║")
    print("  ║                                        ║")
    print("  ║         🎉  V I C T O R Y !  🎉        ║")
    print("  ║                                        ║")
    print("  ║     ★  ★  ★  ★  ★  ★  ★  ★  ★        ║")
    print("  ║                                        ║")
    print("  ╚════════════════════════════════════════╝")


def draw_defeat():
    """Display the defeat screen."""
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║                                        ║")
    print("  ║            ┌─────────┐                 ║")
    print("  ║            │  R.I.P  │                 ║")
    print("  ║            │  Your   │                 ║")
    print("  ║            │  G.P.A  │                 ║")
    print("  ║            └────┬────┘                 ║")
    print("  ║              ___|___                   ║")
    print("  ║                                        ║")
    print("  ║         💀  D E F E A T E D  💀        ║")
    print("  ║                                        ║")
    print("  ╚════════════════════════════════════════╝")


def draw_boss_entrance(boss_name):
    """Show dramatic boss entrance with ASCII art."""
    art = BOSS_ART.get(boss_name, BOSS_ART["default"])
    print()
    print("  ╔════════════════════════════════════════╗")
    for line in art:
        print(f"  ║  {line:<38}║")
    print("  ╚════════════════════════════════════════╝")


def type_text(text, delay=0.03):
    """Print text with a typing effect."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def draw_attack_hit(damage, critical=False):
    """Show attack impact visual."""
    if critical:
        print("              ╔═══════════════╗")
        print("              ║  ★ CRITICAL   ║")
        print("              ║     HIT! ★    ║")
        print(f"              ║   -{damage} HP!     ║")
        print("              ╚═══════════════╝")
    else:
        print(f"              >>> -{damage} HP! <<<")


def draw_miss():
    """Show miss visual."""
    print("              ~ MISS ~")


def draw_level_up(player):
    """Show level up celebration."""
    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║                                      ║")
    print("  ║     ★  ★  ★  LEVEL UP!  ★  ★  ★     ║")
    print(f"  ║         Now Level {player.level}!{' ' * (18 - len(str(player.level)))}║")
    print("  ║                                      ║")
    print(f"  ║     Max HP:     {player.max_hp}{' ' * (20 - len(str(player.max_hp)))}║")
    print(f"  ║     Max Energy: {player.max_energy}{' ' * (20 - len(str(player.max_energy)))}║")
    print(f"  ║     Max Sanity: {player.max_sanity}{' ' * (20 - len(str(player.max_sanity)))}║")
    print("  ║                                      ║")
    print("  ╚══════════════════════════════════════╝")


def draw_reward_screen(boss_name, xp_gained, player):
    """Show post-battle rewards."""
    remaining = player.xp_to_next_level() - player.xp
    print()
    print("  ┌──────────── REWARDS ────────────┐")
    print(f"  │  💫 +{xp_gained} XP{' ' * (26 - len(str(xp_gained)))}│")
    print(f"  │  📊 XP: {player.xp}/{player.xp_to_next_level()} ({remaining} to next){' ' * max(0, 10 - len(str(remaining)))}│")
    print(f"  │  🏆 Defeated: {boss_name}{' ' * max(0, 17 - len(boss_name))}│")
    print("  └────────────────────────────────┘")


# ── Boss ASCII Art ──────────────────────────────────────────

BOSS_ART = {
    "Monday Morning": [
        "",
        "        ╔═══════════╗",
        "        ║  5:00 AM  ║",
        "        ╚═══════════╝",
        "     BRRRING! BRRRING!",
        "       ┌───────────┐",
        "       │  (╬ಠ益ಠ)  │",
        "       │  zzz...NO │",
        "       └───────────┘",
        "",
    ],
    "Final Exam": [
        "",
        "        ╔═══════════╗",
        "        ║  EXAM DAY ║",
        "        ╚═══════════╝",
        "       ┌───────────┐",
        "       │ Q1: ????? │",
        "       │ Q2: ????? │",
        "       │ Q3: ????? │",
        "       │ TIME: 0:05│",
        "       └───────────┘",
    ],
    "Group Project": [
        "",
        "      ┌─────────────────┐",
        "      │  GROUP PROJECT   │",
        "      │  Due: TOMORROW   │",
        "      ├─────────────────┤",
        "      │ You:     100%   │",
        "      │ Partner: ???    │",
        "      │ Partner: offline│",
        "      │ Partner: lol    │",
        "      └─────────────────┘",
    ],
    "Alarm Clock": [
        "",
        "          .-=========-.  ",
        "          \\'-=======-'/  ",
        "          _|   .=.   |_  ",
        "         ((|  {{0}}  |)) ",
        "          \\|   /|\\   |/  ",
        "           \\__ '`' __/   ",
        "             `'---'`     ",
        "         RING RING RING  ",
        "",
    ],
    "Deadline": [
        "",
        "       ╔═══════════════╗  ",
        "       ║  DUE: TODAY   ║  ",
        "       ║  11:59 PM     ║  ",
        "       ╚═══════════════╝  ",
        "          \\  |  /         ",
        "         -- ⏰ --         ",
        "          /  |  \\         ",
        "        TICK TOCK...      ",
        "",
    ],
    "Job Interview": [
        "",
        "       ┌───────────────┐  ",
        "       │   ┌───────┐   │  ",
        "       │   │ (O)(O)│   │  ",
        "       │   │  ___  │   │  ",
        "       │   │ |   | │   │  ",
        "       │   └───────┘   │  ",
        "       │ 'Tell me about│  ",
        "       │  yourself...' │  ",
        "       └───────────────┘  ",
    ],
    "default": [
        "",
        "       ┌───────────┐",
        "       │           │",
        "       │  (⊙_⊙)   │",
        "       │           │",
        "       │  BOSS!!   │",
        "       │           │",
        "       └───────────┘",
        "",
        "",
    ],
}


def clear_screen():
    """Print some newlines to simulate clearing the screen."""
    print("\n" * 3)
