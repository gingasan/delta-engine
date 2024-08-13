from engine import *


class Aerodactyl(PokemonBase):
    _species='Aerodactyl'
    _types=['Rock','Flying']
    _gender='Male'
    _ability=['Rock Head']
    _move_1=('Head Smash',120,80,'Physical','Rock',0,['recoil'])
    _move_2=('Sky Attack',140,90,'Physical','Flying',0,[])
    def __init__(self):
        super().__init__()

    def get_power(self):        
        power=self['act']['power']
        if self['act']['id']=='Head Smash' and self['hp']==self['max_hp']:
            power*=1.5
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Head Smash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Sky Attack
        self.target.set_boost('def',+1)
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<50/100:
                self.target.set_condition('FLINCH',counter=0)

# -------------------------------------------------------------

@Increment(Aerodactyl,'_move_3')
def value():
    return ('Rock Slide',75,90,'Physical','Rock',0,['contact'])

@Increment(Aerodactyl)
def move_3(self): # Rock Slide
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('FLINCH',counter=0)

# -------------------------------------------------------------

@Increment(Aerodactyl,'_move_4')
def value():
    return ('Aerial Ace',60,1000000,'Physical','Flying',0,['contact'])

@Increment(Aerodactyl)
def move_4(self): # Aerial Ace
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Aerodactyl,'_ability')
def value():
    return ['Rock Head','Velocity Surge']

@Increment(Aerodactyl)
def set_boost(self,key,x,from_='target'):
    bar=6 if key in ['atk','def','spa','spd','spe'] else 3
    if x>0:
        self['boosts'][key]=min(bar,self['boosts'][key]+x)
    else:
        self['boosts'][key]=max(-bar,self['boosts'][key]+x)
    if key=='spe' and x>0:
        self.set_boost('atk',1,'self')

# -------------------------------------------------------------

@Increment(Aerodactyl,'_move_5')
def value():
    return ('Dragon Claw',80,100,'Physical','Dragon',0,['contact'])

@Increment(Aerodactyl)
def move_5(self): # Dragon Claw
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
