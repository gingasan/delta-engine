from engine import *


class Incineroar(PokemonBase):
    _species='Incineroar'
    _types=['Fire','Dark']
    _gender='Femle'
    _ability=['Contrary']
    _move_1=('V-create',180,95,'Physical','Fire',0,['contact'])
    _move_2=('Power Trip',20,100,'Physical','Dark',0,['contact'])
    _base=(115,135,100,80,100,70)
    def __init__(self):
        super().__init__()

    def set_boost(self,key,x,from_='target'):
        x=-x
        bar=6 if key in ['atk','def','spa','spd','spe'] else 3
        if x>0:
            self['boosts'][key]=min(bar,self['boosts'][key]+x)
        else:
            self['boosts'][key]=max(-bar,self['boosts'][key]+x)
        self.log(script='boost',species=self._species,key=key,x=x)

    def get_power(self):
        power=self['act']['power']
        if self['act']['id']=='Power Trip':
            x=1
            for key in ['atk','def','spa','spd','spe']:
                x=x+self['boosts'][key] if self['boosts'][key]>0 else x
            power=power+x*20
        return int(power*self.get_weather_power_mult())
    
    def move_1(self): # V-create
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('spe',-1,'self')
            self.set_boost('def',-1,'self')
            self.set_boost('spd',-1,'self')

    def move_2(self): # Power Trip
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Incineroar,'_move_3')
def value():
    return ('Drain Punch',75,100,'Physical','Fighting',0,['contact','punch'])

@Increment(Incineroar)
def move_3(self): # Drain Punch
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.restore(int(1/2*damage),'drain')

# ----------

@Increment(Incineroar,'_ability')
def value():
    return ['Contrary','Simple']

@Increment(Incineroar)
def set_boost(self,key,x,from_='target'):
    x=-x*2
    bar=6 if key in ['atk','def','spa','spd','spe'] else 3
    if x>0:
        self['boosts'][key]=min(bar,self['boosts'][key]+x)
    else:
        self['boosts'][key]=max(-bar,self['boosts'][key]+x)
    self.log(script='boost',species=self._species,key=key,x=x)

# ----------

@Increment(Incineroar,'_move_4')
def value():
    return ('Double Iron Bash',60,100,'Physical','Steel',0,['contact'])

@Increment(Incineroar)
def move_4(self): # Double Iron Bash
    hit=True; i=0
    while hit and i<2:
        damage_ret=self.get_damage()
        if damage_ret['miss']: break
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        i+=1; hit=False if self.target.isfaint() else True
        if i<2 and rnd()<30/100:
            self.target.set_condition('FLINCH',counter=0)

# ----------

@Increment(Incineroar,'_move_5')
def value():
    return ('Hammer Arm',100,90,'Physical','Fighting',0,['contact'])

@Increment(Incineroar)
def move_5(self): # Hammer Arm
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_boost('spe',-1,'self')
