from engine import *


class Aerodactyl(PokemonBase):
    _species='Aerodactyl'
    _types=['Rock','Flying']
    _gender='Male'
    _ability=['Tough Claws']
    _move_1=('Head Smash',150,80,'Physical','Rock',0,['contact'])
    _move_2=('Dual Wingbeat',40,90,'Physical','Flying',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_power(self):        
        power=self['act']['power']
        if 'contact' in self['act']['property']:
            power*=1.3
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Head Smash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.take_damage(damage//2,'recoil')

    def move_2(self): # Brave Bird
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.take_damage(int(0.33*damage),'recoil')

# ----------

@Increment(Aerodactyl,'_move_3')
def value():
    return ('Dragon Claw',80,100,'Physical','Dragon',0,['contact'])

@Increment(Aerodactyl)
def move_3(self): # Dragon Claw
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# ----------

@Increment(Aerodactyl,'_move_4')
def value():
    return ('Dragon Dance',0,100000,'Status','Dragon',0,[])

@Increment(Aerodactyl)
def move_4(self): # Dragon Dance
    self.set_boost('atk',1,'self')
    self.set_boost('spe',1,'self')

# ----------

@Increment(Aerodactyl,'_ability')
def value():
    return ['Tough Claws','Rock Head']

@Increment(Aerodactyl)
def move_1(self): # Head Smash
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

@Increment(Aerodactyl)
def move_2(self): # Brave Bird
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# ----------

@Increment(Aerodactyl,'_move_5')
def value():
    return ('Earthquake',100,100,'Physical','Ground',0,[])

@Increment(Aerodactyl)
def move_5(self): # Earthquake
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
