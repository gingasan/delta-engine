from utils import *


class PokemonBase:
    _species='Mew'
    _types=['Normal']
    _gender='Male'
    _move_1=('Earthquake',100,100,'Physical','Normal',0,[])
    _base=(100,100,100,100,100,100)
    def __init__(self):
        self.state = self.init_state()

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
        self.side_id = None

        self.logger = None

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
            "act": None, "act_taken": None, "canact": True,
            "last_act": None, "last_act_taken": None,
        }

    def __getitem__(self, x):
        if hasattr(self, x):
            return getattr(self, x)
        elif x in self.state:
            return self.state[x]
        return None

    def get_moves(self):
        available_move_ids = []
        disabled = self.target.get_disable_moves(self._moves)
        for m in self._moves:
            if m not in disabled:
                available_move_ids += [m]
        return available_move_ids

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

    def move_1(self): # Earthquake
        damage_ret = self.get_damage()
        if not damage_ret["miss"]:
            damage = damage_ret["damage"]
            self.target.take_damage(damage)
    
    def get_weather_power_mult(self):
        if self.env.get("Sunlight") and self["act"]["type"] in ["Fire", "Water"]:
            return {"Fire": 1.5, "Water": 0.5}[self["act"]["type"]]
        if self.env.get("Rain") and self["act"]["type"] in ["Fire", "Water"]:
            return {"Fire": 0.5, "Water": 1.5}[self["act"]["type"]]
        if self.env.get("Electric Terrain") and self["act"]["type"] == "Electric":
            return 1.3
        if self.env.get("Grassy Terrain") and self["act"]["type"] == "Grass":
            return 1.3
        if self.env.get("Psychic Terrain") and self["act"]["type"] == "Psychic":
            return 1.3
        if self.env.get("Misty Terrain") and self["act"]["type"] == "Dragon":
            return 0.5
        return 1.

    def get_weather_stat_mult(self, key):
        if self.env.get("Sandstorm") and key == "spd" and self.istype("Rock"):
            return 1.5
        if self.env.get("Snow") and key == "def" and self.istype("Ice"):
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

    def get_base_damage(self, power, crit):
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
            damage_ret = {"miss": True}
            self.register_act_damage(damage_ret)
            self.log("Miss!")
            return damage_ret

        power = self.get_power()

        crit = self.get_crit()

        damage = self.get_base_damage(power, crit)

        # critical hit
        if crit:
            damage = int(damage * 1.5)

        # randomize
        damage = randomize(damage)

        # same type attack bonus (STAB)
        stab = self.get_stab()
        damage = int(damage * stab)
        
        # type effectiveness
        type_effect = self.get_type_effect()
        damage = int(damage * type_effect)

        # status, conditions, etc.
        status_mult = self.get_other_mult()
        damage = int(damage * status_mult)
    
        damage_ret = {
            "damage": damage,
            "crit": crit,
            "miss": False,
            "type_effect": type_effect,
        }
        self.register_act_damage(damage_ret)
        return damage_ret
    
    def get_confusion_damage(self):
        attack = self.get_stat("atk")
        defense = self.get_stat("def")
        level = 100
        power = 40
        base_damage = int(int(int(int(2 * level / 5 + 2) * power * attack) / defense) / 50) + 2

        return max(1, base_damage)

    def get_priority(self, move_id):
        return self._moves[move_id]["priority"]
    
    def _take_damage_attack(self, x):
        if "type_effect" in self.target["act"] and self.target["act"]["type_effect"] < 0.1:
            self.logger.log("It is immune by %s." % self._species)
            return
        self.register_act_taken()
        self.state["hp"] = max(0, self["hp"] - x)
        self.log(script="attack", species=self._species, x=x, **self["act_taken"])

    def _take_damage_loss(self, x):
        self.state["hp"] = max(0, self["hp"] - x)
        self.log("{} loses {} HP.".format(self._species, x))
    
    def _take_damage_recoil(self, x):
        self.state["hp"] = max(0, self["hp"] - x)
        self.log("{} loses {} HP from recoil.".format(self._species, x))

    def _restore_heal(self, x):
        self.state["hp"] = min(self["max_hp"], self["hp"] + x)
        self.log("{} heals {} HP.".format(self._species, x))

    def _restore_drain(self, x):
        self.state["hp"] = min(self["max_hp"], self["hp"] + x)
        self.log("{} drains {} HP from {}.".format(self._species, x, self.target._species))

    def log(self, content=None, **kwargs):
        self.logger.log(content, **kwargs)

    def get_logs(self):
        return self.logger.logs
    
    def init_env(self, env):
        self.env = env

    # public

    def isstatus(self, x):
        return x in self["status"] if self["status"] else False

    def istype(self, x):
        return x in self["types"]
    
    def isfaint(self):
        return self["status"] == "FNT" or self["hp"] < 1
    
    def take_damage(self, x, from_="attack"):
        if from_ == "attack":
            self._take_damage_attack(x)
        elif from_ == "loss":
            self._take_damage_loss(x)
        elif from_ == "recoil":
            self._take_damage_recoil(x)
        if self["hp"] == 0:
            self.state["status"] = "FNT"
            self.log("%s faints." % self._species)

    def restore(self, x, from_="heal"):
        if from_ == "heal":
            self._restore_heal(x)
        elif from_ == "drain":
            self._restore_drain(x)

    def set_status(self, x):
        if self["status"] or self.env.get("Misty Terrain"):
            return
        if x == "BRN":
            if not self.istype("Fire"):
                self.state["status"] = {x: {"counter": 0}}
        elif x == "PAR":
            if self.istype("Electric"):
                return
            self.state["status"] = {x: {"counter": 0}}
        elif x == "PSN":
            if self.istype("Poison") and not self.istype("Steel"):
                return
            self.state["status"] = {x: {"counter": 0}}
        elif x == "TOX":
            if self.istype("Poison") and not self.istype("Steel"):
                return
            self.state["status"] = {x: {"counter": 0}}
        elif x == "FRZ":
            if self.istype("Ice"):
                return
            self.state["status"] = {x: {"counter": 0}}
        elif x == "SLP":
            if self.env.get("Electric Terrain"):
                return
            self.state["status"] = {x: {"counter": 0}}
        self.log(script="status", species=self._species, x=x)

    def set_boost(self, key, x, from_="target"):
        bar = 6 if key in ["atk", "def", "spa", "spd", "spe"] else 3
        if x > 0:
            self["boosts"][key] = min(bar, self["boosts"][key] + x)
        else:
            self["boosts"][key] = max(-bar, self["boosts"][key] + x)
        self.log(script="boost", species=self._species, key=key, x=x)

    def set_stat(self, key, x, from_="target"):
        self["stats"][key] = int(self["stats"][key] * x)

    def set_condition(self, x, **kwargs):
        if not self["conditions"].get(x):
            self.state["conditions"].update({x: kwargs})
            if "broadcast" in kwargs:
                self.log(kwargs["broadcast"])

    def get_evasion(self):
        return 1

    def get_disable_moves(self, moves):
        target = self.target
        disabled = []
        return disabled


