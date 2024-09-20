from engine import *


class Tyranitar(PokemonBase):
    _species='Tyranitar'
    _types=['Rock','Dark']
    _gender='Male'
    _ability=['Sand Stream']
    _move_1=('Stone Edge',100,80,'Physical','Rock',0,[])
    _move_2=('Crunch',80,100,'Physical','Dark',0,['contact'])
    _base=(120,134,100,85,100,61)
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.env.set_weather('Sandstorm',from_=self._species)

    def get_crit(self):
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        if self['act']['id']=='Stone Edge':
            crit_ratio=min(3,crit_ratio+1)
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit

    def move_1(self): # Stone Edge
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Crunch
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100: self.target.set_boost('def',-1)

# ----------

@Increment(Tyranitar,'_move_3')
def value():
    return ('Earthquake',100,100,'Physical','Ground',0,[])

@Increment(Tyranitar)
def move_3(self): # Earthquake
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# ----------

@Increment(Tyranitar,'_move_4')
def value():
    return ('Toxic',0,90,'Status','Poison',0,[])

@Increment(Tyranitar)
def move_4(self): # Toxic
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        self.target.set_status('TOX')

# ----------

@Increment(Tyranitar,'_ability')
def value():
    return ['Sand Stream','Heavy Armor']

@Increment(Tyranitar)
def _take_damage_attack(self,x):
    if self.target['act']['type_effect']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    self.register_act_taken()
    if rnd()<30/100:
        x//=2
        self.log("Tyranitar's Heavy Armor is activated.",color='orange')
    self.state['hp']=max(0,self['hp']-x)
    self.log(script='attack',species=self._species,x=x,**self['act_taken'])

# ----------

@Increment(Tyranitar,'_move_5')
def value():
    return ('Dragon Dance',0,100000,'Status','Dragon',0,[])

@Increment(Tyranitar)
def move_5(self): # Dragon Dance
    self.set_boost('atk',+1,'self')
    self.set_boost('spe',+1,'self')
