from utils import *


class Battle:
    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.env = {}
        self.pokemon1.init_env(self.env)
        self.pokemon2.init_env(self.env)

    def _act(self, source, target, move_id):
        if source["conditions"].get("FLINCH"): # Flinch
            del source["conditions"]["FLINCH"]
            return
        if source["status"]: # Freeze & Paralysis & Sleep
            if source.isstatus("FRZ"):
                if rnd() < 0.2:
                    source.state["status"] = None
                else:
                    return
            elif source.isstatus("PAR"):
                if rnd() < 0.25:
                    return
            elif source.isstatus("SLP"):
                wakeup_ratio = {0: 0.0, 1: 0.33, 2: 0.5, 3: 1.0}
                if rnd() < wakeup_ratio[source["status"]["SLP"]["counter"]]:
                    source.state["status"] = None
                else:
                    source.state["status"]["SLP"]["counter"] += 1
                    return
        if source["conditions"].get("CONFUSION"): # Confusion
            if source["conditions"]["CONFUSION"]["counter"] == 4:
                del source["conditions"]["CONFUSION"]
            elif rnd() < 0.33:
                source.take_damage(source.get_confusion_damage(), "recoil")
                source["conditions"]["CONFUSION"]["counter"] += 1
                return
            else:
                source["conditions"]["CONFUSION"]["counter"] += 1
        source._act(move_id, target)

    def endturn(self):
        if self.pokemon1.isfaint() or self.pokemon2.isfaint():
            self.pokemon1.deregister()
            self.pokemon2.deregister()
            return self.pokemon1, self.pokemon2
        self.pokemon1.endturn()
        self.pokemon2.endturn()
        for p in [self.pokemon1, self.pokemon2]:
            if p["status"]: # Burn & Poison & Badly Poison
                if p.isstatus("BRN"):
                    p.take_damage(p["max_hp"] // 16, "loss")
                elif p.isstatus("PSN"):
                    p.take_damage(p["max_hp"] // 8, "loss")
                elif p.isstatus("TOX"):
                    p["status"]["TOX"]["counter"] += 1
                    p.take_damage(p["max_hp"] // 16 * p["status"]["TOX"]["counter"], "loss")
            if p["conditions"].get("FLINCH"): # Flinch
                del p["conditions"]["FLINCH"]

        self._count()
        self.pokemon1.deregister()
        self.pokemon2.deregister()

    def start(self):
        self.pokemon1.target = self.pokemon2
        self.pokemon2.target = self.pokemon1
        self.pokemon1.onswitch()
        self.pokemon2.onswitch()

    def _count(self):
        del_list = []
        for k, v in self.env.items():
            if "counter" in v:
                v["counter"] += 1
                if v["counter"] == v["max_count"]:
                    del_list += [k]
        for k in del_list:
            del self.env[k]
        for p in [self.pokemon1, self.pokemon2]:
            del del_list[:]
            for k, v in p["side_conditions"].items():
                if v.get("max_count"):
                    v["counter"] += 1
                    if v["counter"] == v["max_count"]:
                        del_list += [k]
            for k in del_list:
                del p["side_conditions"][k]
        if self.env.get("SANDSTORM"):
            for p in [self.pokemon1, self.pokemon2]:
                if any([x in p["types"] for x in ["Rock", "Ground", "Steel"]]):
                    continue
                p.take_damage(p["max_hp"] // 16, "loss")
        if self.env.get("HAIL"):
            for p in [self.pokemon1, self.pokemon2]:
                if "Ice" in p["types"]:
                    continue
                p.take_damage(p["max_hp"] // 16, "loss")

    def movefirst(self, move1_id, move2_id):
        prio1 = self.pokemon1.get_priority(move1_id)
        prio2 = self.pokemon2.get_priority(move2_id)
        if prio1 != prio2:
            return ((self.pokemon1, move1_id), (self.pokemon2, move2_id)) if prio1 > prio2 else ((self.pokemon2, move2_id), (self.pokemon1, move1_id))
        speed1 = self.pokemon1.get_stat("spe")
        speed2 = self.pokemon2.get_stat("spe")
        if speed1 == speed2:
            speed1 = speed1 + 1 if rnd() < 0.5 else speed1 - 1
        if self.env.get("TRICK_ROOM"):
            speed1, speed2 = speed2, speed1
        return ((self.pokemon1, move1_id), (self.pokemon2, move2_id)) if speed1 > speed2 else ((self.pokemon2, move2_id), (self.pokemon1, move1_id))
    
    def act(self, move1_id, move2_id):
        if isinstance(self.pokemon1["canact"], str):
            move1_id = self.pokemon1["canact"]
            self.pokemon1.state["canact"] = True
        if isinstance(self.pokemon2["canact"], str):
            move2_id = self.pokemon2["canact"]
            self.pokemon2.state["canact"] = True
        (t1, move1_id), (t2, move2_id) = self.movefirst(move1_id, move2_id)
        if t1["canact"]:
            self._act(t1, t2, move1_id)
        if not t2.isfaint() and t2["canact"]:
            self._act(t2, t1, move2_id)


class PokemonBase:
    _species='Arceus'
    _types=['Normal']
    _gender='Male'
    _move_1=('Earthquake',100,100,'Physical','Normal',0,[])
    _base=(100,100,100,100,100,100)
    def __init__(self, state=None):
        self.state = self.init_state() if not state else state

        self.move2fct = {}
        self._moves = {}
        i = 1
        while self["_move_%d" % i]:
            move = self["_move_%d" % i]
            self.move2fct[move[0]] = self["move_%d" % i]
            self._moves[move[0]] = {"id": move[0], "power": move[1], "accuracy": move[2], "category": move[3], "type": move[4], "priority": move[5], "property": move[6]}
            i += 1

        self.env = None
        self.target = None

    @staticmethod
    def get_attrs(base_stats):
        level = 100
        iv = 31
        ev = 252
        stats = {s: 0 for s in ["hp", "atk", "def", "spa", "spd", "spe"]}
        for i, stat in enumerate(stats):
            base = base_stats[i]
            if stat == "hp":
                stats[stat] = int((base * 2 + iv + int(ev * 0.25)) * level * 0.01) + 10 + level
            else:
                stats[stat] = int((base * 2 + iv + int(ev * 0.25)) * level * 0.01) + 5
        return stats

    def init_state(self):
        attrs = self.get_attrs(self._base)
        return {
            "types": [t for t in self._types],
            "status": None,
            "hp": attrs["hp"], "max_hp": attrs["hp"],
            "stats": {k: v for k, v in attrs.items() if k != "hp"},
            "boosts": {k: 0 for k in ["atk", "def", "spa", "spd", "spe", "accuracy", "crit"]},
            "conditions": {},
            "side_conditions": {},
            "act": None, "act_taken": None, "canact": True,
            "last_act": None, "last_act_taken": None,
        }

    @property
    def sum(self):
        info = {
            "species": self._species,
            "hp": self["hp"], "max_hp": self["max_hp"],
            "status": "",
            "boosts": "",
            "conditions": " ".join(self["conditions"].keys()) if self["conditions"] else "",
            "side_conditions": " ".join(self["side_conditions"].keys()) if self["side_conditions"] else ""
        }
        for k, v in self["boosts"].items():
            if v == 0:
                continue
            info["boosts"] += " {}{}{}".format(k, "+" if v > 0 else "-", abs(v))
        info["boosts"] = info["boosts"].strip()
        if self["status"]:
            try:
                info["status"] = list(self["status"].keys())[0]
            except AttributeError:
                info["status"] = self["status"]
        return "{species}|{hp}/{max_hp}|{status}|{boosts}|{conditions}|{side_conditions}".format_map(info)
    
    def __getitem__(self, x):
        if hasattr(self, x):
            return getattr(self, x)
        elif x in self.state:
            return self.state[x]
        return None

    def get_moves(self):
        available_move_ids = []
        disabled = self.target.disable_moves(self._moves)
        for m in self._moves:
            if m not in disabled:
                available_move_ids += [m]
        return available_move_ids

    def disable_moves(self, moves):
        target = self.target
        disabled = []
        return disabled

    def onswitch(self):
        pass

    def endturn(self):
        pass

    def register_act(self, move_id, target):
        self.state["act"] = deepcopy(self._moves[move_id])
    
    def register_act_damage(self, damage_ret):
        self.state["act"].update(damage_ret)
    
    def register_act_taken(self):
        self.state["act_taken"] = deepcopy(self.target["act"])
    
    def deregister(self):
        self.state["last_act"] = deepcopy(self.state["act"])
        self.state["last_act_taken"] = deepcopy(self.state["act_taken"])
        self.state["act"] = None
        self.state["act_taken"] = None

    def _act(self, move_id, target):
        assert move_id in self.move2fct
        self.register_act(move_id, target)
        self.move2fct[move_id]()

    def init_env(self, env):
        self.env = env

    def move_1(self): # Earthquake
        damage_ret = self.get_damage()
        if not damage_ret["miss"]:
            damage = damage_ret["damage"]
            self.target.take_damage(damage)

    def set_env(self, x, max_count=5):
        if self.env.get(x):
            return
        def set_weather():
            for k in CFG["weather"]:
                if k in self.env:
                    del self.env[k]
            self.env[x] = {"counter": 0, "max_count": max_count}
        def set_terrain():
            for k in CFG["terrain"]:
                if k in self.env:
                    del self.env[k]
            self.env[x] = {"counter": 0, "max_count": max_count}

        if x in CFG["weather"]:
            set_weather()
        elif x in CFG["terrain"]:
            set_terrain()
        else:
            self.env[x] = {"counter": 0, "max_count": max_count}
    
    def get_weather_power_mult(self):
        if self.env.get("SUNNYDAY"):
            if self["act"]["type"] in ["Fire", "Water"]:
                return {"Fire": 1.5, "Water": 0.5}[self["act"]["type"]]
        if self.env.get("RAINDANCE"):
            if self["act"]["type"] in ["Fire", "Water"]:
                return {"Fire": 0.5, "Water": 1.5}[self["act"]["type"]]
        if self.env.get("ELECTRIC_TERRAIN"):
            if self["act"]["type"] == "Electric":
                return 1.3
        if self.env.get("GRASSY_TERRAIN"):
            if self["act"]["type"] == "Grass":
                return 1.3
        if self.env.get("PSYCHIC_TERRAIN"):
            if self["act"]["type"] == "Psychic":
                return 1.3
        if self.env.get("MISTY_TERRAIN"):
            if self["act"]["type"] == "Dragon":
                return 0.5
        return 1.

    def get_weather_stat_mult(self, key):
        if self.env.get("SANDSTORM") and key == "spd" and "Rock" in self["types"]:
            return 1.5
        if self.env.get("SNOW") and key == "def" and "Ice" in self["types"]:
            return 1.5
        return 1.
    
    def get_other_mult(self):
        if self.isstatus("BRN") and self["act"]["category"] == "Physical":
            return 0.5
        return 1.
    
    def get_crit(self):
        crit_mult = [0, 24, 8, 2, 1]
        crit_ratio = self["boosts"]["crit"]
        crit = False
        if rnd() * crit_mult[crit_ratio + 1] < 1:
            crit = True
        return crit

    def get_power(self):
        power = self["act"]["power"]
        return int(power * self.get_weather_power_mult())

    def get_stat(self, key, boost=None):
        stat = self["stats"][key]
        boost = self["boosts"][key] if not boost else boost
        stat_ratio = {0: 1, 1: 1.5, 2: 2, 3: 2.5, 4: 3, 5: 3.5, 6: 4}[min(6, abs(boost))]
        if boost < 0:
            stat_ratio = 1 / stat_ratio
        stat_ratio *= self.get_weather_stat_mult(key)
        if key == "spe" and self.isstatus("PAR"):
            stat_ratio *= 0.5
        return int(stat * stat_ratio)

    def get_type_effect(self):
        move_type = self["act"]["type"]
        target_types = self.target["types"]
        effect = 1
        for tt in target_types:
            effect *= TYPEEFFECTIVENESS[move_type][tt]
        return effect

    def get_stab(self):
        stab = 1
        if self["act"]["type"] in self["types"]:
            stab = 1.5
        return stab

    def get_accuracy(self):
        acc = self["act"]["accuracy"]
        acc_mult = [1.0, 1.33, 1.67, 2.0]
        if self["boosts"]["accuracy"] >= 0:
            acc *= acc_mult[self["boosts"]["accuracy"]]
        else:
            acc /= acc_mult[self["boosts"]["accuracy"]]
        acc *= self.target.get_evasion()
        return acc / 100

    def get_evasion(self):
        return 1

    def _get_base_damage(self, power, crit):
        atk_boost = self["boosts"]["atk"] if self["act"]["category"] == "Physical" else self["boosts"]["spa"]
        def_boost = self.target["boosts"]["def"] if self["act"]["category"] == "Physical" else self.target["boosts"]["spd"]
        
        if crit:
            atk_boost = max(0, atk_boost)
            def_boost = min(0, def_boost)

        attack = self.get_stat("atk" if self["act"]["category"] == "Physical" else "spa", atk_boost)
        defense = self.target.get_stat("def" if self["act"]["category"] == "Physical" else "spd", def_boost)

        level = 100
        base_damage = int(int(int(int(2 * level / 5 + 2) * power * attack) / defense) / 50) + 2

        return base_damage

    def get_damage(self):
        accuracy = self.get_accuracy()
        if rnd() >= accuracy:
            self.register_act_damage({"miss": True})
            return {"miss": True}

        power = self.get_power()
        
        crit = self.get_crit()
        
        damage = self._get_base_damage(power, crit)

        # critical hit
        if crit:
            damage = int(damage * 1.5)

        # randomize
        damage = randomize(damage)

        # same type attack bonus (STAB)
        stab = self.get_stab()
        damage = int(damage * stab)
        
        # type effectiveness
        type_efc = self.get_type_effect()
        damage = int(damage * type_efc)

        # status, side conditions, etc.
        status_mult = self.get_other_mult()
        damage = int(damage * status_mult)
        
        damage_ret = {
            "damage": damage,
            "crit": crit,
            "miss": False,
            "type_efc": type_efc,
        }
        self.register_act_damage(damage_ret)
        return damage_ret
    
    def take_damage(self, x, from_="attack"):
        if from_ == "attack":
            self._take_damage_attack(x)
        elif from_ == "loss":
            self._take_damage_loss(x)
        elif from_ == "recoil":
            self._take_damage_recoil(x)

    def _take_damage_attack(self, x):
        self.register_act_taken()
        self.state["hp"] = max(0, self["hp"] - x)
        if self["hp"] == 0:
            self.state["status"] = "FNT"

    def _take_damage_loss(self, x):
        self.state["hp"] = max(0, self["hp"] - x)
        if self["hp"] == 0:
            self.state["status"] = "FNT"
    
    def _take_damage_recoil(self, x):
        self.state["hp"] = max(0, self["hp"] - x)
        if self["hp"] == 0:
            self.state["status"] = "FNT"

    def restore(self, x, from_="heal"):
        if from_ == "heal":
            self._restore_heal(x)
        elif from_ == "drain":
            self._restore_drain(x)

    def _restore_heal(self, x):
        self.state["hp"] = min(self["max_hp"], self["hp"] + x)

    def _restore_drain(self, x):
        self.state["hp"] = min(self["max_hp"], self["hp"] + x)

    def set_status(self, x):
        if self["status"] or self.env.get("MISTY_TERRAIN"):
            return
        if x == "BRN":
            if not self.istype("Fire"):
                self.state["status"] = {x: {"counter": 0}}
        elif x == "PAR":
            if not self.istype("Electric"):
                self.state["status"] = {x: {"counter": 0}}
        elif x == "PSN":
            if not self.istype("Poison") and not self.istype("Steel"):
                self.state["status"] = {x: {"counter": 0}}
        elif x == "TOX":
            if not self.istype("Poison") and not self.istype("Steel"):
                self.state["status"] = {x: {"counter": 0}}
        elif x == "FRZ":
            if not self.istype("Ice"):
                self.state["status"] = {x: {"counter": 0}}
        elif x == "SLP":
            self.state["status"] = {x: {"counter": 0}}
    
    def isstatus(self, x):
        return x in self["status"] if self["status"] else False

    def istype(self, x):
        return x in self["types"]
    
    def set_boost(self, key, x, from_="target"):
        bar = 6 if key in ["atk", "def", "spa", "spd", "spe"] else 3
        if x > 0:
            self["boosts"][key] = min(bar, self["boosts"][key] + x)
        else:
            self["boosts"][key] = max(-bar, self["boosts"][key] + x)

    def set_stat(self, key, x):
        self["stats"][key] = int(self["stats"][key] * x)
    
    def set_condition(self, x, **kwargs):
        if not self["conditions"].get(x):
            self.state["conditions"].update({x: kwargs})
    
    def set_side_condition(self, x, **kwargs):
        if not self["side_conditions"].get(x):
            self.state["side_conditions"].update({x: kwargs})

    def isfaint(self):
        return self["status"] == "FNT" or self["hp"] < 1
    
    def get_confusion_damage(self):
        attack = self.get_stat("atk")
        defense = self.target.get_stat("def")
        level = 100
        power = 40
        base_damage = int(int(int(int(2 * level / 5 + 2) * power * attack) / defense) / 50) + 2
        
        return max(1, base_damage)

    def get_priority(self, move_id):
        return self._moves[move_id]["priority"]


def Increment(cls, attr=None):
    def increment(fct):
        if not attr:
            setattr(cls, fct.__name__, fct)
        else:
            setattr(cls, attr, fct())
        return fct
    return increment