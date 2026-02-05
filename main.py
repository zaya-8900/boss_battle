"""Boss Battle Simulator: Life Edition - Main game loop."""

from display import draw_box, draw_title_screen, draw_hp_bar
from player import Player
from bosses import get_all_bosses
from attacks import PLAYER_ATTACKS
from combat import battle, survival_battle


def show_main_menu(player):
    """Display the main menu and return the user's choice."""
    draw_box(
        "⚔️  MAIN MENU ⚔️",
        [
            "",
            "[1] ⚔️   Quick Battle (Random Boss)",
            "[2] 🎯  Choose Your Boss",
            "[3] 🧙  View Character Stats",
            "[4] 🏆  Victory Log",
            "[5] ❓  How to Play",
            "[6] 💀  Survival Mode",
            "[7] 🚪  Exit to Reality",
            "",
            f"Player: {player.name}   Lv.{player.level}   "
            f"W:{player.wins} L:{player.losses}",
            "",
        ],
    )
    return input("Enter choice: ").strip()


def quick_battle(player):
    """Start a battle with a random boss."""
    import random
    bosses = get_all_bosses()
    boss = random.choice(bosses)
    player.restore_for_battle()
    print(f"\n  A wild {boss.name} (Lv.{boss.level}) appeared!")
    battle(player, boss, PLAYER_ATTACKS)
    player.save()
    print("  💾 Progress saved!")


def choose_boss(player):
    """Let the player pick a boss to fight."""
    bosses = get_all_bosses()
    lines = [
        "",
        "  EASY",
        "  ────",
    ]
    for i, boss in enumerate(bosses, 1):
        # Add section headers
        if boss.level == 15 and lines[-1] != "  MEDIUM":
            lines.append("")
            lines.append("  MEDIUM")
            lines.append("  ──────")
        elif boss.level == 20 and lines[-1] != "  HARD":
            lines.append("")
            lines.append("  HARD")
            lines.append("  ────")
        elif boss.level >= 30 and "SECRET" not in lines[-1]:
            lines.append("")
            lines.append("  SECRET")
            lines.append("  ──────")

        defeated = " ✓" if boss.name in player.bosses_defeated else ""
        lines.append(f"  [{i}] {boss.name} (Lv.{boss.level}, HP:{boss.hp}){defeated}")

    lines.append("")
    lines.append("[M] Back to Menu")
    lines.append("")

    draw_box("🎯 CHOOSE YOUR OPPONENT", lines)
    choice = input("Enter choice: ").strip().lower()

    if choice == "m":
        return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(bosses):
            boss = bosses[idx]
            player.restore_for_battle()
            print(f"\n  You challenge {boss.name}!")
            battle(player, boss, PLAYER_ATTACKS)
            player.save()
            print("  💾 Progress saved!")
        else:
            print("  Invalid choice.")
    except ValueError:
        print("  Invalid choice.")


def view_stats(player):
    """Display current player stats."""
    xp_bar = draw_hp_bar(player.xp, player.xp_to_next_level(), length=15)
    win_rate = (
        f"{player.wins / (player.wins + player.losses) * 100:.0f}%"
        if (player.wins + player.losses) > 0
        else "N/A"
    )
    total_bosses = len(get_all_bosses())
    defeated_count = len(player.bosses_defeated)

    draw_box(
        "🧙 CHARACTER STATS",
        [
            "",
            f"Name:  {player.name}",
            f"Level: {player.level}",
            f"XP:    {xp_bar}",
            "",
            f"Max HP:     {player.max_hp}",
            f"Max Energy: {player.max_energy}",
            f"Max Sanity: {player.max_sanity}",
            "",
            f"Victories: {player.wins}",
            f"Defeats:   {player.losses}",
            f"Win Rate:  {win_rate}",
            f"Bosses:    {defeated_count}/{total_bosses} defeated",
            "",
        ],
    )
    input("Press Enter to continue...")


def view_victory_log(player):
    """Display list of defeated bosses."""
    all_bosses = get_all_bosses()
    total = len(all_bosses)
    defeated_count = len(player.bosses_defeated)

    lines = [""]
    for boss in all_bosses:
        if boss.name in player.bosses_defeated:
            lines.append(f"  ✓ {boss.name} (Lv.{boss.level})")
        else:
            lines.append(f"  ✗ {boss.name} (Lv.{boss.level}) - NOT DEFEATED")
    lines.append("")
    lines.append(f"  Progress: {defeated_count}/{total} bosses defeated")
    if defeated_count == total:
        lines.append("  🌟 ALL BOSSES DEFEATED! YOU ARE THE CHAMPION! 🌟")
    lines.append("")

    draw_box("🏆 VICTORY LOG", lines)
    input("Press Enter to continue...")


def survival_mode(player):
    """Start survival mode — endless boss waves until defeat."""
    bosses = get_all_bosses()
    player.restore_for_battle()
    waves, total_xp = survival_battle(player, bosses, PLAYER_ATTACKS)
    player.save()
    print("  💾 Progress saved!")
    input("  Press Enter to continue...")


def show_help():
    """Display how to play instructions."""
    draw_box(
        "❓ HOW TO PLAY",
        [
            "",
            "GOAL: Defeat all 6 bosses!",
            "",
            "BATTLE:",
            "  - Pick an attack each turn",
            "  - Attacks cost Energy and/or Sanity",
            "  - Boss attacks back each turn",
            "  - If HP reaches 0, you lose",
            "  - If Sanity reaches 0, you take extra damage",
            "",
            "ATTACKS:",
            "  Educated Guess - Free but weak (40% hit)",
            "  Actually Study - Strong, costs Energy",
            "  Caffeine Rush  - Restores Energy, costs Sanity",
            "  Cry            - Restores Sanity, weak damage",
            "  Procrastinate  - Skip turn, big Energy restore",
            "  All-Nighter    - Massive damage, huge cost",
            "",
            "TIPS:",
            "  - Manage Energy and Sanity carefully!",
            "  - Use Cry and Procrastinate to recover",
            "  - Level up to increase your max stats",
            "  - XP gained = Boss Level x 20",
            "",
        ],
    )
    input("Press Enter to continue...")


def main():
    """Main game loop."""
    draw_title_screen()
    print("\n  Welcome, brave student!")
    name = input("  Enter your name: ").strip()
    if not name:
        name = "Student"

    # Load saved progress or create new player
    player = Player.load(name)

    if player.level > 1 or player.wins > 0:
        print(f"\n  💾 Save data loaded!")
        print(f"  Welcome back, {player.name}! (Lv.{player.level}, {player.wins} wins)")
    else:
        print(f"\n  New adventure started for {player.name}!")
        player.save()

    while True:
        choice = show_main_menu(player)

        if choice == "1":
            quick_battle(player)
        elif choice == "2":
            choose_boss(player)
        elif choice == "3":
            view_stats(player)
        elif choice == "4":
            view_victory_log(player)
        elif choice == "5":
            show_help()
        elif choice == "6":
            survival_mode(player)
        elif choice == "7":
            player.save()
            print("\n  💾 Progress saved!")
            print("  You escaped back to reality... for now. 👋\n")
            break
        else:
            print("  Invalid choice. Try again.")


if __name__ == "__main__":
    main()
