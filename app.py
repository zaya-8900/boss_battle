"""Flask web interface for Boss Battle Simulator: Life Edition."""

import random

from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    jsonify,
)

from player import Player
from bosses import get_all_bosses, Boss
from attacks import PLAYER_ATTACKS, Attack
from display import BOSS_ART

app = Flask(__name__)
app.secret_key = "boss-battle-web-secret-key-change-me"


@app.context_processor
def inject_theme():
    """Make theme available in all templates."""
    settings = session.get("settings", {})
    return {"theme": settings.get("theme", "dark")}


# ── Session Helpers ─────────────────────────────────────────


def player_to_session(player):
    """Serialize a Player object into the Flask session."""
    session["player"] = {
        "name": player.name,
        "level": player.level,
        "xp": player.xp,
        "max_hp": player.max_hp,
        "hp": player.hp,
        "max_energy": player.max_energy,
        "energy": player.energy,
        "max_sanity": player.max_sanity,
        "sanity": player.sanity,
        "wins": player.wins,
        "losses": player.losses,
        "bosses_defeated": player.bosses_defeated,
    }


def player_from_session():
    """Deserialize a Player object from the Flask session."""
    data = session.get("player")
    if not data:
        return None
    player = Player(data["name"])
    player.level = data["level"]
    player.xp = data["xp"]
    player.max_hp = data["max_hp"]
    player.hp = data["hp"]
    player.max_energy = data["max_energy"]
    player.energy = data["energy"]
    player.max_sanity = data["max_sanity"]
    player.sanity = data["sanity"]
    player.wins = data["wins"]
    player.losses = data["losses"]
    player.bosses_defeated = data["bosses_defeated"]
    return player


def boss_to_session(boss):
    """Serialize a Boss object into the Flask session."""
    session["boss"] = {
        "name": boss.name,
        "level": boss.level,
        "hp": boss.hp,
        "max_hp": boss.max_hp,
        "intro_quote": getattr(boss, "intro_quote", ""),
        "defeat_quote": getattr(boss, "defeat_quote", ""),
        "attacks": [
            {
                "name": a.name,
                "power": a.power,
                "accuracy": a.accuracy,
                "description": a.description,
                "status_effect": a.status_effect,
            }
            for a in boss.attacks
        ],
    }


def boss_from_session():
    """Deserialize a Boss object from the Flask session."""
    data = session.get("boss")
    if not data:
        return None
    attacks = [
        Attack(a["name"], a["power"], a["accuracy"], description=a["description"],
               status_effect=a.get("status_effect"))
        for a in data["attacks"]
    ]
    boss = Boss(data["name"], data["level"], data["max_hp"], attacks,
                intro_quote=data.get("intro_quote", ""),
                defeat_quote=data.get("defeat_quote", ""))
    boss.hp = data["hp"]
    return boss


# ── Routes ──────────────────────────────────────────────────


@app.route("/")
def index():
    """Landing page: show name form if no player, else main menu."""
    player = player_from_session()
    return render_template("menu.html", player=player)


@app.route("/start", methods=["POST"])
def start():
    """Create or load a player from the save file."""
    name = request.form.get("name", "").strip()
    if not name:
        name = "Student"
    player = Player.load(name)
    player_to_session(player)
    player.save()
    return redirect(url_for("index"))


@app.route("/choose_boss")
def choose_boss():
    """Boss selection screen."""
    player = player_from_session()
    if not player:
        return redirect(url_for("index"))
    bosses = get_all_bosses()
    return render_template("choose_boss.html", player=player, bosses=bosses)


@app.route("/battle/start", methods=["POST"])
def battle_start():
    """Initialize a battle with a chosen or random boss."""
    player = player_from_session()
    if not player:
        return redirect(url_for("index"))

    bosses = get_all_bosses()
    boss_index = request.form.get("boss_index")

    if boss_index is not None:
        try:
            idx = int(boss_index)
            if 0 <= idx < len(bosses):
                boss = bosses[idx]
            else:
                boss = random.choice(bosses)
        except ValueError:
            boss = random.choice(bosses)
    else:
        boss = random.choice(bosses)

    # Restore player stats for the new battle
    player.restore_for_battle()
    _apply_difficulty(player, boss)
    player_to_session(player)
    boss_to_session(boss)
    session["turn"] = 1
    session["battle_active"] = True
    session["player_effects"] = []
    session["boss_effects"] = []

    return redirect(url_for("battle"))


