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


# ── Status Effect Helpers ─────────────────────────────────────

def try_apply_effect(atk, target_effects, target_name):
    """Roll for a status effect from an attack. Returns a message or None."""
    se = atk.status_effect
    if not se:
        return None

    if random.randint(1, 100) > se["chance"]:
        return None

    # Don't stack the same effect — refresh duration instead
    for e in target_effects:
        if e["name"] == se["name"]:
            e["turns_left"] = se.get("turns", e["turns_left"])
            return f"{target_name} is already {se['name']}ed — duration refreshed!"

    effect = {"name": se["name"], "turns_left": se.get("turns", 1)}
    if se["name"] == "poison":
        effect["damage"] = se["damage"]
    elif se["name"] == "weaken":
        effect["reduction"] = se["reduction"]

    target_effects.append(effect)

    labels = {"poison": "POISONED", "stun": "STUNNED", "weaken": "WEAKENED"}
    return f"{target_name} is {labels.get(se['name'], se['name'].upper())}!"


def process_effects(target, effects, target_name):
    """Apply active effects at start of turn. Returns (messages, is_stunned)."""
    messages = []
    stunned = False
    remaining = []

    for e in effects:
        if e["name"] == "poison":
            target.take_damage(e["damage"])
            messages.append(f"{target_name} takes {e['damage']} poison damage!")
        elif e["name"] == "stun":
            stunned = True
            messages.append(f"{target_name} is stunned and can't act!")
        # weaken is checked during damage calculation, not here

        e["turns_left"] -= 1
        if e["turns_left"] > 0:
            remaining.append(e)
        else:
            labels = {"poison": "Poison", "stun": "Stun", "weaken": "Weaken"}
            messages.append(f"{labels.get(e['name'], e['name'])} wore off on {target_name}.")

    effects.clear()
    effects.extend(remaining)
    return messages, stunned


def get_weaken_multiplier(effects):
    """Return the damage multiplier from weaken effects (1.0 = normal)."""
    for e in effects:
        if e["name"] == "weaken":
            return 1.0 - e["reduction"]
    return 1.0


def format_active_effects(effects):
    """Return a display string of active effects."""
    if not effects:
        return ""
    labels = {"poison": "PSN", "stun": "STN", "weaken": "WKN"}
    parts = [f"{labels.get(e['name'], e['name'])}({e['turns_left']})" for e in effects]
    return " ".join(parts)


# ── Battle Display ────────────────────────────────────────────

def show_battle_status(player, boss, player_effects=None, boss_effects=None):
    """Display current HP/stats for both player and boss."""
    player_effects = player_effects or []
    boss_effects = boss_effects or []

    print()
    boss_eff_str = format_active_effects(boss_effects)
    boss_line = f"  ┌─── {boss.name} (Lv.{boss.level})"
    if boss_eff_str:
        boss_line += f" [{boss_eff_str}]"
    boss_line += " ───"
    print(boss_line)
    print(f"  │ HP: {draw_hp_bar(boss.hp, boss.max_hp)}")
    print(f"  └{'─' * 40}")

    print()
    player_eff_str = format_active_effects(player_effects)
    player_line = f"  ┌─── {player.name} (Lv.{player.level})"
    if player_eff_str:
        player_line += f" [{player_eff_str}]"
    player_line += " ───"
    print(player_line)
    print(f"  │ HP:     {draw_hp_bar(player.hp, player.max_hp)}")
    print(f"  │ Energy: {draw_hp_bar(player.energy, player.max_energy)}")
    print(f"  │ Sanity: {draw_hp_bar(player.sanity, player.max_sanity)}")
    print(f"  └{'─' * 40}")


def show_attack_menu(player_attacks, player, allow_run=True):
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
    if allow_run:
        print(f"  ║ [R] 🏃 Run Away")
    else:
        print(f"  ║ [R] 🚫 No running in survival!")
    print(f"  ╚{'═' * 28}╝")

    choice = input("  What will you do? ").strip().lower()

    if choice == "r":
        if allow_run:
            return "run"
        else:
            print("\n  No running in survival mode! Stand and fight!")
            return None

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


def player_turn(player, boss, player_attacks, allow_run=True, boss_effects=None):
    """Handle the player's turn. Returns 'run' if player flees, else None."""
    boss_effects = boss_effects or []

    while True:
        result = show_attack_menu(player_attacks, player, allow_run=allow_run)

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

            # Try to apply status effect
            msg = try_apply_effect(atk, boss_effects, boss.name)
            if msg:
                print(f"  {msg}")
        else:
            draw_miss()
            print(f"  {atk.description}")

        time.sleep(0.5)
        return None


