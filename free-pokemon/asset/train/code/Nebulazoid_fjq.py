from engine import *


class Nebulazoid(PokemonBase):
    _species='Nebulazoid'
    _types=['Psychic','Dark']
    _gender='Male'
    _ability=['Mind Surge']
    _move_1=('Void Beam',100,95,'Special','Dark',0,[])
    _move_2=('Psychic',90,100,'Special','Psychic',0,[])
    def __init__(self):
        super().__init__()
    
    def get_other_mult(self):
        if self.target['conditions'].get('Confusion') and self['act']['type']=='Psychic':
            return 2.0
        return 1.0

    def move_1(self): # Void Beam
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('spd',-1)

    def move_2(self): # Psychic
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_boost('spd',-1)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('Confusion',counter=0)

# ----------

@Increment(Nebulazoid,'_move_3')
def value():
    return ('Nightmare Pulse',80,100,'Special','Dark',0,[])

@Increment(Nebulazoid)
def move_3(self): # Nightmare Pulse
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('Confusion',counter=0)

# ----------

@Increment(Nebulazoid,'_move_4')
def value():
    return ('Astral Gaze',0,1000000,'Status','Psychic',0,[])

@Increment(Nebulazoid)
def move_4(self): # Astral Gaze
    self.set_boost('spa',+1,'self')
    self.set_boost('spe',+1,'self')

# ----------

@Increment(Nebulazoid,'_ability')
def value():
    return ['Mind Surge','Dark Aura']

@Increment(Nebulazoid)
def get_power(self):
    power=self['act']['power']
    if self['act']['type']=='Dark':
        power*=1.33
    return int(power*self.get_weather_power_mult())

# ----------

@Increment(Nebulazoid,'_move_5')
def value():
    return ('Shadow Blast',110,85,'Special','Dark',0,[])

@Increment(Nebulazoid)
def move_5(self): # Shadow Blast
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('Confusion',counter=0)