@app.route("/battle")
def battle():
    """Render the two-panel battle page."""
    player = player_from_session()
    boss = boss_from_session()

    if not player or not boss or not session.get("battle_active"):
        return redirect(url_for("index"))

    boss_art_lines = BOSS_ART.get(boss.name, BOSS_ART["default"])
    boss_art = "\n".join(boss_art_lines)

    return render_template(
        "battle.html",
        player=player,
        boss=boss,
        boss_art=boss_art,
        attacks=PLAYER_ATTACKS,
        turn=session.get("turn", 1),
        player_effects=session.get("player_effects", []),
        boss_effects=session.get("boss_effects", []),
    )


@app.route("/battle/action", methods=["POST"])
def battle_action():
    """Process one combat turn. Returns JSON for the modal."""
    player = player_from_session()
    boss = boss_from_session()

    if not player or not boss:
        return jsonify({"error": "No active battle"}), 400

    data = request.get_json()
    action_type = data.get("action_type", "")
    events = []
    battle_over = False
    result = None
    victory_data = None

    player_effects = session.get("player_effects", [])
    boss_effects = session.get("boss_effects", [])

    # ── Process status effects at start of turn ───────────
    player_stunned = _process_effects_web(player, player_effects, player.name, events)
    boss_stunned = _process_effects_web(boss, boss_effects, boss.name, events)

    # Check if player died from effects
    if not player.is_alive():
        player.losses += 1
        battle_over = True
        result = "defeat"

    if not battle_over and player_stunned and action_type != "run":
        events.append({"type": "stun_skip", "text": "You're stunned! Turn skipped..."})
        # Boss still attacks (if not stunned)
        if not boss_stunned:
            _boss_attacks(boss, player, events, player_effects)
            _sanity_check(player, events)
        else:
            events.append({"type": "stun_skip", "text": f"{boss.name} is stunned! Turn skipped!"})

        if not player.is_alive():
            player.losses += 1
            battle_over = True
            result = "defeat"

    # ── Run attempt ──────────────────────────────────────
    elif not battle_over and action_type == "run":
        if random.randint(1, 100) <= 50:
            events.append({
                "type": "run_success",
                "text": "You successfully ran away!",
            })
            battle_over = True
            result = "run"
        else:
            events.append({
                "type": "run_fail",
                "text": "You tried to run but tripped over your backpack!",
            })
            if not boss_stunned:
                _boss_attacks(boss, player, events, player_effects)
                _sanity_check(player, events)
            else:
                events.append({"type": "stun_skip", "text": f"{boss.name} is stunned! Turn skipped!"})

            if not player.is_alive():
                player.losses += 1
                battle_over = True
                result = "defeat"

    # ── Player attack ────────────────────────────────────
    elif not battle_over and action_type == "attack":
        attack_index = data.get("attack_index", 0)
        if not (0 <= attack_index < len(PLAYER_ATTACKS)):
            return jsonify({"error": "Invalid attack"}), 400

        atk = PLAYER_ATTACKS[attack_index]

        if atk.energy_cost > 0 and player.energy < atk.energy_cost:
            return jsonify({
                "error": f"Not enough energy! Need {atk.energy_cost}, have {player.energy}",
            }), 400
        if atk.sanity_cost > 0 and player.sanity < atk.sanity_cost:
            return jsonify({
                "error": f"Not enough sanity! Need {atk.sanity_cost}, have {player.sanity}",
            }), 400

        player.use_energy(atk.energy_cost)
        player.use_sanity(atk.sanity_cost)

        events.append({
            "type": "player_attack",
            "text": f"You used {atk.name}!",
        })

        if atk.power == 0:
            events.append({
                "type": "skip",
                "text": "You're... doing nothing. But you feel rested.",
            })
        else:
            hit_roll = random.randint(1, 100)
            if hit_roll <= atk.accuracy:
                damage = atk.power + random.randint(-5, 5)
                damage = max(1, damage)

                if random.randint(1, 100) <= 10:
                    damage *= 2
                    events.append({
                        "type": "critical",
                        "text": f"CRITICAL HIT! {damage} damage!",
                    })
                else:
                    events.append({
                        "type": "hit",
                        "text": f"{damage} damage!",
                    })

                boss.take_damage(damage)

                # Try to apply status effect to boss
                effect_msg = _try_apply_effect_web(atk, boss_effects, boss.name)
                if effect_msg:
                    events.append({"type": "status_effect", "text": effect_msg})
            else:
                events.append({
                    "type": "miss",
                    "text": f"MISS! {atk.description}",
                })

        if not boss.is_alive():
            xp_gained = boss.level * 20
            leveled_up = player.gain_xp(xp_gained)
            player.wins += 1
            player.record_victory(boss.name)
            battle_over = True
            result = "victory"
            victory_data = {
                "xp_gained": xp_gained,
                "leveled_up": leveled_up,
                "new_level": player.level,
                "boss_name": boss.name,
                "defeat_quote": boss.defeat_quote,
                "max_hp": player.max_hp,
                "max_energy": player.max_energy,
                "max_sanity": player.max_sanity,
            }
        else:
            if not boss_stunned:
                _boss_attacks(boss, player, events, player_effects)
                _sanity_check(player, events)
            else:
                events.append({"type": "stun_skip", "text": f"{boss.name} is stunned! Turn skipped!"})

            if not player.is_alive():
                player.losses += 1
                battle_over = True
                result = "defeat"

    # ── Persist state ────────────────────────────────────

    if battle_over:
        session["battle_active"] = False
        session["player_effects"] = []
        session["boss_effects"] = []
        player.save()
    else:
        session["player_effects"] = player_effects
        session["boss_effects"] = boss_effects

    player_to_session(player)
    boss_to_session(boss)
    session["turn"] = session.get("turn", 1) + 1

    return jsonify({
        "events": events,
        "battle_over": battle_over,
        "result": result,
        "victory_data": victory_data,
        "player_effects": player_effects,
        "boss_effects": boss_effects,
        "player": {
            "hp": player.hp,
            "max_hp": player.max_hp,
            "energy": player.energy,
            "max_energy": player.max_energy,
            "sanity": player.sanity,
            "max_sanity": player.max_sanity,
        },
        "boss": {
            "hp": boss.hp,
            "max_hp": boss.max_hp,
        },
        "turn": session.get("turn", 1),
    })


