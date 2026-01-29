"""Display helpers for formatting, ASCII art, and UI boxes."""


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
    print("║                     _____                                    ║")
    print("║                    |     |    FIGHT YOUR                     ║")
    print("║                    | x_x |    DAILY DEMONS                   ║")
    print("║                    |_____|                                   ║")
    print("║                                                              ║")
    print("╚════════════════════════════════════════════════════════════════╝")


def draw_victory():
    """Display the victory screen."""
    print()
    print("  ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")
    print("       🎉 VICTORY! 🎉")
    print("  ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")


def draw_defeat():
    """Display the defeat screen."""
    print()
    print("        ┌─────┐")
    print("        │ RIP │")
    print("        │ GPA │")
    print("        └──┬──┘")
    print("         __|__")
    print()
    print("      💀 DEFEATED 💀")


def clear_screen():
    """Print some newlines to simulate clearing the screen."""
    print("\n" * 3)
