from engine import *


class Chirona(PokemonBase):
    _species='Chirona'
    _types=['Psychic','Ground']
    _gender='Male'
    _ability=['Wise Mentor']
    _move_1=('Healing Touch',0,100,'Status','Psychic',0,[])
    _move_2=('Nature Wrath',100,85,'Special','Ground',0,[])
    def __init__(self):
        super().__init__()

    def get_type_effect(self):
        if self['act']['type'] in ['Psychic','Ground']:
            return 1
        move_type=self['act']['type']
        target_types=self.target['types']
        effect=1
        for tt in target_types:
            effect*=TYPEEFFECTIVENESS[move_type][tt]
        return effect

    def move_1(self): # Healing Touch
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            self.target.restore(self.target['max_hp']//10,'heal')
            self.state['status']=None

    def move_2(self): # Nature Wrath
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('spe',-1)

# ----------

@Increment(Chirona,'_move_3')
def value():
    return ('Philosopher Strike',90,100,'Physical','Psychic',0,[])

@Increment(Chirona)
def move_3(self): # Philosopher Strike
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if self.target['status']:
            self.set_condition('DOUBLE_DAMAGE',counter=0)

@Increment(Chirona)
def get_other_mult(self):
    mult=1
    if self.isstatus('BRN') and self['act']['category']=='Physical':
        mult*=0.5
    if self['conditions'].get('DOUBLE_DAMAGE'):
        mult*=2
    return mult

@Increment(Chirona)
def endturn(self):
    if self['conditions'].get('DOUBLE_DAMAGE'):
        self['conditions']['DOUBLE_DAMAGE']['counter']+=1
        if self['conditions']['DOUBLE_DAMAGE']['counter']==2:
            del self['conditions']['DOUBLE_DAMAGE']

# ----------

@Increment(Chirona,'_move_4')
def value():
    return ('Cave Shield',0,100000,'Status','Ground',0,[])

@Increment(Chirona)
def move_4(self): # Cave Shield
    self.set_boost('def',+1,'self')
    self.set_boost('spd',+1,'self')

# ----------

@Increment(Chirona,'_ability')
def value():
    return ['Wise Mentor','Nature Blessing']

@Increment(Chirona)
def endturn(self):
    if self.env.get('Grassy Terrain'):
        self.restore(self['max_hp']//8,'heal')
    if self['conditions'].get('DOUBLE_DAMAGE'):
        self['conditions']['DOUBLE_DAMAGE']['counter']+=1
        if self['conditions']['DOUBLE_DAMAGE']['counter']==2:
            del self['conditions']['DOUBLE_DAMAGE']
