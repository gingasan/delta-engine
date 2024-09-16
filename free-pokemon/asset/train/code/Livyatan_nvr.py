from engine import *


class Livyatan(PokemonBase):
    _species='Livyatan'
    _types=['Water','Dark']
    _gender='Male'
    _ability=['Apex Predator']
    _move_1=('Tidal Crush',85,90,'Physical','Water',0,['contact'])
    _move_2=('Abyssal Bite',100,95,'Physical','Dark',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_power(self):
        power=self['act']['power']
        if self.target['stats']['spe']<self['stats']['spe']:
            power*=1.3
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Tidal Crush
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('CONFUSION',counter=0)

    def move_2(self): # Abyssal Bite
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<50/100:
                self.target.set_boost('def',-1)

# ----------

@Increment(Livyatan,'_move_3')
def value():
    return ('Whale Song',0,100000,'Status','Water',0,[])

@Increment(Livyatan)
def move_3(self): # Whale Song
    self.set_boost('atk',+1,'self')
    self.set_boost('spe',+1,'self')

# ----------

@Increment(Livyatan,'_move_4')
def value():
    return ('Dark Surge',80,100,'Special','Dark',0,[])

@Increment(Livyatan)
def move_4(self): # Dark Surge
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Livyatan,'_ability')
def value():
    return ['Apex Predator','Enamel Armor']

@Increment(Livyatan)
def _take_damage_attack(self,x):
    if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    self.register_act_taken()
    if self['act_taken']['category']=='Physical':
        x=int(x*0.75)
    self.state['hp']=max(0,self['hp']-x)
    self.log(script='attack',species=self._species,x=x,**self['act_taken'])
    if self['hp']==0:
        return
    if 'property' in self['act_taken'] and 'contact' in self['act_taken']['property'] and rnd()<20/100:
        self.target.set_boost('def',-1)

# ----------

@Increment(Livyatan,'_move_5')
def value():
    return ('Hydro Blast',110,80,'Special','Water',0,[])

@Increment(Livyatan)
def move_5(self): # Hydro Blast
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_condition('CONFUSION',counter=0)
