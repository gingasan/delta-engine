from engine import *
from utils import *



def create_role(code_path):
    code = (
        "from {} import *\n"
        "pokemon={}()"
    ).format(code_path, code_path.split(".")[-1])
    global_vars = {}
    exec(code, global_vars)
    role = global_vars["pokemon"]
    return role


def fct1(battle):
    return {
        "pokemon_user": {
            "species": battle.pokemon1._species,
            "types": battle.pokemon1._types,
            "gender": battle.pokemon1._gender,
            "ability": battle.pokemon1._ability,
            "moves": battle.pokemon1._moves,
            "state": battle.pokemon1.state
        },
        "pokemon_oppo": {
            "species": battle.pokemon2._species,
            "types": battle.pokemon2._types,
            "gender": battle.pokemon2._gender,
            "ability": battle.pokemon2._ability,
            "moves": battle.pokemon2._moves,
            "state": battle.pokemon2.state
        }
    }

def fct2(battle, move_user, move_oppo):
    battle.act(move_user, move_oppo)
    return {
        "pokemon_user": {
            "species": battle.pokemon1._species,
            "types": battle.pokemon1._types,
            "gender": battle.pokemon1._gender,
            "ability": battle.pokemon1._ability,
            "moves": battle.pokemon1._moves,
            "state": battle.pokemon1.state
        },
        "pokemon_oppo": {
            "species": battle.pokemon2._species,
            "types": battle.pokemon2._types,
            "gender": battle.pokemon2._gender,
            "ability": battle.pokemon2._ability,
            "moves": battle.pokemon2._moves,
            "state": battle.pokemon2.state
        }
    }

def fct3(battle):
    flag = battle.endturn()
    if flag:
        return {
            "BattleEnd": True,
            "Winner": battle.pokemon1._species if not battle.pokemon1.isfaint() else battle.pokemon2._species
        }
    else:
        return {
            "BattleEnd": False,
            "Winner": ""
        }


role = create_role("asset.{}.{}".format("ginga", "Graphal"))
oppo = create_role("asset.{}.{}".format("ginga", "Graphal"))
battle = Battle(role, oppo)
battle.start()
