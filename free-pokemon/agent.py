from engine import *
from asset.user.Lucario import Lucario
from asset.user.Graphal import Graphal
from asset.user.TingLu import TingLu
from asset.user.Blaziken import Blaziken


class PokemonAgent(PokemonBase):
    def __init__(self):
        super().__init__()
        self.hist = None
        self.decision = None

    def step_0(self):
        self.hist = {m: 1.0 for m in self.get_moves()}

    def step_1(self):
        if rnd() < 0.5:
            self.hist[self.maxdamage_move] += 1

    def plan(self):
        i = 0
        while 1:
            step = "step_%d" % i
            if not hasattr(self, step):
                break
            getattr(self, step)()
            i += 1
        
        self.decision = self.choose(self.hist)

        return self.decision

    @property
    def maxdamage_move(self):
        ret = []
        for m in self.get_moves():
            move = self._moves[m]
            score = move["power"]
            for t in self.target["types"]:
                score *= TYPEEFFECTIVENESS[move["type"]][t]
            if self.istype(move["type"]):
                score *= 1.5
            if self.isstatus("BRN") and move["category"] == "Physical":
                score *= 0.5
            ret += [(m, int(score))]
        return max(ret, key=lambda x: x[1])[0]

    @staticmethod
    def weakness(target):
        ret = []
        for t in TYPEEFFECTIVENESS:
            effect = 1
            for tt in target["types"]:
                effect *= TYPEEFFECTIVENESS[t][tt]
            if effect > 1:
                ret += [t]
        return ret

    @staticmethod
    def immue_to(target, x):
        for t in target["types"]:
            if TYPEEFFECTIVENESS[x][t] < 0.1:
                return True
        return False
    
    @staticmethod
    def move_effect(move, target):
        move_type = move["type"]
        effect = 1
        for tt in target["types"]:
            effect *= TYPEEFFECTIVENESS[move_type][tt]
        return effect
    
    @staticmethod
    def sample(d):
        keys = get_keys(d)
        weights = get_values(d)

        total_weight = sum(weights)
        c_weights = []
        c = 0.0
        for weight in weights:
            c += weight
            c_weights.append(c)

        r = random.uniform(0, total_weight)
        for i, cumulative_weight in enumerate(c_weights):
            if r <= cumulative_weight:
                return keys[i]
    
    @staticmethod
    def choose(d):
        max_weight = max(get_values(d))
        max_keys = [k for k, v in d.items() if v == max_weight]
        return rndc(max_keys)


class LucarioAgent(PokemonAgent, Lucario):
    def __init__(self):
        super().__init__()

    def step_1(self):
        if not self["last_act"] or self["last_act"]["id"] != "Explore Mind":
            self.hist["Explore Mind"] += 1

            if all([self.move_effect(self._moves[m], self.target) <= 1 for m in self.get_moves()]) and \
                self["boosts"]["atk"] <= 0 or self["boosts"]["spa"] <= 0:
                self.hist["Explore Mind"] += 1

    def step_2(self):
        for m in ["Close Combat", "Aura Sphere", "Flash Cannon", "Shadow Ball"]:
            move = self._moves[m]
            self.hist[m] += self.move_effect(move, self.target)
            if self.istype(move["type"]):
                self.hist[m] += 1

    def step_3(self):
        if self.target["hp_ratio"] < 0.5:
            self.hist["Explore Mind"] -= 1

        if self["boosts"]["atk"] - self.target["boosts"]["def"] < 0 or \
            self["boosts"]["spa"] - self.target["boosts"]["spd"] < 0:
            self.hist["Explore Mind"] += 1

        if any([t in self.weakness(self) for t in self.target["types"]]):
            self.hist["Explore Mind"] -= 1

    def step_4(self):
        if self["last_act"] and self["last_act"]["id"] == "Close Combat":
            self.hist["Close Combat"] -= 1

    def step_5(self):
        if self.target["boosts"]["spd"] > 0:
            for m in self.get_moves():
                move = self._moves[m]
                if move["category"] == "Physical":
                    self.hist[m] += 1
                elif move["category"] == "Special":
                    self.hist[m] -= 1

    def step_6(self):
        if self.target["hp_ratio"] < 0.4 and not self.immue_to(self.target, "Normal"):
            self.hist["Extreme Speed"] += 2
            if self.target["boosts"]["def"] <=0 :
                self.hist["Extreme Speed"] += 1

            if self["hp"] / self["max_hp"] * 100 < 30:
                self.hist["Extreme Speed"] += 2
        else:
            self.hist["Extreme Speed"] -= 1

    def step_7(self):
        if min(get_values(self.hist)) == max(get_values(self.hist)) and not self.immue_to(self.target, "Fighting"):
            self.hist["Aura Sphere"] += 0.5

        if self.hist["Aura Sphere"] == self.hist["Close Combat"]:
            self.hist["Aura Sphere"] += 0.5

        if self.isstatus("BRN"):
            for m in self.get_moves():
                move = self._moves[m]
                if move["category"] == "Special":
                    self.hist[m] += 2
            self.hist["Close Combat"] -= 2


