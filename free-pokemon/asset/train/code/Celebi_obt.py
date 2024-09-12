from engine import *


class Celebi(PokemonBase):
    _species='Celebi'
    _types=['Psychic','Grass']
    _gender='Neutral'
    _ability=['Serene Grace']
    _move_1=('Leech Seed',0,90,'Status','Grass',0,[])
    _move_2=('Psychic',90,100,'Special','Psychic',0,[])
    def __init__(self):
        super().__init__()

    def get_effect_chance(self,effect):
        return 2*effect if effect<=0.5 else 1

    def endturn(self):
        if self.target['conditions'].get('LEECH_SEED'):
            self.target.take_damage(self.target['max_hp']//8,'loss')
            self.take_damage(self.target['max_hp']//8,'drain')

    def move_1(self): # Leech Seed
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            self.target.set_condition('LEECH_SEED',counter=0)

    def move_2(self): # Psychic
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<self.get_effect_chance(10/100):
                self.target.set_boost('spd',-1)

# ----------

@Increment(Celebi,'_move_3')
def value():
    return ('Ancient Power',60,100,'Special','Rock',0,[])

@Increment(Celebi)
def move_3(self): # Ancient Power
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<self.get_effect_chance(10/100):
            for k in ['atk','def','spa','spd','spe']:
                self.set_boost(k,1,'self')

# ----------

@Increment(Celebi,'_move_4')
def value():
    return ('Giga Drain',75,100,'Special','Grass',0,[])

@Increment(Celebi)
def move_4(self): # Giga Drain
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.restore(int(0.5*damage),'drain')

# ----------

@Increment(Celebi,'_move_5')
def value():
    return ('Recover',0,100000,'Status','Normal',0,[])

@Increment(Celebi)
def move_5(self): # Recover
    self.restore(int(0.5*self['max_hp']),'heal')