class Battle:
    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.env = Env()
        self.logger = Logger()
        self.turn = 0

        self.pokemon1.init_env(self.env)
        self.pokemon2.init_env(self.env)
        self.pokemon1.side_id = 0
        self.pokemon2.side_id = 1
        self.pokemon1.logger = self.logger
        self.pokemon2.logger = self.logger
        self.env.logger = self.logger

    def _act(self, source, target, move_id):
        if source["conditions"].get("Flinch"): # Flinch
            del source["conditions"]["Flinch"]
            self.log("%s cannot move because of flinch." % source._species)
            return
        if source["status"]: # Freeze & Paralysis & Sleep
            if source.isstatus("FRZ"):
                if rnd() < 0.2:
                    source.state["status"] = None
                    self.log("%s is recovered from Freeze." % source._species)
                else:
                    self.log("%s cannot move due to Freeze." % source._species)
                    return
            elif source.isstatus("PAR"):
                if rnd() < 0.25:
                    self.log("%s cannot move due to Paralysis." % source._species)
                    return
            elif source.isstatus("SLP"):
                wakeup_ratio = {0: 0.0, 1: 0.33, 2: 0.5, 3: 1.0}
                if rnd() < wakeup_ratio[source["status"]["SLP"]["counter"]]:
                    source.state["status"] = None
                    self.log("%s wakes up." % source._species)
                else:
                    source.state["status"]["SLP"]["counter"] += 1
                    self.log("%s is sleeping." % source._species)
                    return
        if source["conditions"].get("Confusion"): # Confusion
            if source["conditions"]["Confusion"]["counter"] == 4:
                del source["conditions"]["Confusion"]
                self.log("%s is out of confusion." % source._species)
            elif rnd() < 0.33:
                source.take_damage(source.get_confusion_damage(), "recoil")
                source["conditions"]["Confusion"]["counter"] += 2
                self.log("%s hurts itself in its confusion." % source._species)
                return
            else:
                source["conditions"]["Confusion"]["counter"] += 1
        source._act(move_id, target)
        return self.pokemon1.state, self.pokemon2.state

    def endturn(self):
        if self.pokemon1.isfaint() or self.pokemon2.isfaint():
            self.pokemon1.deregister()
            self.pokemon2.deregister()
            self.turn += 1
            return

        self.pokemon1.endturn()
        self.pokemon2.endturn()
        for p in [self.pokemon1, self.pokemon2]:
            if p["status"]: # Burn & Poison & Badly Poison
                if p.isstatus("BRN"):
                    p.take_damage(p["max_hp"] // 16, "loss")
                    self.log("%s is hurt by Burn." % p._species)
                elif p.isstatus("PSN"):
                    p.take_damage(p["max_hp"] // 8, "loss")
                    self.log("%s is hurt by Poison." % p._species)
                elif p.isstatus("TOX"):
                    p["status"]["TOX"]["counter"] += 1
                    p.take_damage(p["max_hp"] // 16 * p["status"]["TOX"]["counter"], "loss")
                    self.log("%s is hurt by Poison." % p._species)
            if p["conditions"].get("Flinch"): # Flinch
                del p["conditions"]["Flinch"]

        self.env.endturn()
        if self.env.get_weather("Sandstorm"):
            for p in [self.pokemon1, self.pokemon2]:
                if any([p.istype(x) for x in ["Rock", "Ground", "Steel"]]):
                    continue
                p.take_damage(p["max_hp"] // 16, "loss")
                self.log("%s is hurt by Sandstorm." % p._species)
        self.pokemon1.deregister()
        self.pokemon2.deregister()
        self.turn += 1

    def start(self):
        self.log("Battle starts: {} ({})\tV.S.\t{} ({}).".format(self.pokemon1._species, " & ".join(self.pokemon1._types), self.pokemon2._species, " & ".join(self.pokemon2._types)))
        self.pokemon1.target = PokemonWrapper(self.pokemon2)
        self.pokemon2.target = PokemonWrapper(self.pokemon1)
        self.pokemon1.onswitch()
        self.pokemon2.onswitch()
        self.turn += 1

    def movefirst(self, move1_id, move2_id):
        prio1 = self.pokemon1.get_priority(move1_id)
        prio2 = self.pokemon2.get_priority(move2_id)
        if prio1 != prio2:
            return ((self.pokemon1, move1_id), (self.pokemon2, move2_id)) if prio1 > prio2 else ((self.pokemon2, move2_id), (self.pokemon1, move1_id))
        speed1 = self.pokemon1.get_stat("spe")
        speed2 = self.pokemon2.get_stat("spe")
        if speed1 == speed2:
            speed1 = speed1 + 1 if rnd() < 0.5 else speed1 - 1
        if self.env.get_side_condition("Trick Room", side_id=0):
            speed1, speed2 = speed2, speed1
        return ((self.pokemon1, move1_id), (self.pokemon2, move2_id)) if speed1 > speed2 else ((self.pokemon2, move2_id), (self.pokemon1, move1_id))

    def act(self, move1_id, move2_id):
        self.log("-- Turn %d --" % self.turn)
        if self.pokemon1.isfaint() or self.pokemon2.isfaint():
            return {"wrap": True}
        ret = {
            "phase_1": None,
            "phase_2": None,
            "phase_3": {}
        }
        if isinstance(self.pokemon1["canact"], str):
            move1_id = self.pokemon1["canact"]
            self.pokemon1.state["canact"] = True
        if isinstance(self.pokemon2["canact"], str):
            move2_id = self.pokemon2["canact"]
            self.pokemon2.state["canact"] = True
        (t1, move1_id), (t2, move2_id) = self.movefirst(move1_id, move2_id)
        if t1["canact"]:
            ret["phase_1"] = {"attacker": t1._species, "defender": t2._species}
            self.log("{} uses {}.".format(t1._species, move1_id))
            self._act(t1, t2, move1_id)
            ret["phase_1"]["pokemon_1"] = deepcopy(self.pokemon1.state)
            ret["phase_1"]["pokemon_2"] = deepcopy(self.pokemon2.state)
            ret["phase_1"]["logs"] = deepcopy(self.get_logs())
            self.logger.clr()
        if not t2.isfaint() and t2["canact"]:
            ret["phase_2"] = {"attacker": t2._species, "defender": t1._species}
            self.log("{} uses {}.".format(t2._species, move2_id))
            self._act(t2, t1, move2_id)
            ret["phase_2"]["pokemon_1"] = deepcopy(self.pokemon1.state)
            ret["phase_2"]["pokemon_2"] = deepcopy(self.pokemon2.state)
            ret["phase_2"]["logs"] = deepcopy(self.get_logs())
            self.logger.clr()
        self.endturn()
        ret["phase_3"]["pokemon_1"] = deepcopy(self.pokemon1.state)
        ret["phase_3"]["pokemon_2"] = deepcopy(self.pokemon2.state)
        ret["phase_3"]["logs"] = deepcopy(self.get_logs())
        self.logger.clr()

        ret["wrap"] = True if self.pokemon1.isfaint() or self.pokemon2.isfaint() else False
        return ret

    def log(self, content, **kwargs):
        self.logger.log(content, **kwargs)

    def get_logs(self):
        return self.logger.logs


class Env:
    def __init__(self):
        self.weather = {}
        self.terrain = {}
        self.side_conditions = [{}, {}]
        self.logger = None

    @property
    def _weather(self):
        return get_keys(self.weather)[0]

    @property
    def _terrain(self):
        return get_keys(self.terrain)[0]

    def clr_weather(self):
        self.log("{} ends.".format(self._weather))
        self.weather = {}

    def clr_terrain(self):
        self.log("{} ends.".format(self._terrain))
        self.terrain = {}

    def set_weather(self, x, from_, **kwargs):
        if self.weather:
            self.clr_weather()
        self.weather[x] = {"counter": 0, "max_count": kwargs.get("max_count", 5), "from_": from_}
        self.log("{} summons {}.".format(from_, x))

    def set_terrain(self, x, from_, **kwargs):
        if self.terrain:
            self.clr_terrain()
        self.terrain[x] = {"counter": 0, "max_count": kwargs.get("max_count", 5), "from_": from_}
        self.log("{} summons {}.".format(from_, x))

    def get_weather(self, x):
        if x in self.weather:
            return self.weather[x]

    def get_terrain(self, x):
        if x in self.terrain:
            return self.terrain[x]

    def get(self, x):
        if x in CFG["weather"]:
            return self.get_weather(x)
        if x in CFG["terrain"]:
            return self.get_terrain(x)

    def set_side_condition(self, x, side_id, from_, **kwargs):
        if not self.side_conditions[side_id].get(x):
            self.side_conditions[side_id].update({x: kwargs})
            self.side_conditions[side_id][x]["from_"] = from_
            self.log("{} summons {}.".format(from_, x))

    def get_side_condition(self, x, side_id):
        if x in self.side_conditions[side_id]:
            return self.side_conditions[side_id][x]
        
    def remove(self, x, side_id=None):
        if side_id is not None:
            if x in self.side_conditions[side_id]:
                del self.side_conditions[side_id][x]
                self.log("{} ends.".format(x))
        else:
            if x in CFG["weather"]:
                self.clr_weather()
            if x in CFG["terrain"]:
                self.clr_terrain()

    def endturn(self):
        if self.weather:
            self.weather[self._weather]["counter"] += 1
            if self.weather[self._weather]["counter"] == self.weather[self._weather]["max_count"]:
                self.clr_weather()
        if self.terrain:
            self.terrain[self._terrain]["counter"] += 1
            if self.terrain[self._terrain]["counter"] == self.terrain[self._terrain]["max_count"]:
                self.clr_terrain()
        for i in range(2):
            for k in get_keys(self.side_conditions[i]):
                v = self.side_conditions[i][k]
                if "max_count" in v:
                    v["counter"] += 1
                    if v["counter"] == v["max_count"]:
                        del self.side_conditions[i][k]
                        self.log("{} ends.".format(k))

    def log(self, content=None, **kwargs):
        self.logger.log(content, **kwargs)

    @property
    def state(self):
        return {
            "weather": self.weather,
            "terrain": self.terrain,
            "side_conditions": self.side_conditions
        }


class Logger:
    def __init__(self):
        self.logs = []

    def clr(self):
        del self.logs[:]

    def log(self, content=None, script=None, **kwargs):
        if script == "attack":
            self._log_attack(**kwargs)
        elif script == "boost":
            self._log_boost(**kwargs)
        elif script == "status":
            self._log_status(**kwargs)
        else:
            line = {"content": content}
            line.update(kwargs)
            self.logs.append(line)

    def _log_attack(self, **kwargs):
        content = "{} loses {} HP.".format(kwargs["species"], kwargs["x"]) 
        if kwargs.get("damage", 0) == 0:
            return
        if kwargs["crit"]:
            self.log("A critical hit!")
        if kwargs["type_effect"] > 1:
            self.log(" ".join(["Super effective.", content]))
        elif kwargs["type_effect"] < 1:
            self.log(" ".join(["Not very effective.", content]))
        else:
            self.log(content)
    
    def _log_boost(self, **kwargs):
        key = {
            "atk": "Atk.", "def": "Def.", "spa": "SpA.", "spd": "SpD.", "spe": "Spd.",
            "accuracy": "Acc.", "crit": "Crit."}[kwargs["key"]]
        self.log("{}'s {} is {} by {}.".format(kwargs["species"], key, "raised" if kwargs["x"] > 0 else "lowered", abs(kwargs["x"])))

    def _log_status(self, **kwargs):
        if kwargs["x"] == "BRN":
            self.log("%s is burned." % kwargs["species"])
        elif kwargs["x"] == "PAR":
            self.log("%s is paralyzed." % kwargs["species"])
        elif kwargs["x"] == "PSN":
            self.log("%s is poisoned." % kwargs["species"])
        elif kwargs["x"] == "TOX":
            self.log("%s is badly poisoned." % kwargs["species"])
        elif kwargs["x"] == "FRZ":
            self.log("%s is frozen." % kwargs["species"])
        elif kwargs["x"] == "SLP":
            self.log("%s falls asleep." % kwargs["species"])


class PokemonWrapper:
    def __init__(self, pokemon):
        self.__pokemon = pokemon
        self._species = pokemon._species
        self.public_list = [
            "isstatus", "istype", "isfaint",
            "take_damage", "restore",
            "set_status", "set_boost", "set_stat", "set_condition",
            "get_evasion", "get_disable_moves", "get_stat",
            "side_id"
        ]

    @property
    def state(self):
        return {
            "types":  self.__pokemon["types"],
            "status": self.__pokemon["status"],
            "hp": self.__pokemon["hp"], "max_hp": self.__pokemon["max_hp"], "hp_ratio": self.__pokemon["hp"] / self.__pokemon["max_hp"] * 100,
            "boosts": {k: self.__pokemon["boosts"][k] for k in ["atk", "def", "spa", "spd", "spe", "accuracy", "crit"]},
            "conditions": self.__pokemon["conditions"],
            "act": self.__pokemon["act"], "act_taken": self.__pokemon["act_taken"],
            "last_act": self.__pokemon["last_act"], "last_act_taken": self.__pokemon["last_act_taken"],
        }

    def __getitem__(self, x):
        if x in self.state:
            return self.state[x]
        return None

    def __getattr__(self, x):
        if x in self.public_list:
            return getattr(self.__pokemon, x)
        else:
            raise NotImplementedError

    def unwrap(self, obj):
        if isinstance(obj, Battle):
            return self.__pokemon


def Increment(cls, attr=None):
    def increment(fct):
        if not attr:
            setattr(cls, fct.__name__, fct)
        else:
            setattr(cls, attr, fct())
        return fct
    return increment
