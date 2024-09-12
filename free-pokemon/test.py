from engine import *
from utils import *
import argparse


def create_role(code_path):
    code = (
        "from {} import *\n"
        "pokemon={}()"
    ).format(code_path, code_path.split(".")[-1])
    global_vars = {}
    exec(code, global_vars)
    role = global_vars["pokemon"]
    return role


parser = argparse.ArgumentParser()
parser.add_argument("--user", type=str, default="user", help="User id.")
parser.add_argument("--role", type=str, default="Graphal", help="Name of the role.")
parser.add_argument("--oppo", type=str, default="Aerodactyl", help="Name of the opponent.")
args = parser.parse_args()


role = create_role("asset.{}.{}".format(args.user, args.role))
oppo = create_role("asset.{}.{}".format(args.user, args.oppo))
battle = Battle(role, oppo)

flag = None
turn = 0
battle.start()
while not flag:
    available_moves = {str(i + 1): m for i, m in enumerate(role.get_moves())}
    state1 = deepcopy(role.state)
    state2 = deepcopy(oppo.state)
    move1_id = available_moves[input("**\nChoose your move from:\n{}\n".format(available_moves))]
    move2_id = rndc(oppo.get_moves())
    data = battle.act(move1_id, move2_id)
    # print(data)
    flag = data["wrap"]
    print("**")
    for phase in ["phase-1", "phase-2", "phase-3"]:
        if data[phase]:
            for line in data[phase]["logs"]:
                print(line["content"])
    print("**\n")

    # print(role.sum)
    # print(oppo.sum)

print("\n**\nBattle is over. {} wins.\n**".format(role._species if not role.isfaint() else oppo._species))
