"""Battle logic and combat system."""

import random
import time

from display import (
    draw_hp_bar,
    draw_victory,
    draw_defeat,
    draw_boss_entrance,
    draw_attack_hit,
    draw_miss,
    draw_level_up,
    draw_reward_screen,
    type_text,
)


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
            print("  Invalid choice. Pick a number from the list.")
            return None
    except ValueError:
        print("  Invalid choice. Pick a number from the list.")
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

        # Procrastinate does no damage but restores resources
        if atk.power == 0:
            print(f"  You're... doing nothing. But you feel rested.")
            time.sleep(0.5)
            return None

        # Check accuracy
        hit_roll = random.randint(1, 100)
        if hit_roll <= atk.accuracy:
            # Calculate damage with some randomness
            damage = atk.power + random.randint(-5, 5)
            damage = max(1, damage)

            # Critical hit (10% chance)
            if random.randint(1, 100) <= 10:
                damage *= 2
                draw_attack_hit(damage, critical=True)
            else:
                draw_attack_hit(damage, critical=False)

            time.sleep(0.3)
            boss.take_damage(damage)
            print(f"  {boss.name} takes {damage} damage!")
        else:
            draw_miss()
            print(f"  {atk.description}")

        time.sleep(0.5)
        return None


def boss_turn(player, boss):
    """Handle the boss's turn."""
    atk = random.choice(boss.attacks)
    print(f"\n  {boss.name} uses {atk.name}!")
    type_text(f"  \"{atk.description}\"", delay=0.02)
    time.sleep(0.3)

    hit_roll = random.randint(1, 100)
    if hit_roll <= atk.accuracy:
        damage = atk.power + random.randint(-3, 3)
        damage = max(1, damage)
        player.take_damage(damage)
        draw_attack_hit(damage)

        # Bosses also drain sanity
        sanity_drain = random.randint(2, 8)
        player.use_sanity(sanity_drain)
        print(f"  Sanity -{sanity_drain}...")
    else:
        draw_miss()
        print(f"  You dodged it!")

    time.sleep(0.5)


def battle(player, boss, player_attacks):
    """Run a battle between the player and a boss.

    Returns:
        True if player wins, False if player loses.
    """
    # Dramatic entrance
    print()
    print("=" * 50)
    draw_boss_entrance(boss.name)
    print()
    type_text(f"  ⚔️  {player.name}  VS  {boss.name} (Lv.{boss.level})  ⚔️", delay=0.04)
    print("=" * 50)
    if boss.intro_quote:
        print()
        type_text(f'  "{boss.intro_quote}"', delay=0.03)
    time.sleep(0.5)

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
        if player.sanity <= 0 and player.is_alive():
            print("\n  😵 Your sanity reached 0!")
            type_text("  You start questioning the meaning of everything...", delay=0.02)
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
        if boss.defeat_quote:
            type_text(f'  "{boss.defeat_quote}"', delay=0.03)
        player.wins += 1
        player.record_victory(boss.name)

        # Award XP based on boss level
        xp_gained = boss.level * 20
        leveled_up = player.gain_xp(xp_gained)

        if leveled_up:
            draw_level_up(player)

        draw_reward_screen(boss.name, xp_gained, player)

        return True
    else:
        draw_defeat()
        type_text(f"\n  {boss.name} was too powerful...", delay=0.03)
        player.losses += 1
        return False
