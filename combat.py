"""Battle logic and combat system."""

import random
import time

from display import draw_box, draw_hp_bar, draw_victory, draw_defeat


def show_battle_status(player, boss):
    """Display current HP/stats for both player and boss."""
    print()
    print(f"  ┌─── {boss.name} (Lv.{boss.level}) ───")
    print(f"  │ HP: {draw_hp_bar(boss.hp, boss.max_hp)}")
    print(f"  └{'─' * 40}")
    print()
    print(f"  ┌─── {player.name} (Lv.{player.level}) ───")
    print(f"  │ HP:     {draw_hp_bar(player.hp, player.max_hp)}")
    print(f"  │ Energy: {draw_hp_bar(player.energy, player.max_energy)}")
    print(f"  │ Sanity: {draw_hp_bar(player.sanity, player.max_sanity)}")
    print(f"  └{'─' * 40}")


def show_attack_menu(player_attacks, player):
    """Display attack options and return chosen attack or None."""
    print()
    print("  ╔═══ CHOOSE YOUR ATTACK ═══╗")
    for i, atk in enumerate(player_attacks, 1):
        cost_info = ""
        if atk.energy_cost > 0:
            cost_info += f" | -{atk.energy_cost} Energy"
        elif atk.energy_cost < 0:
            cost_info += f" | +{-atk.energy_cost} Energy"
        if atk.sanity_cost > 0:
            cost_info += f" | -{atk.sanity_cost} Sanity"
        elif atk.sanity_cost < 0:
            cost_info += f" | +{-atk.sanity_cost} Sanity"

        print(f"  ║ [{i}] {atk.name}")
        print(f"  ║     Pwr:{atk.power}  Acc:{atk.accuracy}%{cost_info}")
        print(f"  ║     \"{atk.description}\"")
    print(f"  ║")
    print(f"  ║ [R] 🏃 Run Away")
    print(f"  ╚{'═' * 28}╝")

    choice = input("  What will you do? ").strip().lower()

    if choice == "r":
        return "run"

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(player_attacks):
            atk = player_attacks[idx]
            # Check if player has enough energy
            if atk.energy_cost > 0 and player.energy < atk.energy_cost:
                print(f"\n  Not enough energy! (Need {atk.energy_cost}, have {player.energy})")
                return None
            if atk.sanity_cost > 0 and player.sanity < atk.sanity_cost:
                print(f"\n  Not enough sanity! (Need {atk.sanity_cost}, have {player.sanity})")
                return None
            return atk
        else:
            print("  Invalid choice.")
            return None
    except ValueError:
        print("  Invalid choice.")
        return None


def player_turn(player, boss, player_attacks):
    """Handle the player's turn. Returns 'run' if player flees, else None."""
    while True:
        result = show_attack_menu(player_attacks, player)

        if result == "run":
            chance = random.randint(1, 100)
            if chance <= 50:
                print("\n  🏃 You successfully ran away!")
                return "run"
            else:
                print("\n  ❌ You tried to run but tripped over your backpack!")
                return None

        if result is None:
            continue

        # Player attacks
        atk = result
        print(f"\n  ⚔️  You used {atk.name}!")
        time.sleep(0.5)

        # Apply costs
        player.use_energy(atk.energy_cost)
        player.use_sanity(atk.sanity_cost)

        # Check accuracy
        hit_roll = random.randint(1, 100)
        if hit_roll <= atk.accuracy:
            # Calculate damage with some randomness
            damage = atk.power + random.randint(-5, 5)
            damage = max(1, damage)

            # Critical hit (10% chance)
            if random.randint(1, 100) <= 10:
                damage *= 2
                print(f"  ★ CRITICAL HIT! ★")
                time.sleep(0.3)

            boss.take_damage(damage)
            print(f"  {boss.name} takes {damage} damage!")
        else:
            print(f"  MISS! {atk.description}")

        time.sleep(0.5)
        return None


def boss_turn(player, boss):
    """Handle the boss's turn."""
    atk = random.choice(boss.attacks)
    print(f"\n  {boss.name} uses {atk.name}!")
    print(f"  \"{atk.description}\"")
    time.sleep(0.5)

    hit_roll = random.randint(1, 100)
    if hit_roll <= atk.accuracy:
        damage = atk.power + random.randint(-3, 3)
        damage = max(1, damage)
        player.take_damage(damage)
        print(f"  You take {damage} damage!")

        # Bosses also drain sanity
        sanity_drain = random.randint(2, 8)
        player.use_sanity(sanity_drain)
        print(f"  Sanity decreased by {sanity_drain}...")
    else:
        print(f"  {boss.name} missed!")

    time.sleep(0.5)


def battle(player, boss, player_attacks):
    """Run a battle between the player and a boss.

    Returns:
        True if player wins, False if player loses.
    """
    print()
    print("=" * 50)
    print(f"  ⚔️  {player.name}  VS  {boss.name} (Lv.{boss.level})  ⚔️")
    print("=" * 50)
    time.sleep(1)

    turn = 1

    while player.is_alive() and boss.is_alive():
        print(f"\n{'─' * 50}")
        print(f"  TURN {turn}")
        print(f"{'─' * 50}")

        show_battle_status(player, boss)

        # Player turn
        result = player_turn(player, boss, player_attacks)
        if result == "run":
            print("\n  You fled the battle!")
            return False

        # Check if boss is defeated
        if not boss.is_alive():
            break

        # Boss turn
        boss_turn(player, boss)

        # Check if player's sanity hits 0
        if player.sanity <= 0:
            print("\n  😵 Your sanity reached 0!")
            print("  You start questioning the meaning of everything...")
            extra_damage = random.randint(10, 20)
            player.take_damage(extra_damage)
            print(f"  Existential crisis deals {extra_damage} damage!")

        turn += 1

    # Battle over
    print()
    print("=" * 50)

    if player.is_alive():
        draw_victory()
        print(f"\n  {boss.name} has been defeated!")
        player.wins += 1
        player.record_victory(boss.name)

        # Award XP based on boss level
        xp_gained = boss.level * 20
        print(f"  💫 +{xp_gained} XP!")

        leveled_up = player.gain_xp(xp_gained)
        if leveled_up:
            print()
            print("  ╔══════════════════════════════╗")
            print(f"  ║   🎉 LEVEL UP! Now Lv.{player.level}!    ║")
            print(f"  ║   Max HP:     {player.max_hp}              ║")
            print(f"  ║   Max Energy: {player.max_energy}              ║")
            print(f"  ║   Max Sanity: {player.max_sanity}              ║")
            print("  ╚══════════════════════════════╝")
        else:
            remaining = player.xp_to_next_level() - player.xp
            print(f"  📊 XP: {player.xp}/{player.xp_to_next_level()} ({remaining} to next level)")

        return True
    else:
        draw_defeat()
        print(f"\n  {boss.name} was too powerful...")
        player.losses += 1
        return False
