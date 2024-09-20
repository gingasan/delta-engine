from flask import Flask, jsonify, request
from flask_cors import CORS
from engine import *
from utils import *
from agent import *


def create_role(code_path):
    code = (
        "from {} import *\n"
        "pokemon={}()"
    ).format(code_path, code_path.split(".")[-1])
    global_vars = {}
    exec(code, global_vars)
    role = global_vars["pokemon"]
    return role

def step(move1_id):
    if user.isfaint() or oppo.isfaint():
        return
    battle.logger.clr()
    if isinstance(oppo, PokemonAgent):
        move2_id = oppo.plan()
    else:
        move2_id = rndc(oppo.get_moves())
    state = battle.act(move1_id, move2_id)
    for phase in ["phase_1", "phase_2"]:
        if state[phase]:
            attacker, defender = ("pokemon-1", "pokemon-2") if state[phase]["attacker"] == user._species else ("pokemon-2", "pokemon-1")
            state[phase]["attacker"] = attacker
            state[phase]["defender"] = defender

    if state["wrap"]:
        if user.isfaint():
            for phase in ["phase_1", "phase_2"]:
                if state[phase] and state[phase]["pokemon_1"]["status"] == "FNT":
                    state[phase]["pokemon_1"]["status"] = {"FNT": ""}
            state["phase_3"]["pokemon_1"]["status"] = {"FNT": ""}
        if oppo.isfaint():
            for phase in ["phase_1", "phase_2"]:
                if state[phase] and state[phase]["pokemon_2"]["status"] == "FNT":
                    state[phase]["pokemon_2"]["status"] = {"FNT": ""}
            state["phase_3"]["pokemon_2"]["status"] = {"FNT": ""}
        state["phase_3"]["logs"].append({"content": "{} wins.".format(user._species if not user.isfaint() else oppo._species)})

    return state


app = Flask(__name__)
CORS(app)


oppo_pool = {
    # "Ceruledge": "937Ceruledge.png",
    "Blaziken": "257Blaziken-Mega.png",
    # "Tyranitar": "248Tyranitar.png",
    # "Aerodactyl": "142Aerodactyl-Mega.png",
    "TingLu": "1003Ting-Lu.png",
    # "Scizor": "212Scizor.png",
    "Lucario": "448Lucario.png",
    # "ChenLoong": "131Lapras.png",
    # "RedMoon": "373Salamence-Mega.png",
    # "Zapdos": "145Zapdos.png",
    "Graphal": "Graphal.webp"
}


@app.route("/init-state", methods=["POST"])
def init_state():
    global user, oppo, battle

    init_data = request.get_json()
    print(init_data)
    user = create_role("asset.user.{}".format(init_data["species"]))
    t = rndc(oppo_pool)
    try:
        oppo = {
            "Blaziken": BlazikenAgent(),
            "Lucario": LucarioAgent(),
            "TingLu": TingLuAgent(),
            "Graphal": GraphalAgent()
        }[t]
    except KeyError:
        oppo = create_role("asset.user.{}".format(t))
    battle = Battle(user, oppo)

    battle.start()
    state = {
        "pokemon_1": deepcopy(user.state),
        "pokemon_2": deepcopy(oppo.state),
    }
    state["logs"] = battle.get_logs()
    moves = {}
    for i, (k, v) in enumerate(user._moves.items()):
        moves["move_%s" % (i + 1)] = v
    state["pokemon_1"].update(moves)

    state["pokemon_2"]["species"] = oppo._species
    state["pokemon_2"]["avatar"] = oppo_pool[n2f(oppo._species)]
    state["code"] = read("asset/user/{}.py".format(init_data["species"])) + "\n\n\n\n\n\n"

    script = read_json("asset/user/{}.json".format(init_data["species"]))
    for i, k in enumerate(script["moves"]):
        state["pokemon_1"]["move_%s" % (i + 1)]["effect"] = script["moves"][k]["effect"]

    return jsonify(state)

@app.route("/get-state")
def get_state():
    move_id = request.args.get("move_id")
    state = step(move_id)

    print(state)
    return jsonify(state)


if __name__ == "__main__":
    app.run(debug=True)
