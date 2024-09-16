from engine import *


class Gardevoir(PokemonBase):
    _species='Gardevoir'
    _types=['Psychic','Fairy']
    _gender='Female'
    _ability=['Wonder Skin']
    _move_1=('Dazzling Gleam',80,100,'Special','Fairy',0,[])
    _move_2=('Shadow Ball',80,100,'Special','Ghost',0,[])
    def __init__(self):
        super().__init__()

    def get_evasion(self):
        if self.target['act']['category']=='Status':
            return 0.5
        return 1
    
    def move_1(self): # Dazzling Gleam
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Shadow Ball
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<0.2:
                self.target.set_boost('spd',-1)

# ----------

@Increment(Gardevoir,'_move_3')
def value():
    return ('Mind Blast',90,95,'Special','Psychic',0,[])

@Increment(Gardevoir)
def move_3(self): # Mind Blast
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_condition('Confusion',counter=0)

# ----------

@Increment(Gardevoir,'_move_4')
def value():
    return ('Fairy Shield',0,100000,'Status','Fairy',0,[])

@Increment(Gardevoir)
def move_4(self): # Fairy Shield
    self.set_boost('def',1,'self')
    self.set_boost('spd',1,'self')

# ----------

@Increment(Gardevoir,'_ability')
def value():
    return ['Wonder Skin','Psychic Surge']

@Increment(Gardevoir)
def onswitch(self):
    self.env.set_terrain('Psychic Terrain',from_=self._species)
