from engine import *


class Lucario(PokemonBase):
    _species='Lucario'
    _types=['Fighting','Steel']
    _gender='Male'
    _ability=['Adaptability']
    _move_1=('Aura Sphere',80,100000,'Special','Fighting',0,[])
    _move_2=('Flash Cannon',80,100,'Special','Steel',0,[])
    _base=(70,130,88,130,70,112)
    def __init__(self):
        super().__init__()

    def get_stab(self):
        stab=1
        if self['act']['type'] in self['types']:
            stab=2
        return stab
    
    def move_1(self): # Aura Sphere
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Flash Cannon
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: self.target.set_boost('spd',-1)

# ----------

@Increment(Lucario,'_move_3')
def value():
    return ('Explore Mind',0,100000,'Status','Psychic',0,[])

@Increment(Lucario)
def move_3(self): # Explore Mind
    self.set_boost('atk',1,'self')
    self.set_boost('spa',1,'self')
    self.set_boost('spe',1,'self')

# ----------

@Increment(Lucario,'_move_4')
def value():
    return ('Extreme Speed',80,100,'Physical','Normal',2,['contact'])

@Increment(Lucario)
def move_4(self): # Extreme Speed
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# ----------

@Increment(Lucario,'_ability')
def value():
    return ['Adaptability','Vitory Heart']

@Increment(Lucario)
def onswitch(self):
    self.set_stat('atk',1.25)
    self.set_stat('spa',1.25)
    self.log('Lucario craves victory and raises its Attack and Special Attack!',color='red')

# ----------

@Increment(Lucario,'_move_5')
def value():
    return ('Close Combat',120,100,'Physical','Fighting',0,['contact'])

@Increment(Lucario)
def move_5(self): # Close Combat
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_boost('def',-1,'self')
        self.set_boost('spd',-1,'self')

# ----------

@Increment(Lucario,'_move_6')
def value():
    return ('Shadow Ball',80,100,'Special','Ghost',0,[])

@Increment(Lucario)
def move_6(self): # Shadow Ball
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100: self.target.set_boost('spd',-1)
