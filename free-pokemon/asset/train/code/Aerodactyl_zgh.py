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
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Sky Attack
        self.target.set_boost('def',+1)
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<50/100:
                self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Aerodactyl,'_move_3')
def value():
    return ('Rock Slide',75,90,'Physical','Rock',0,['contact'])

@Increment(Aerodactyl)
def move_3(self): # Rock Slide
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Aerodactyl,'_move_4')
def value():
    return ('Aerial Ace',60,1000000,'Physical','Flying',0,['contact'])

@Increment(Aerodactyl)
def move_4(self): # Aerial Ace
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# ----------

@Increment(Aerodactyl,'_ability')
def value():
    return ['Rock Head','Velocity Surge']

@Increment(Aerodactyl)
def set_boost(self,key,x,from_='target'):
    self._set_boost(key,x)
    if key=='spe' and x>0:
        self._set_boost('atk',1)
        self.log("Aerodactyl further raises its Atk. by 1.")

# ----------

@Increment(Aerodactyl,'_move_5')
def value():
    return ('Dragon Claw',80,100,'Physical','Dragon',0,['contact'])

@Increment(Aerodactyl)
def move_5(self): # Dragon Claw
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
