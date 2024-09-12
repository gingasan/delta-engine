from engine import *


class Infernape(PokemonBase):
    _species='Infernape'
    _types=['Fire','Fighting']
    _gender='Male'
    _ability=['Iron Fist']
    _move_1=('Fire Punch',75,100,'Physical','Fire',0,['contact','punch'])
    _move_2=('Stone Edge',100,80,'Physical','Rock',0,[])
    def __init__(self):
        super().__init__()
    
    def get_power(self):        
        power=self['act']['power']
        if 'punch' in self['act']['property']:
            power*=1.3
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Fire Punch
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Stone Edge
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Infernape,'_move_3')
def value():
    return ('Thunder Punch',75,100,'Physical','Electric',0,['contact','punch'])

@Increment(Infernape)
def move_3(self): # Thunder Punch
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# ----------

@Increment(Infernape,'_move_4')
def value():
    return ('Earthquake',100,100,'Physical','Ground',0,[])

@Increment(Infernape)
def move_4(self): # Earthquake
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# ----------

@Increment(Infernape,'_ability')
def value():
    return ['Iron Fist','Sheer Force']

@Increment(Infernape)
def get_power(self):        
    power=self['act']['power']
    if 'punch' in self['act']['property']:
        power*=1.3
    if self['act']['id'] in ['Fire Punch', 'Stone Edge', 'Thunder Punch', 'Ice Punch']:
        power*=1.3
    return int(power*self.get_weather_power_mult())

# ----------

@Increment(Infernape,'_move_5')
def value():
    return ('Ice Punch',75,100,'Physical','Ice',0,['contact','punch'])

@Increment(Infernape)
def move_5(self): # Ice Punch
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