def _try_apply_effect_web(atk, target_effects, target_name):
    """Roll for a status effect. Returns a message or None."""
    se = atk.status_effect
    if not se:
        return None
    if random.randint(1, 100) > se["chance"]:
        return None

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


def _process_effects_web(target, effects, target_name, events):
    """Apply active effects at start of turn. Returns True if target is stunned."""
    remaining = []
    stunned = False
    for e in effects:
        if e["name"] == "poison":
            target.take_damage(e["damage"])
            events.append({"type": "effect_damage", "text": f"{target_name} takes {e['damage']} poison damage!"})
        elif e["name"] == "stun":
            stunned = True
        e["turns_left"] -= 1
        if e["turns_left"] > 0:
            remaining.append(e)
        else:
            labels = {"poison": "Poison", "stun": "Stun", "weaken": "Weaken"}
            events.append({"type": "effect_expire", "text": f"{labels.get(e['name'], e['name'])} wore off on {target_name}."})
    effects.clear()
    effects.extend(remaining)
    return stunned


def _boss_attacks(boss, player, events, player_effects=None):
    """Execute the boss's attack and append events."""
    if player_effects is None:
        player_effects = []
    boss_atk = random.choice(boss.attacks)
    events.append({
        "type": "boss_attack",
        "text": f"{boss.name} uses {boss_atk.name}!",
    })
    events.append({
        "type": "boss_desc",
        "text": f'"{boss_atk.description}"',
    })

    hit_roll = random.randint(1, 100)
    if hit_roll <= boss_atk.accuracy:
        damage = boss_atk.power + random.randint(-3, 3)
        damage = max(1, damage)

        # Apply weaken: boss deals less damage when weakened
        boss_effects = session.get("boss_effects", [])
        for e in boss_effects:
            if e["name"] == "weaken":
                damage = int(damage * (1.0 - e.get("reduction", 0.3)))
                break

        player.take_damage(damage)
        events.append({"type": "boss_hit", "text": f"-{damage} HP!"})

        sanity_drain = random.randint(2, 8)
        player.use_sanity(sanity_drain)
        events.append({"type": "sanity_drain", "text": f"Sanity -{sanity_drain}..."})

        # Try to apply status effect to player
        effect_msg = _try_apply_effect_web(boss_atk, player_effects, player.name)
        if effect_msg:
            events.append({"type": "status_effect", "text": effect_msg})
    else:
        events.append({"type": "boss_miss", "text": "You dodged it!"})


def _sanity_check(player, events):
    """Check for sanity=0 crisis damage."""
    if player.sanity <= 0 and player.is_alive():
        extra = random.randint(10, 20)
        player.take_damage(extra)
        events.append({
            "type": "sanity_crisis",
            "text": f"Your sanity reached 0! Existential crisis deals {extra} damage!",
        })


