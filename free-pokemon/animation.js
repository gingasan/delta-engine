function triggerAttackAnimation(attacker, defender) {
    const attackerImg = document.querySelector(`.${attacker} img`);
    const defenderImg = document.querySelector(`.${defender} img`);

    let animation;
    if (attacker === "pokemon-1") {
        animation = "attack-animation-1";
    } else {
        animation = "attack-animation-2";
    }
    attackerImg.classList.add(animation);
    setTimeout(() => {
        defenderImg.classList.add("shake-animation");
    }, 250);
    setTimeout(() => {
        attackerImg.classList.remove(animation);
        defenderImg.classList.remove("shake-animation");
    }, 1250);
}
