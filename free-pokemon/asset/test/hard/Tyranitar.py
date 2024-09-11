from engine import *


class Tyranitar(PokemonBase):
    _species='Tyranitar'
    _types=['Rock','Dark']
    _gender='Male'
    _ability=['Sand Stream']
    _move_1=('Stone Edge',100,80,'Physical','Rock',0,[])
    _move_2=('Crunch',80,100,'Physical','Dark',0,['contact'])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_env('Sandstorm','weather')

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

# -------------------------------------------------------------

@Increment(Tyranitar,'_move_3')
def value():
    return ('Earthquake',100,100,'Physical','Ground',0,[])

@Increment(Tyranitar)
def move_3(self): # Earthquake
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Tyranitar,'_move_4')
def value():
    return ('Toxic',0,90,'Status','Poison',0,[])

@Increment(Tyranitar)
def move_4(self): # Toxic
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        self.target.set_status('TOX')

# -------------------------------------------------------------

@Increment(Tyranitar,'_ability')
def value():
    return ['Sand Stream','Heavy Armor']

@Increment(Tyranitar)
def _take_damage_attack(self,x):
    if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    self.register_act_taken()
    if rnd()<30/100:
        x//=2
    self.state['hp']=max(0,self['hp']-x)
    self.log('{} loses {} HP.'.format(self._species,x),act_taken=self['act_taken'])

# -------------------------------------------------------------

@Increment(Tyranitar,'_move_5')
def value():
    return ('Iron Defense',0,100000,'Status','Steel',0,[])

@Increment(Tyranitar)
def move_5(self): # Iron Defense
    self.set_boost('def',2,'self')