@app.route("/survival/start", methods=["POST"])
def survival_start():
    """Start survival mode — wave 1."""
    player = player_from_session()
    if not player:
        return redirect(url_for("index"))

    bosses = get_all_bosses()
    template = random.choice(bosses)

    wave = 1
    scaled_hp = int(template.max_hp * (1 + 0.15 * wave))
    boss = Boss(template.name, template.level, scaled_hp, template.attacks)

    player.restore_for_battle()
    player_to_session(player)
    boss_to_session(boss)
    session["turn"] = 1
    session["battle_active"] = True
    session["survival_mode"] = True
    session["survival_wave"] = wave
    session["survival_xp"] = 0

    return redirect(url_for("survival"))


@app.route("/survival")
def survival():
    """Render the survival battle page (reuses battle.html)."""
    player = player_from_session()
    boss = boss_from_session()

    if not player or not boss or not session.get("battle_active"):
        return redirect(url_for("index"))

    boss_art_lines = BOSS_ART.get(boss.name, BOSS_ART["default"])
    boss_art = "\n".join(boss_art_lines)

    return render_template(
        "battle.html",
        player=player,
        boss=boss,
        boss_art=boss_art,
        attacks=PLAYER_ATTACKS,
        turn=session.get("turn", 1),
        survival_mode=True,
        survival_wave=session.get("survival_wave", 1),
    )


@app.route("/survival/action", methods=["POST"])
def survival_action():
    """Process one survival combat turn. Returns JSON."""
    player = player_from_session()
    boss = boss_from_session()

    if not player or not boss:
        return jsonify({"error": "No active battle"}), 400

    data = request.get_json()
    action_type = data.get("action_type", "")
    events = []
    battle_over = False
    result = None
    victory_data = None

    wave = session.get("survival_wave", 1)
    total_xp = session.get("survival_xp", 0)

    # No running in survival
    if action_type == "run":
        events.append({
            "type": "run_fail",
            "text": "No running in survival mode! Stand and fight!",
        })
        _boss_attacks(boss, player, events)
        _sanity_check(player, events)

        if not player.is_alive():
            player.losses += 1
            battle_over = True
            result = "defeat"
            victory_data = {
                "survival_wave": wave - 1,
                "survival_xp": total_xp,
            }

    elif action_type == "attack":
        attack_index = data.get("attack_index", 0)
        if not (0 <= attack_index < len(PLAYER_ATTACKS)):
            return jsonify({"error": "Invalid attack"}), 400

        atk = PLAYER_ATTACKS[attack_index]

        if atk.energy_cost > 0 and player.energy < atk.energy_cost:
            return jsonify({
                "error": f"Not enough energy! Need {atk.energy_cost}, have {player.energy}",
            }), 400
        if atk.sanity_cost > 0 and player.sanity < atk.sanity_cost:
            return jsonify({
                "error": f"Not enough sanity! Need {atk.sanity_cost}, have {player.sanity}",
            }), 400

        player.use_energy(atk.energy_cost)
        player.use_sanity(atk.sanity_cost)

        events.append({
            "type": "player_attack",
            "text": f"You used {atk.name}!",
        })

        if atk.power == 0:
            events.append({
                "type": "skip",
                "text": "You're... doing nothing. But you feel rested.",
            })
        else:
            hit_roll = random.randint(1, 100)
            if hit_roll <= atk.accuracy:
                damage = atk.power + random.randint(-5, 5)
                damage = max(1, damage)

                if random.randint(1, 100) <= 10:
                    damage *= 2
                    events.append({
                        "type": "critical",
                        "text": f"CRITICAL HIT! {damage} damage!",
                    })
                else:
                    events.append({
                        "type": "hit",
                        "text": f"{damage} damage!",
                    })

                boss.take_damage(damage)
            else:
                events.append({
                    "type": "miss",
                    "text": f"MISS! {atk.description}",
                })

        # Boss defeated — advance wave
        if not boss.is_alive():
            xp_gained = boss.level * 20
            total_xp += xp_gained
            player.gain_xp(xp_gained)
            player.record_victory(boss.name)
            player.wins += 1

            # Partial recovery
            player.heal(30)
            player.use_energy(-20)
            player.use_sanity(-20)

            events.append({
                "type": "survival_wave_clear",
                "text": f"Wave {wave} cleared! +{xp_gained} XP | +30 HP, +20 Energy, +20 Sanity",
            })

            # Spawn next wave boss
            wave += 1
            bosses = get_all_bosses()
            template = random.choice(bosses)
            scaled_hp = int(template.max_hp * (1 + 0.15 * wave))
            new_boss = Boss(template.name, template.level, scaled_hp, template.attacks)
            boss = new_boss

            events.append({
                "type": "survival_next_wave",
                "text": f"Wave {wave}: {boss.name} (HP: {boss.hp}) approaches!",
            })

            session["survival_wave"] = wave
            session["survival_xp"] = total_xp
        else:
            _boss_attacks(boss, player, events)
            _sanity_check(player, events)

            if not player.is_alive():
                player.losses += 1
                battle_over = True
                result = "defeat"
                victory_data = {
                    "survival_wave": wave - 1,
                    "survival_xp": total_xp,
                }

    if battle_over:
        session["battle_active"] = False
        session["survival_mode"] = False
        player.save()

    player_to_session(player)
    boss_to_session(boss)
    session["turn"] = session.get("turn", 1) + 1

    return jsonify({
        "events": events,
        "battle_over": battle_over,
        "result": result,
        "victory_data": victory_data,
        "survival_mode": True,
        "survival_wave": session.get("survival_wave", 1),
        "player": {
            "hp": player.hp,
            "max_hp": player.max_hp,
            "energy": player.energy,
            "max_energy": player.max_energy,
            "sanity": player.sanity,
            "max_sanity": player.max_sanity,
        },
        "boss": {
            "hp": boss.hp,
            "max_hp": boss.max_hp,
            "name": boss.name,
            "level": boss.level,
        },
        "turn": session.get("turn", 1),
    })


