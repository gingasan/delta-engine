from engine import *


class Bazelgeuse(PokemonBase):
    _species='Bazelgeuse'
    _types=['Fire','Dragon']
    _gender='Male'
    _ability=['Explosive Scales']
    _move_1=('Scale Burst',0,100,'Status','Fire',0,[])
    _move_2=('Inferno Blast',100,70,'Special','Fire',0,[])
    def __init__(self):
        super().__init__()

    def drop_scales(self):
        if not self.target['conditions'].get('EXPLOSIVE_SCALES'):
            self.target.set_condition('EXPLOSIVE_SCALES',counter=0)
        self.target['conditions']['EXPLOSIVE_SCALES']['counter']+=1

    def explode_scales(self):
        if not self.target['conditions'].get('EXPLOSIVE_SCALES'):
            return
        for _ in range(self.target['conditions']['EXPLOSIVE_SCALES']['counter']):
            self.target.take_damage(self.target['max_hp']//10,'loss')
        del self.target['conditions']['EXPLOSIVE_SCALES']

    def take_damage_attack(self,x):
        self.register_act_taken()
        self._set_hp(-x)        
        self.drop_scales()

    def endturn(self):
        self.explode_scales()

    def move_1(self): # Scale Burst
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            self.drop_scales()
    
    def move_2(self): # Inferno Blast
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<50/100: self.target.set_status('BRN')

# ----------

@Increment(Bazelgeuse,'_move_3')
def value():
    return ('Draco Meteor',130,90,'Special','Dragon',0,[])

@Increment(Bazelgeuse)
def move_3(self): # Draco Meteor
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_boost('spa',-2,'self')

# ----------

@Increment(Bazelgeuse,'_move_4')
def value():
    return ('Dragon Roar',0,100,'Status','Dragon',0,[])

@Increment(Bazelgeuse)
def move_4(self): # Dragon Roar
    self.target.set_boost('atk',-1)
    self.target.set_boost('spa',-1)

# ----------

@Increment(Bazelgeuse,'_ability')
def value():
    return ['Explosive Scales','Superheated State']

@Increment(Bazelgeuse)
def explode_scales(self):
    if not self.target['conditions'].get('EXPLOSIVE_SCALES'):
        return
    for _ in range(self.target['conditions']['EXPLOSIVE_SCALES']['counter']):
        self.target.take_damage(self.target['max_hp']//10,'loss')
        if self['hp']<self['max_hp']//2:
            self.target.take_damage(self.target['max_hp']//10,'loss')
    del self.target['conditions']['EXPLOSIVE_SCALES']

# ----------

@Increment(Bazelgeuse,'_move_5')
def value():
    return ('Earth Power',90,100,'Special','Ground',0,[])

@Increment(Bazelgeuse)
def move_5(self): # Earth Power
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<0.1:
            self.target.set_boost('spd',-1)
