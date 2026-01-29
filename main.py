"""Boss Battle Simulator: Life Edition - Main game loop."""

from display import draw_box, draw_title_screen, clear_screen
from player import Player
from bosses import get_all_bosses
from attacks import PLAYER_ATTACKS
from combat import battle


def show_main_menu():
    """Display the main menu and return the user's choice."""
    draw_box(
        "⚔️  MAIN MENU ⚔️",
        [
            "",
            "[1] ⚔️   Quick Battle (Random Boss)",
            "[2] 🎯  Choose Your Boss",
            "[3] 🧙  View Character Stats",
            "[4] 🚪  Exit to Reality",
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


def choose_boss(player):
    """Let the player pick a boss to fight."""
    bosses = get_all_bosses()
    lines = [""]
    for i, boss in enumerate(bosses, 1):
        lines.append(f"[{i}] {boss.name} (Lv.{boss.level}, HP:{boss.hp})")
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
        else:
            print("  Invalid choice.")
    except ValueError:
        print("  Invalid choice.")


def view_stats(player):
    """Display current player stats."""
    draw_box(
        "🧙 CHARACTER STATS",
        [
            "",
            f"Name:  {player.name}",
            f"Level: {player.level}",
            f"XP:    {player.xp}",
            "",
            f"Max HP:     {player.max_hp}",
            f"Max Energy: {player.max_energy}",
            f"Max Sanity: {player.max_sanity}",
            "",
            f"Wins:   {player.wins}",
            f"Losses: {player.losses}",
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

    player = Player(name)

    while True:
        choice = show_main_menu()

        if choice == "1":
            quick_battle(player)
        elif choice == "2":
            choose_boss(player)
        elif choice == "3":
            view_stats(player)
        elif choice == "4":
            print("\n  You escaped back to reality... for now. 👋\n")
            break
        else:
            print("  Invalid choice. Try again.")


if __name__ == "__main__":
    main()
