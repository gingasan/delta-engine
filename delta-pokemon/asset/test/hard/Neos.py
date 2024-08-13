from engine import *


class Neos(PokemonBase):
    _species='Neos'
    _types=['Normal']
    _gender='Male'
    _ability=['Elemental Heart']
    _move_1=('Neos Force',80,100,'Physical','Normal',2,['contact'])
    _move_2=('Skyrip Wing',80,100000,'Physical','Flying',0,[])
    _base=(100,100,100,100,100,100)
    def __init__(self):
        super().__init__()

    def type_change(self):
        self.state['types']=['Normal',self['act']['type']]

    def move_1(self): # Neos Force
        if self['types']!=['Normal']:
            del self.state['types'][-1]
            self.set_boost('atk',1,'self')
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Skyrip Wing
        self.type_change()
        if self['hp']<self.target['hp']:
            self.set_boost('atk',1,'self')
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Neos,'_move_3')
def value():
    return ('Burn to Ash',90,85,'Special','Fire',0,[])

@Increment(Neos)
def move_3(self): # Burn to Ash
    self.type_change()
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<50/100:
            self.target.set_status('BRN')

# -------------------------------------------------------------

@Increment(Neos,'_move_4')
def value():
    return ('Echo Burst',90,100,'Special','Water',0,[])

@Increment(Neos)
def move_4(self): # Echo Burst
    self.type_change()
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint():
            t=rndc(['atk','def','spa','spd','spe'])
            self.target.set_boost(t,-1)

# -------------------------------------------------------------

@Increment(Neos,'_ability')
def value():
    return ['Elemental Heart','Elemental Boost']

@Increment(Neos)
def type_change(self):
    if self['types']!=['Normal',self['act']['type']]:
        self.state['types']=['Normal',self['act']['type']]
        self.state['status']=None
        self.restore(self['max_hp']//3,'heal')

# -------------------------------------------------------------

@Increment(Neos,'_move_5')
def value():
    return ('Wrath of Black',100,90,'Physical','Ghost',0,[])

@Increment(Neos)
def move_5(self): # Wrath of Black
    self.type_change()
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

@Increment(Neos)
def _get_base_damage(self,power,crit):
    atk_boost=self['boosts']['atk'] if self['act']['category']=='Physical' else self['boosts']['spa']
    if self['act']['id']=='Wrath of Black':
        def_boost=0
    else:
        def_boost=self.target['boosts']['def'] if self['act']['category']=='Physical' else self.target['boosts']['spd']

    if crit:
        atk_boost=max(0,atk_boost)
        def_boost=min(0,def_boost)

    attack=self.get_stat('atk' if self['act']['category']=='Physical' else 'spa',atk_boost)
    defense=self.target.get_stat('def' if self['act']['category']=='Physical' else 'spd',def_boost)

    level=100
    base_damage=int(int(int(int(2*level/5+2)*power*attack)/defense)/50)+2

    return base_damage

@Increment(Neos)
def get_type_effect(self):
    move_type=self['act']['type']
    target_types=self.target['types']
    effect=1
    for tt in target_types:
        if tt=='Fairy' and self['act']['id']=='Wrath of Black':
            effect*=2
        else:
            effect*=TYPEEFFECTIVENESS[move_type][tt]
    return effect
