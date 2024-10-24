from flask import Flask, jsonify, request
from flask_cors import CORS
from engine import *
from utils import *
from agent import *
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


load_from="model/cg7_v101"
load_model_path = "google/codegemma-7b-it"
model = AutoModelForCausalLM.from_pretrained(load_model_path, cache_dir="../cache")
model = PeftModel.from_pretrained(model, load_from)
model.cuda(2)
tokenizer = AutoTokenizer.from_pretrained(load_model_path, padding_side="left", cache_dir="../cache", use_fast=True)


app = Flask(__name__)
CORS(app)


ROLES = read_json("game_config/roles.json")


INSTRUCTION = """
You are a game programmer for Pokemon. You are tasked to finish either of the following two tasks.
1. I will give you a json script that details a pokemon role. Generate its python implementation.
2. I will give you an updated json script of the pokemon role and its previous python implementation. Generate the incremental code based on the previous implementation. You can overload methods or add new ones.
""".strip()
INPUT1 = """
Role script:
```json
{}
```
""".strip()
INPUT2 = """
Previous implementation:
```python
{}
```
""".strip()


def inference(script, code=""):
    if code == "":
        text = "<|im_start|>system\n{}<|im_end|>\n<|im_start|>user\n{}<|im_end|>\n<|im_start|>assistant\n".format(INSTRUCTION, INPUT1.format(json.dumps(script, indent=2)))
    else:
        text = "<|im_start|>system\n{}<|im_end|>\n<|im_start|>user\n{}<|im_end|>\n<|im_start|>assistant\n".format(INSTRUCTION, "\n\n".join([INPUT1.format(json.dumps(script, indent=2)), INPUT2.format(code)]))
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    input_ids = input_ids.cuda(2)
    outputs = model.generate(input_ids=input_ids, max_new_tokens=1000, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id)

    return tokenizer.decode(outputs[0][:-1]).split("assistant")[-1].split("<|im_end|>")[0].strip()


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


@app.route("/init-state", methods=["POST"])
def init_state():
    global user, oppo, battle

    init_data = request.get_json()
    print(init_data)

    script = {
        "species": init_data["species"],
        "types": [
            init_data["type1"],
            init_data["type2"]
        ],
        "ability": {
            init_data["ability-name"]: init_data["ability-effect"]
        },
        "moves": {
            init_data["move1-name"]: {
                "power": init_data["move1-power"],
                "accuracy": init_data["move1-accuracy"],
                "category": init_data["move1-category"],
                "type": init_data["move1-type"],
                "effect": init_data["move1-effect"],
                "priority": init_data["move1-priority"],
                "property": init_data["move1-property"]
            },
            init_data["move2-name"]: {
                "power": init_data["move2-power"],
                "accuracy": init_data["move2-accuracy"],
                "category": init_data["move2-category"],
                "type": init_data["move2-type"],
                "effect": init_data["move2-effect"],
                "priority": init_data["move2-priority"],
                "property": init_data["move2-property"]
            },
            init_data["move3-name"]: {
                "power": init_data["move3-power"],
                "accuracy": init_data["move3-accuracy"],
                "category": init_data["move3-category"],
                "type": init_data["move3-type"],
                "effect": init_data["move3-effect"],
                "priority": init_data["move3-priority"],
                "property": init_data["move3-property"]
            },
            init_data["move4-name"]: {
                "power": init_data["move4-power"],
                "accuracy": init_data["move4-accuracy"],
                "category": init_data["move4-category"],
                "type": init_data["move4-type"],
                "effect": init_data["move4-effect"],
                "priority": init_data["move4-priority"],
                "property": init_data["move4-property"]
            }
        }
    }
    print(script)

    code = inference(script)
    code = code.strip("```python\\n").strip()
    write(code, "ugc/tmp/{}.py".format(script["species"]))

    user = create_role("ugc.tmp.{}".format(init_data["species"]))
    # user = create_role("ugc.tmp.Neos")
    t = rndc(ROLES)
    try:
        oppo = {
            "Blaziken": BlazikenAgent(),
            "Lucario": LucarioAgent(),
            "TingLu": TingLuAgent(),
            "Graphal": GraphalAgent()
        }[ROLES[t]["class_name"]]
    except KeyError:
        oppo = create_role("asset.user.{}".format(ROLES[t]["class_name"]))
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
    state["pokemon_2"]["avatar"] = ROLES[oppo._species]["avatar"]
    state["code"] = code + "\n\n\n\n\n\n"
    # state["code"] = read("asset/user/{}.py".format(init_data["species"])) + "\n\n\n\n\n\n"

    # script = read_json("asset/user/{}.json".format(init_data["species"]))
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