@app.route("/stats")
def stats():
    """Player stats page."""
    player = player_from_session()
    if not player:
        return redirect(url_for("index"))

    total_bosses = len(get_all_bosses())
    defeated_count = len(player.bosses_defeated)
    total_battles = player.wins + player.losses
    win_rate = (
        f"{player.wins / total_battles * 100:.0f}%"
        if total_battles > 0
        else "N/A"
    )

    return render_template(
        "stats.html",
        player=player,
        total_bosses=total_bosses,
        defeated_count=defeated_count,
        win_rate=win_rate,
    )


@app.route("/victory_log")
def victory_log():
    """Victory log page."""
    player = player_from_session()
    if not player:
        return redirect(url_for("index"))

    all_bosses = get_all_bosses()
    total = len(all_bosses)
    defeated_count = len(player.bosses_defeated)
    all_defeated = defeated_count == total

    return render_template(
        "victory_log.html",
        player=player,
        all_bosses=all_bosses,
        total=total,
        defeated_count=defeated_count,
        all_defeated=all_defeated,
    )


@app.route("/help")
def help_page():
    """How to play page."""
    player = player_from_session()
    if not player:
        return redirect(url_for("index"))
    return render_template("help.html", player=player, attacks=PLAYER_ATTACKS)


@app.route("/settings")
def settings():
    """Settings page."""
    player = player_from_session()
    if not player:
        return redirect(url_for("index"))
    current = session.get("settings", {"difficulty": "normal", "theme": "dark"})
    return render_template("settings.html", player=player, settings=current)


@app.route("/settings", methods=["POST"])
def save_settings():
    """Save settings to session."""
    difficulty = request.form.get("difficulty", "normal")
    theme = request.form.get("theme", "dark")
    if difficulty not in ("easy", "normal", "hard"):
        difficulty = "normal"
    if theme not in ("dark", "light"):
        theme = "dark"
    session["settings"] = {"difficulty": difficulty, "theme": theme}
    return redirect(url_for("index"))


def _apply_difficulty(player, boss):
    """Apply difficulty modifiers to player HP and boss damage."""
    settings = session.get("settings", {})
    difficulty = settings.get("difficulty", "normal")
    if difficulty == "easy":
        # Player gets +25% HP
        bonus = int(player.max_hp * 0.25)
        player.max_hp += bonus
        player.hp += bonus
        # Boss gets -25% on all attack power (stored in session)
        for atk in boss.attacks:
            atk.power = max(1, int(atk.power * 0.75))
    elif difficulty == "hard":
        # Player gets -25% HP
        penalty = int(player.max_hp * 0.25)
        player.max_hp = max(1, player.max_hp - penalty)
        player.hp = min(player.hp, player.max_hp)
        # Boss gets +25% on all attack power
        for atk in boss.attacks:
            atk.power = int(atk.power * 1.25)


@app.route("/logout", methods=["POST"])
def logout():
    """Save player progress and clear the session."""
    player = player_from_session()
    if player:
        player.save()
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
