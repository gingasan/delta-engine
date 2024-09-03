from engine import *


class Aerodactyl(PokemonBase):
    _species='Aerodactyl'
    _types=['Rock','Flying']
    _gender='Male'
    _ability=['Momentum Claws']
    _move_1=('Rock Claw',80,100,'Physical','Rock',0,['contact'])
    _move_2=('Dual Wingbeat',40,90,'Physical','Flying',0,['contact'])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_condition('MOMENTUM_CLAWS',counter=0)

    def get_power(self):
        power=self['act']['power']
        if self['act']['id']=='Rock Claw':
            power+=10*self['conditions']['MOMENTUM_CLAWS']['counter']
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Rock Claw
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
        self['conditions']['MOMENTUM_CLAWS']['counter']+=1

    def move_2(self): # Dual Wingbeat
        hit=True; i=0
        while hit and i<2:
            damage_ret=self.get_damage()
            if damage_ret['miss']:break
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True

# -------------------------------------------------------------

@Increment(Aerodactyl,'_move_3')
def value():
    return ('Air Slash',75,95,'Special','Flying',0,[])

@Increment(Aerodactyl)
def move_3(self): # Air Slash
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if rnd()<30/100:
            self.target.set_condition('FLINCH',counter=0)

# -------------------------------------------------------------

@Increment(Aerodactyl,'_move_4')
def value():
    return ('Dragon Claw',80,100,'Physical','Dragon',0,['contact'])

@Increment(Aerodactyl)
def move_4(self): # Dragon Claw
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
    self['conditions']['MOMENTUM_CLAWS']['counter']+=1

@Increment(Aerodactyl)
def get_power(self):
    power=self['act']['power']
    if self['act']['id'] in ['Rock Claw','Dragon Claw']:
        power+=10*self['conditions']['MOMENTUM_CLAWS']['counter']
    return int(power*self.get_weather_power_mult())

# -------------------------------------------------------------

@Increment(Aerodactyl,'_ability')
def value():
    return ['Momentum Claws','Wind Rider']

@Increment(Aerodactyl)
def move_2(self): # Dual Wingbeat
    hit=True; i=0
    while hit and i<2:
        damage_ret=self.get_damage()
        if damage_ret['miss']:break
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        i+=1; hit=False if self.target.isfaint() else True
    self.set_boost('spe',2)

@Increment(Aerodactyl)
def move_3(self): # Air Slash
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if rnd()<30/100:
            self.target.set_condition('FLINCH',counter=0)
    self.set_boost('spe',2)

# -------------------------------------------------------------

@Increment(Aerodactyl,'_move_5')
def value():
    return ('Stone Edge',100,80,'Physical','Rock',0,['contact'])

@Increment(Aerodactyl)
def get_crit(self):
    crit_mult=[0,24,8,2,1]
    crit_ratio=self['boosts']['crit']
    if self['act']['id']=='Stone Edge':
        crit_ratio=min(3,crit_ratio+1)
    crit=False
    if rnd()*crit_mult[crit_ratio+1]<1:
        crit=True
    return crit

@Increment(Aerodactyl)
def move_5(self): # Stone Edge
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
