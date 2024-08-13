from engine import *


class Sharpedo(PokemonBase):
    _species='Sharpedo'
    _types=['Water','Dark']
    _gender='Male'
    _ability=['Speed Boost']
    _move_1=('Crunch',80,100,'Physical','Dark',0,['bite','contact'])
    _move_2=('Liquidation',85,100,'Physical','Water',0,['contact'])
    def __init__(self):
        super().__init__()
    
    def endturn(self):
        self.set_boost('spe',1,'self')
        
    def move_1(self): # Crunch
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('def',-1)

    def move_2(self): # Liquidation
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('def',-1)

# -------------------------------------------------------------

@Increment(Sharpedo,'_move_3')
def value():
    return ('Aqua Jet',40,100,'Physical','Water',1,['contact'])

@Increment(Sharpedo)
def move_3(self): # Aqua Jet
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Sharpedo,'_move_4')
def value():
    return ('Fin Slash',70,100,'Physical','Water',0,['contact'])

@Increment(Sharpedo)
def move_4(self): # Fin Slash
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('FLINCH',counter=0)

# -------------------------------------------------------------

@Increment(Sharpedo,'_ability')
def value():
    return ['Speed Boost','Razor Fin']

@Increment(Sharpedo)
def get_power(self):
    power=self['act']['power']
    if 'bite' in self['act']['property']:
        power*=1.5
    return int(power*self.get_weather_power_mult())
