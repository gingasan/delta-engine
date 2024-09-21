from engine import *


class Deviljho(PokemonBase):
    _species='Deviljho'
    _types=['Dark','Dragon']
    _gender='Neutral'
    _ability=['Endless Hunger']
    _move_1=('Devour',80,100,'Physical','Dark',0,['contact','bite'])
    _move_2=('Territorial Roar',0,100,'Status','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def move_1(self):
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.restore(damage//4,'drain')
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('Flinch',counter=0)

    def move_2(self):
        self.target.set_boost('def',-1)
        self.target.set_boost('spd',-1)

# ----------

@Increment(Deviljho,'_move_3')
def value():
    return ('Rampage',120,85,'Physical','Dragon',0,['contact'])

@Increment(Deviljho)
def move_3(self):
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if rnd()<30/100:
            self.set_condition('Confusion',counter=0)

# ----------

@Increment(Deviljho,'_ability')
def value():
    return ['Endless Hunger','Territorial Domination']

@Increment(Deviljho)
def onswitch(self):
    self.set_boost('atk',1)
