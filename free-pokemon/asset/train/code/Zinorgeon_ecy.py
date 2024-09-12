from engine import *


class Zinorgeon(PokemonBase):
    _species='Zinorgeon'
    _types=['Electric','Dragon']
    _gender='Male'
    _ability=['Thunder Surge']
    _move_1=('Volt Slam',100,90,'Physical','Electric',0,[])
    _move_2=('Dragon Claw',80,100,'Physical','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_env('Electric Terrain','terrain',max_count=5)

    def move_1(self): # Volt Slam
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Dragon Claw
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Zinorgeon,'_move_3')
def value():
    return ('Electric Orb',60,95,'Special','Electric',0,[])

@Increment(Zinorgeon)
def move_3(self): # Electric Orb
    hit=True; i=0
    while hit and i<3:
        damage_ret=self.get_damage()
        if damage_ret['miss']: break
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        i+=1; hit=False if self.target.isfaint() else True

# ----------

@Increment(Zinorgeon,'_move_4')
def value():
    return ('Thunder Howl',0,1000000,'Status','Electric',0,[])

@Increment(Zinorgeon)
def move_4(self): # Thunder Howl
    self.set_boost('atk',+1,'self')
    self.set_boost('spe',+1,'self')

# ----------

@Increment(Zinorgeon,'_ability')
def value():
    return ['Thunder Surge','Apex Fury']

@Increment(Zinorgeon)
def move_1(self): # Volt Slam
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('PAR',counter=0)

@Increment(Zinorgeon)
def move_3(self): # Electric Orb
    hit=True; i=0
    while hit and i<3:
        damage_ret=self.get_damage()
        if damage_ret['miss']: break
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        i+=1; hit=False if self.target.isfaint() else True
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('PAR',counter=0)

@Increment(Zinorgeon)
def get_other_mult(self):
    mult=1
    if self.isstatus('BRN') and self['act']['category']=='Physical':
        mult*=0.5
    if self.target.isstatus('PAR') and self['act']['type']=='Electric':
        mult*=2.0
    return mult

# ----------

@Increment(Zinorgeon,'_move_5')
def value():
    return ('Earthquake',100,100,'Physical','Ground',0,[])

@Increment(Zinorgeon)
def move_5(self): # Earthquake
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
