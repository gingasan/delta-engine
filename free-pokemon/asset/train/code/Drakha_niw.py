from engine import *


class Drakha(PokemonBase):
    _species='Drakha'
    _types=['Dark','Dragon']
    _gender='Male'
    _ability=['Shadow Realm']
    _move_1=('Abyssal Flame',100,90,'Special','Dragon',0,[])
    _move_2=('Dark Pulse',80,100,'Special','Dark',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.env.set_side_condition('Shadow Realm',self.side_id,from_=self._species,counter=0,max_count=3)
    
    def get_power(self):
        power=self['act']['power']
        if self.env.get_side_condition('Shadow Realm',self.side_id) and self['act']['type']=='Dark':
            power*=1.5
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Abyssal Flame
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_status('BRN')

    def move_2(self): # Dark Pulse
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Drakha,'_move_3')
def value():
    return ('Despair Roar',0,100000,'Status','Dark',0,[])

@Increment(Drakha)
def move_3(self): # Despair Roar
    self.target.set_boost('atk',-1)
    self.target.set_boost('spa',-1)

# ----------

@Increment(Drakha,'_move_4')
def value():
    return ('Dragon Claw',80,100,'Physical','Dragon',0,[])

@Increment(Drakha)
def move_4(self): # Dragon Claw
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# ----------

@Increment(Drakha,'_ability')
def value():
    return ['Shadow Realm','Destruction Surge']

@Increment(Drakha)
def set_boost(self,key,x,from_='target'):
    self._set_boost(key,x)
    if x<0:
        self.set_condition('DESTRUCTION_SURGE',counter=0)

@Increment(Drakha)
def get_other_mult(self):
    mult=1
    if self.isstatus('BRN') and self['act']['category']=='Physical':
        mult*=0.5
    if self['conditions'].get('DESTRUCTION_SURGE'):
        mult*=2
        del self['conditions']['DESTRUCTION_SURGE']
    return mult
