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
        self._set_boost(key,x)

    def move_1(self): # Wing Slash
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Steel Wing
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
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
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        recoil=int(damage/3)
        self.take_damage(recoil,'recoil')

# ----------

@Increment(Corviknight,'_ability')
def value():
    return ['Mirror Armor','Steel Clad']

@Increment(Corviknight)
def take_damage_attack(self,x):
    self.register_act_taken()
    if 'type_effect' in self['act_taken'] and self['act_taken']['type_effect']>1:
        x=int(0.75*x)
    self._set_hp(-x)    

# ----------

@Increment(Corviknight,'_move_5')
def value():
    return ('Body Press',80,100,'Physical','Fighting',0,['contact'])

@Increment(Corviknight)
def move_5(self): # Body Press
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
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

# ----------

@Increment(Corviknight,'_move_6')
def value():
    return ('Taunt',0,100,'Status','Dark',0,[])

@Increment(Corviknight)
def move_6(self): # Taunt
    self.target.set_condition('Taunt',counter=0)

@Increment(Corviknight)
def disable_moves(self, moves):
    disabled = []
    if self.target['conditions'].get('Taunt'):
        for _, move in moves.items():
            if move['category']=='Status':
                disabled+=[move['id']]
    return disabled

@Increment(Corviknight)
def endturn(self):
    if self.target['conditions'].get('Taunt'):
        self.target['conditions']['Taunt']['counter']+=1
        if self.target['conditions']['Taunt']['counter']==4:
            del self.target['conditions']['Taunt']
