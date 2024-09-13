function initState(init_data) {
    fetch("http://127.0.0.1:5000/init-state", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(init_data)
    })
        .then(response => response.json())
        .then(data => {
            const pokemon1Name = document.querySelector(".pokemon-1 .name")
            const pokemon1Img = document.querySelector(".pokemon-1 img");
            pokemon1Name.textContent = init_data.species;
            pokemon1Img.src = `asset/pm/${init_data.avatar}`;
            if (pokemon1Img.classList.contains("faint-animation")) {
                pokemon1Img.classList.remove("faint-animation");
            }

            const moves = document.querySelectorAll(".move");
            moves.forEach((move, i) => {
                if (!data.pokemon_1[`move_${i + 1}`]) {
                    return;
                }
                const moveName = move.querySelector(".move-name");
                const moveInfo = move.querySelector(".move-info");
                const moveImg = move.querySelector("img");
                
                // update move
                moveName.firstChild.textContent = data.pokemon_1[`move_${i + 1}`].id;
                moveInfo.textContent = `pow: ${data.pokemon_1[`move_${i + 1}`].power} acc: ${data.pokemon_1[`move_${i + 1}`].accuracy}`;

                // update type icon
                moveImg.src = `asset/type/${data.pokemon_1[`move_${i + 1}`].type.toLowerCase()}.png`;
            });

            // update logs
            const logContainer = document.querySelector(".log-container");
            logContainer.innerHTML = "";
            data.logs.forEach(entry => {
                const logDiv = document.createElement("div");
                logDiv.className = "log-entry";
                logDiv.textContent = entry.content;
                if (entry.color) {
                    logDiv.style.color = entry.color;
                }
                logContainer.appendChild(logDiv);
            });
            logContainer.scrollTop = logContainer.scrollHeight;

            // update opponent
            const pokemon2Name = document.querySelector(".pokemon-2 .name")
            const pokemon2Img = document.querySelector(".pokemon-2 img");
            pokemon2Name.textContent = data.pokemon_2.species;
            pokemon2Img.src = `asset/pm/${data.pokemon_2.avatar}`;
            if (pokemon2Img.classList.contains("faint-animation")) {
                pokemon2Img.classList.remove("faint-animation");
            }

            // update hp & status
            const hp1 = document.querySelector(".pokemon-1 .hp");
            hp1.style.width = "100%";
            document.querySelector(".pokemon-1 .status img").style.display = "none";
            const hp2 = document.querySelector(".pokemon-2 .hp");
            hp2.style.width = "100%";
            document.querySelector(".pokemon-2 .status img").style.display = "none";

            // update code
            const codeDisplay = document.querySelector('.code-display pre code');
            codeDisplay.textContent = data.code;
            Prism.highlightElement(codeDisplay);
            document.querySelector(".toggle-code-display").textContent = `Code for ${init_data.species}`;
        });
}

function updateStatePhase(data) {
    // update hp
    const hp1 = document.querySelector(".pokemon-1 .hp");
    hp1.style.width = `${(data.pokemon_1.hp / data.pokemon_1.max_hp) * 100}%`;

    const hp2 = document.querySelector(".pokemon-2 .hp");
    hp2.style.width = `${(data.pokemon_2.hp / data.pokemon_2.max_hp) * 100}%`;

    // update status
    const status1Img = document.querySelector(".pokemon-1 .status img");
    if (data.pokemon_1.status) {
        status1Img.src = `asset/status/${Object.keys(data.pokemon_1.status)[0]}.png`;
        status1Img.style.display = "block";
    } else {
        status1Img.style.display = "none";
    }

    const status2Img = document.querySelector(".pokemon-2 .status img");
    if (data.pokemon_2.status) {
        status2Img.src = `asset/status/${Object.keys(data.pokemon_2.status)[0]}.png`;
        status2Img.style.display = "block";
    } else {
        status2Img.style.display = "none";
    }

    // update logs
    const logContainer = document.querySelector(".log-container");
    data.logs.forEach(entry => {
        const logDiv = document.createElement("div");
        logDiv.className = "log-entry";
        logDiv.textContent = entry.content;
        if (entry.color) {
            logDiv.style.color = entry.color;
        }
        logContainer.appendChild(logDiv);
    });
    logContainer.scrollTop = logContainer.scrollHeight;
}

function updateState(move_id) {
    fetch(`http://127.0.0.1:5000/get-state?move_id=${move_id}`)
        .then(response => response.json())
        .then(data => {
            // hide move selector
            document.querySelector(".move-select").style.display = "none";

            // phase 1
            if (data.phase_1) {
                // attack animation
                triggerAttackAnimation(data.phase_1.attacker, data.phase_1.defender);
                // update state
                updateStatePhase(data.phase_1);
            }
            
            // phase 2
            setTimeout(() => {
                if (data.phase_2) {
                    // attack animation
                    triggerAttackAnimation(data.phase_2.attacker, data.phase_2.defender);
                    // update state
                    updateStatePhase(data.phase_2);
                }
            }, 1500);

            // phase 3
            setTimeout(() => {
                updateStatePhase(data.phase_3);

                // faint out animation
                if (data.phase_3.pokemon_1.hp === 0) {
                    const pokemon1Img = document.querySelector(".pokemon-1 img");
                    pokemon1Img.classList.add("faint-animation");
                }
                if (data.phase_3.pokemon_2.hp === 0) {
                    const pokemon2Img = document.querySelector(".pokemon-2 img");
                    pokemon2Img.classList.add("faint-animation");
                }
                
                // show move selector
                if (!data.wrap) {
                    document.querySelector(".move-select").style.display = "block";
                }
            }, 3500);

            // next battle
            setTimeout(() => {
                if (data.wrap) {
                    document.querySelector(".result-section").classList.remove('hidden');
                }
                document.querySelector(".move-select").style.display = "block";
            }, 5500);
        });
}
