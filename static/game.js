(function () {
    var overlay = document.getElementById("modal-overlay");
    var modalEvents = document.getElementById("modal-events");
    var modalBtn = document.getElementById("modal-btn");
    var battleOver = false;

    // Attach click handlers to attack buttons
    document.querySelectorAll(".attack-btn").forEach(function (btn) {
        btn.addEventListener("click", function () {
            if (btn.disabled) return;
            var index = parseInt(btn.dataset.index, 10);
            sendAction({ action_type: "attack", attack_index: index });
            disableAllButtons();
        });
    });

    // Run button
    document.getElementById("run-btn").addEventListener("click", function () {
        sendAction({ action_type: "run" });
        disableAllButtons();
    });

    function disableAllButtons() {
        document.querySelectorAll(".attack-btn, .run-btn").forEach(function (b) {
            b.disabled = true;
        });
    }

    function sendAction(payload) {
        fetch("/battle/action", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        })
            .then(function (res) {
                if (!res.ok) {
                    return res.json().then(function (d) {
                        throw new Error(d.error || "Server error");
                    });
                }
                return res.json();
            })
            .then(function (data) {
                if (data.error) {
                    alert(data.error);
                    location.reload();
                    return;
                }
                updateBars(data);
                showModal(data);
            })
            .catch(function (err) {
                alert(err.message);
                location.reload();
            });
    }

    function updateBars(data) {
        var p = data.player;
        var b = data.boss;
        animateBar("player-hp-fill", "player-hp-text", p.hp, p.max_hp);
        animateBar("player-energy-fill", "player-energy-text", p.energy, p.max_energy);
        animateBar("player-sanity-fill", "player-sanity-text", p.sanity, p.max_sanity);
        animateBar("boss-hp-fill", "boss-hp-text", b.hp, b.max_hp);

        // Update status effect badges
        updateEffectBadges("player-effects", data.player_effects || []);
        updateEffectBadges("boss-effects", data.boss_effects || []);
    }

    function updateEffectBadges(containerId, effects) {
        var container = document.getElementById(containerId);
        if (!container) return;
        container.innerHTML = "";
        effects.forEach(function (e) {
            var span = document.createElement("span");
            span.className = "effect-badge effect-" + e.name;
            span.textContent = e.name.toUpperCase() + "(" + e.turns_left + ")";
            container.appendChild(span);
        });
    }

    function animateBar(fillId, textId, current, max) {
        var fill = document.getElementById(fillId);
        var text = document.getElementById(textId);
        var pct = max > 0 ? (current / max) * 100 : 0;
        fill.style.width = pct + "%";
        text.textContent = current + "/" + max;
    }

    function showModal(data) {
        modalEvents.innerHTML = "";

        data.events.forEach(function (ev) {
            var div = document.createElement("div");
            div.className = "event event-" + ev.type;
            div.textContent = ev.text;
            modalEvents.appendChild(div);
        });

        if (data.battle_over) {
            battleOver = true;

            if (data.result === "victory") {
                var vd = data.victory_data;
                var div = document.createElement("div");
                div.className = "event event-victory";
                var html = "<strong>* VICTORY! *</strong><br>";
                html += "+" + vd.xp_gained + " XP gained!";
                if (vd.leveled_up) {
                    html += "<br>* LEVEL UP! Now Level " + vd.new_level + "! *";
                    html +=
                        "<br>Max HP: " +
                        vd.max_hp +
                        " | Max Energy: " +
                        vd.max_energy +
                        " | Max Sanity: " +
                        vd.max_sanity;
                }
                div.innerHTML = html;
                modalEvents.appendChild(div);
            } else if (data.result === "defeat") {
                var defDiv = document.createElement("div");
                defDiv.className = "event event-defeat";
                defDiv.innerHTML =
                    "<strong>DEFEATED</strong><br>R.I.P. Your G.P.A.";
                modalEvents.appendChild(defDiv);
            }
            // run_success is already in events

            modalBtn.textContent = "Back to Menu";
        } else {
            modalBtn.textContent = "Continue";
        }

        overlay.classList.add("active");
    }

    modalBtn.addEventListener("click", function () {
        if (battleOver) {
            window.location.href = "/";
        } else {
            window.location.reload();
        }
    });
})();