def boss_turn(player, boss, player_effects=None, boss_effects=None):
    """Handle the boss's turn."""
    player_effects = player_effects or []
    boss_effects = boss_effects or []

    atk = random.choice(boss.attacks)
    print(f"\n  {boss.name} uses {atk.name}!")
    type_text(f"  \"{atk.description}\"", delay=0.02)
    time.sleep(0.3)

    hit_roll = random.randint(1, 100)
    if hit_roll <= atk.accuracy:
        damage = atk.power + random.randint(-3, 3)
        damage = max(1, damage)

        # Apply weaken from boss_effects (boss deals less when weakened)
        damage = int(damage * get_weaken_multiplier(boss_effects))

        player.take_damage(damage)
        draw_attack_hit(damage)

        # Bosses also drain sanity
        sanity_drain = random.randint(2, 8)
        player.use_sanity(sanity_drain)
        print(f"  Sanity -{sanity_drain}...")

        # Try to apply status effect to player
        msg = try_apply_effect(atk, player_effects, player.name)
        if msg:
            print(f"  {msg}")
    else:
        draw_miss()
        print(f"  You dodged it!")

    time.sleep(0.5)


def battle(player, boss, player_attacks):
    """Run a battle between the player and a boss.

    Returns:
        True if player wins, False if player loses.
    """
    player_effects = []  # effects on the player
    boss_effects = []    # effects on the boss

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

        # Process effects at start of turn
        msgs, player_stunned = process_effects(player, player_effects, player.name)
        for m in msgs:
            print(f"  {m}")

        msgs, boss_stunned = process_effects(boss, boss_effects, boss.name)
        for m in msgs:
            print(f"  {m}")

        if not player.is_alive():
            break

        show_battle_status(player, boss, player_effects, boss_effects)

        # Player turn (skip if stunned)
        if player_stunned:
            print("\n  You're stunned! Turn skipped...")
        else:
            result = player_turn(player, boss, player_attacks, boss_effects)
            if result == "run":
                print("\n  You fled the battle!")
                return False

        # Check if boss is defeated
        if not boss.is_alive():
            break

        # Boss turn (skip if stunned)
        if boss_stunned:
            print(f"\n  {boss.name} is stunned! Their turn is skipped!")
        else:
            boss_turn(player, boss, player_effects, boss_effects)

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


def survival_battle(player, all_bosses, player_attacks):
    """Run an endless survival mode — fight random bosses with scaling HP.

    Player gets only partial recovery between waves.
    Returns (waves_survived, total_xp).
    """
    from bosses import Boss

    wave = 0
    total_xp = 0

    player.restore_for_battle()

    print()
    print("=" * 50)
    type_text("  ⚔️  SURVIVAL MODE ⚔️", delay=0.04)
    type_text("  Fight boss after boss until you fall!", delay=0.02)
    print("=" * 50)
    time.sleep(0.5)

    while player.is_alive():
        wave += 1
        template = random.choice(all_bosses)

        # Scale boss HP: base_hp * (1 + 0.15 * wave)
        scaled_hp = int(template.max_hp * (1 + 0.15 * wave))
        boss = Boss(
            template.name,
            template.level,
            scaled_hp,
            list(template.attacks),
        )

        print(f"\n{'=' * 50}")
        print(f"  WAVE {wave}")
        print(f"{'=' * 50}")
        draw_boss_entrance(boss.name)
        type_text(f"  ⚔️  {boss.name} (Lv.{boss.level}) — HP: {boss.hp}  ⚔️", delay=0.03)
        time.sleep(0.3)

        turn = 1
        while player.is_alive() and boss.is_alive():
            print(f"\n{'─' * 50}")
            print(f"  WAVE {wave} — TURN {turn}")
            print(f"{'─' * 50}")

            show_battle_status(player, boss)

            result = player_turn(player, boss, player_attacks, allow_run=False)
            # No running in survival

            if not boss.is_alive():
                break

            boss_turn(player, boss)

            if player.sanity <= 0 and player.is_alive():
                print("\n  😵 Your sanity reached 0!")
                extra_damage = random.randint(10, 20)
                player.take_damage(extra_damage)
                print(f"  Existential crisis deals {extra_damage} damage!")

            turn += 1

        if not player.is_alive():
            break

        # Boss defeated — partial recovery
        xp_gained = boss.level * 20
        total_xp += xp_gained
        player.gain_xp(xp_gained)
        player.record_victory(boss.name)

        print()
        draw_victory()
        print(f"  Wave {wave} cleared! +{xp_gained} XP")

        # Partial heal between waves
        player.heal(30)
        player.use_energy(-20)  # restores 20
        player.use_sanity(-20)  # restores 20
        print(f"  Partial recovery: +30 HP, +20 Energy, +20 Sanity")
        time.sleep(0.5)

    # Survival over
    print()
    print("=" * 50)
    draw_defeat()
    print(f"\n  SURVIVAL OVER!")
    print(f"  Waves survived: {wave - 1}")
    print(f"  Total XP earned: {total_xp}")
    print(f"={'=' * 49}")

    player.losses += 1
    return wave - 1, total_xp
