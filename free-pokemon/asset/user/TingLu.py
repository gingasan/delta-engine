from engine import *


class TingLu(PokemonBase):
    _species='Ting-Lu'
    _types=['Dark','Ground']
    _gender='Male'
    _ability=['Vessel of Ruin']
    _move_1=('Ruination',0,90,'Special','Dark',0,[])
    _move_2=('Earthquake',100,100,'Physical','Ground',0,[])
    _base=(165,110,125,55,105,40)
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.log('Ting-Lu dampens the SpA. of the surrounding.',color='green')
        self.target.set_stat('spa',0.75)
    
    def move_1(self): # Ruination
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=int(0.5*self.target['hp'])
            self.target.take_damage(damage)
    
    def move_2(self): # Earthquake
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(TingLu,'_move_3')
def value():
    return ('Rock Slide',75,90,'Physical','Rock',0,[])

@Increment(TingLu)
def move_3(self): # Rock Slide
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(TingLu,'_move_4')
def value():
    return ('Ancient Curse',0,100000,'Status','Ghost',0,[])

@Increment(TingLu)
def move_4(self): # Ancient Curse
    self.set_boost('spe',-1)
    self.set_boost('atk',+1,'self')
    self.set_boost('def',+1,'self')

# ----------

@Increment(TingLu,'_ability')
def value():
    return ['Vessel of Ruin','Mound']

@Increment(TingLu)
def _take_damage_attack(self,x):
    if self.target['act']['type_effect']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    self.register_act_taken()
    if self['act_taken']['type']=='Water':
        x//=2
        self.log('Water-type attack becomes weak against Ting-Lu.',color='green')
    self.state['hp']=max(0,self['hp']-x)
    self.log(script='attack',species=self._species,x=x,**self['act_taken'])

# ----------

@Increment(TingLu,'_move_5')
def value():
    return ('Sin-Absorb',0,100000,'Status','Dark',-4,[])

@Increment(TingLu)
def move_5(self): # Sin-Absorb
    self.log('Ting-Lu absorbs the power of sin.',color='orange')
    if self['act_taken']:
        self.restore(self['max_hp']//3*2,'heal')
    else:
        self.restore(self['max_hp']//8,'heal')

# ----------

@Increment(TingLu,'_move_6')
def value():
    return ('Body Press',80,100,'Physical','Fighting',0,['contact'])

@Increment(TingLu)
def move_6(self): # Body Press
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

@Increment(TingLu)
def get_base_damage(self,power,crit):
    if self['act']['id']=='Body Press':
        atk_boost=self['boosts']['def']
    else:
        atk_boost=self['boosts']['atk'] if self['act']['category']=='Physical' else self['boosts']['spa']
    def_boost=self.target['boosts']['def'] if self['act']['category']=='Physical' else self.target['boosts']['spd']
    
    if crit:
        atk_boost=max(0,atk_boost)
        def_boost=min(0,def_boost)

    if self['act']['id']=='Body Press':
        attack=self.get_stat('def',atk_boost)
    else:
        attack=self.get_stat('atk' if self['act']['category']=='Physical' else 'spa',atk_boost)
    defense=self.target.get_stat('def' if self['act']['category']=='Physical' else 'spd',def_boost)

    level=100
    base_damage=int(int(int(int(2*level/5+2)*power*attack)/defense)/50)+2

    return base_damage
