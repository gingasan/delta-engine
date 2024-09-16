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
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_status('BRN')

    def move_2(self): # Dark Pulse
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
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
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# ----------

@Increment(Drakha,'_ability')
def value():
    return ['Shadow Realm','Destruction Surge']

@Increment(Drakha)
def set_boost(self,key,x,from_='target'):
    bar=6 if key in ['atk','def','spa','spd','spe'] else 3
    if x>0:
        self['boosts'][key]=min(bar,self['boosts'][key]+x)
    else:
        self['boosts'][key]=max(-bar,self['boosts'][key]+x)
        self.set_condition('DESTRUCTION_SURGE',counter=0)
    self.log(script='boost',species=self._species,key=key,x=x)

@Increment(Drakha)
def get_other_mult(self):
    mult=1
    if self.isstatus('BRN') and self['act']['category']=='Physical':
        mult*=0.5
    if self['conditions'].get('DESTRUCTION_SURGE'):
        mult*=2
        del self['conditions']['DESTRUCTION_SURGE']
    return mult