class GraphalAgent(PokemonAgent, Graphal):
    def __init__(self):
        super().__init__()

    def step_1(self):
        if not (self["boosts"]["spa"] > 0 and self["boosts"]["spe"] > 0):
            self.hist["Dark Dealings"] += 5

            if any(t in self.weakness(self) for t in self.target["types"]):
                self.hist["Dark Dealings"] -= 3

            if self.target["hp_ratio"] < 0.5:
                self.hist["Dark Dealings"] -= 1

    def step_2(self):
        for m in ["Dark Rainbow", "Flash Cannon"]:
            if m == "Dark Rainbow" and self.env.get_side_condition("Dark World", self.side_id):
                self.hist[m] += 1
            else:
                move = self._moves[m]
                self.hist[m] += self.move_effect(move, self.target)

        if self.env.get_side_condition("Dark World", self.side_id):
            self.hist["Dark Rainbow"] += 1

        if "Dark" in self.weakness(self.target):
            self.hist["Dark Rainbow"] += 2

        if self["last_act"] and self["last_act"]["id"] == "Dark Rainbow" and self["last_act"]["damage"] < self.target["max_hp"] // 2:
            self.hist["Dark Dealings"] += 2
            self.hist["Dark Rainbow"] -= 1

    def step_3(self):
        effect = self.move_effect(self._moves["Oblivion Wing"], self.target)
        if effect > 1:
            self.hist["Oblivion Wing"] += effect
        elif effect < 1:
            self.hist["Oblivion Wing"] -= 2

        if self["hp"] / self["max_hp"] < 0.5:
            self.hist["Oblivion Wing"] += 1

        if self.target["last_act"] and self.target["last_act"].get("damage", 0) > self["max_hp"] // 2:
            self.hist["Oblivion Wing"] += 1

    def step_4(self):
        if not self.env.get_side_condition("Dark World", self.side_id):
            self.hist["Dark World"] += 3

            if self["hp"] / self["max_hp"] < 0.3:
                self.hist["Dark World"] -= 1

    def step_5(self):
        if self.target["last_act"] and self.target["last_act"]["category"] == "Status":
            if not self.env.get_side_condition("Budokai",self.target.side_id):
                self.hist["Dark Budokai"] += 1
                if self.target["boosts"]["def"] > 0 and self.target["boosts"]["spd"] > 0:
                    self.hist["Dark Budokai"] += 2

    def step_6(self):
        if self.hist["Dark Rainbow"] == self.hist["Flash Cannon"]:
            self.hist["Dark Rainbow"] += 0.5


