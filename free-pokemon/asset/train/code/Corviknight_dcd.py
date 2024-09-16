from engine import *


class Corviknight(PokemonBase):
    _species='Corviknight'
    _types=['Flying','Steel']
    _gender='Male'
    _ability=['Mirror Armor']
    _move_1=('Wing Slash',85,100,'Physical','Flying',0,[])
    _move_2=('Steel Wing',70,90,'Physical','Steel',0,[])
    def __init__(self):
        super().__init__()

    def set_boost(self,key,x,from_='target'):
        if x<0 and from_=='target':
            self.target.set_boost(key,x)
            self.log('Corviknight reflects the stat-lowering effect back to the opponent.')
            return
        bar=6 if key in ['atk','def','spa','spd','spe'] else 3
        if x>0:
            self['boosts'][key]=min(bar,self['boosts'][key]+x)
        else:
            self['boosts'][key]=max(-bar,self['boosts'][key]+x)
        self.log(script='boost',species=self._species,key=key,x=x)

    def move_1(self): # Wing Slash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Steel Wing
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.set_boost('def',+1,'self')

# ----------

@Increment(Corviknight,'_move_3')
def value():
    return ('Mirror Shield',0,100000,'Status','Steel',0,[])

@Increment(Corviknight)
def move_3(self): # Mirror Shield
    self.set_boost('def',+1,'self')
    self.set_boost('spd',+1,'self')

# ----------

@Increment(Corviknight,'_move_4')
def value():
    return ('Sky Dive',120,75,'Physical','Flying',0,[])

@Increment(Corviknight)
def move_4(self): # Sky Dive
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        recoil=int(damage/3)
        self.take_damage(recoil,'recoil')

# ----------

@Increment(Corviknight,'_ability')
def value():
    return ['Mirror Armor','Steel Clad']

@Increment(Corviknight)
def _take_damage_attack(self,x):
    if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    self.register_act_taken()
    if 'type_effect' in self['act_taken'] and self['act_taken']['type_effect']>1:
        x=int(0.75*x)
    self.state['hp']=max(0,self['hp']-x)
    self.log(script='attack',species=self._species,x=x,**self['act_taken'])

# ----------

@Increment(Corviknight,'_move_5')
def value():
    return ('Body Press',80,100,'Physical','Fighting',0,['contact'])

@Increment(Corviknight)
def move_5(self): # Body Press
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

@Increment(Corviknight)
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
