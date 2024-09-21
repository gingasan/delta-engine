from engine import *


class Hydragar(PokemonBase):
    _species='Hydragar'
    _types=['Water','Fire']
    _gender='Neutral'
    _ability=['Regenerative Fury']
    _move_1=('Flame Torrent',95,90,'Special','Fire',0,[])
    _move_2=('Venomous Spit',80,100,'Special','Poison',0,[])
    def __init__(self):
        super().__init__()

    def endturn(self):
        if self['hp']<self['max_hp']//2:
            self.restore(self['max_hp']//5,'heal')

    def move_1(self): # Flame Torrent
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('BRN')

    def move_2(self): # Venomous Spit
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<50/100:
                self.target.set_status('PSN')

# ----------

@Increment(Hydragar,'_move_3')
def value():
    return ('Aqua Slash',85,100,'Physical','Water',0,[])

@Increment(Hydragar)
def move_3(self): # Aqua Slash
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if self['conditions'].get('AQUA_SLASH'):
            self['conditions']['AQUA_SLASH']['counter']+=1
        else:
            self.set_condition('AQUA_SLASH',counter=0)

@Increment(Hydragar)
def get_crit(self):
    crit_mult=[0,24,8,2,1]
    crit_ratio=self['boosts']['crit']
    crit=False
    if self['conditions'].get('AQUA_SLASH'):
        if rnd()*crit_mult[crit_ratio+1]<1*1.2*self['conditions']['AQUA_SLASH']['counter']:
            crit=True
    else:
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
    return crit

# ----------

@Increment(Hydragar,'_move_4')
def value():
    return ('Hydra Wrath',110,85,'Special','Water',0,[])

@Increment(Hydragar)
def move_4(self): # Hydras Wrath
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.target.set_boost('spa',-1)

# ----------

@Increment(Hydragar,'_ability')
def value():
    return ['Regenerative Fury','Nine-Headed Vengeance']

@Increment(Hydragar)
def take_damage_attack(self,x):
    self.register_act_taken()
    self._set_hp(-x)    
    if self['hp']==0:
        return
    if 'crit' in self['act_taken'] and self['act_taken']['crit']:
        self.set_boost('atk',+2,'self')
        self.set_boost('spa',+2,'self')