class TingLuAgent(PokemonAgent, TingLu):
    def __init__(self):
        super().__init__()

    def step_1(self):
        if self["boosts"]["def"] <= 0:
            self.hist["Ancient Curse"] += 1
        
            if any(t in self.weakness(self) for t in self.target["types"]):
                self.hist["Ancient Curse"] += 1

        if self.target["hp_ratio"] > 0.7:
            self.hist["Ruination"] += 2.5

            if all(self.move_effect(self._moves[m], self.target) <= 1 for m in self.get_moves()):
                self.hist["Ruination"] += 2
        else:
            self.hist["Ruination"] -= 1

    def step_2(self):
        for m in ["Earthquake", "Rock Slide", "Body Press"]:
            move = self._moves[m]
            self.hist[m] += self.move_effect(move, self.target)
            if self.target["boosts"]["def"] < 0:
                self.hist[m] += 1
            if self["boosts"]["atk"] > 1:
                self.hist[m] += 2

        if self.hist["Earthquake"] == self.hist["Rock Slide"]:
            self.hist["Earthquake"] += 0.5

    def step_3(self):
        if self["hp"] / self["max_hp"] < 0.5:
            self.hist["Sin-Absorb"] += 3

        if self.target["boosts"]["atk"] > 0 or self.target["boosts"]["spa"] > 0:
            self.hist["Sin-Absorb"] += 2

        if self["last_act"] and self["last_act"]["id"] == "Sin-Absorb":
            self.hist["Sin-Absorb"] -= 1
        
        if self.target["last_act"] and self.target["last_act"].get("damage", 0) < self["max_hp"] // 2:
            self.hist["Sin-Absorb"] -= 1
        else:
            self.hist["Sin-Absorb"] += 1

    def step_4(self):
        if self.target["boosts"]["atk"] > 0:
            self.hist["Ancient Curse"] += 1

    def step_5(self):
        if self["boosts"]["atk"] < 0 and not self.immue_to(self.target, "Fighting"):
            self.hist["Body Press"] += 1
            if self["boosts"]["atk"] < -1:
                self.hist["Body Press"] += 1

        if self["boosts"]["def"] > 0:
            self.hist["Body Press"] += 1

    def step_6(self):
        if self.env.get_side_condition("Aurora Veil", self.target.side_id) or \
            self.env.get_side_condition("Reflect", self.target.side_id):
            self.hist["Ancient Curse"] += 1

    def step_7(self):
        if self.isstatus("BRN"):
            for m in self.get_moves():
                move = self._moves[m]
                if move["category"] == "Physical":
                    self.hist[m] -= 1
                else:
                    self.hist[m] += 1

            self.hist["Sin-Absorb"] += 2

    def step_8(self):
        if self.target["hp_ratio"] < 0.3 and self["hp"] / self["max_hp"] > 0.8:
            self.hist["Sin-Absorb"] -= 2


class BlazikenAgent(PokemonAgent, Blaziken):
    def __init__(self):
        super().__init__()

    def step_1(self):
        if all(self.move_effect(self._moves[m], self.target) <= 1 for m in self.get_moves()) and \
            self["boosts"]["atk"] < 1:
            self.hist["Swords Dance"] += 2

        if self.target["boosts"]["def"] > 0:
            self.hist["Swords Dance"] += 1

        if self["boosts"]["atk"] < 0:
            self.hist["Swords Dance"] += 2
        
        if self["boosts"]["atk"] > 3:
            self.hist["Swords Dance"] -= 3

        if self["last_act"] and self["last_act"]["category"] != "Status" and \
            self["last_act"].get("damage", 0) < self.target["max_hp"] // 2:
            self.hist["Swords Dance"] += 2

        if self["hp"] / self["max_hp"] < 0.5:
            self.hist["Swords Dance"] -= 1

        if any(t in self.weakness(self) for t in self.target["types"]):
            self.hist["Swords Dance"] -= 1

    def step_2(self):
        for m in ["Blaze Kick II", "Double Kick II", "Thunder Punch", "Earthquake"]:
            if m not in self.get_moves():
                continue
            move = self._moves[m]
            effect = self.move_effect(move, self.target)
            if self.istype(move["type"]):
                effect += 0.5
            self.hist[m] += effect

        if self["hp"] / self["max_hp"] < 0.3:
            self.hist["Blaze Kick II"] += 0.5

    def step_3(self):
        if self["boosts"]["spe"] < 1:
            self.hist["Burning Bulwark"] += 1
            if not self["last_act"]:
                self.hist["Burning Bulwark"] += 1

        if not self.target.isstatus("BRN") and \
            self.target["last_act"] and self.target["last_act"]["category"] == "Physical":
            self.hist["Burning Bulwark"] += 2

            if self["hp"] / self["max_hp"] < 0.5:
                self.hist["Burning Bulwark"] += 1

        if self.target.istype("Fire"):
            self.hist["Burning Bulwark"] -= 1

        if self["last_act"] and self["last_act"]["id"] == "Burning Bulwark":
            self.hist["Burning Bulwark"] -= 3
