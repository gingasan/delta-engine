from engine import *


class Moltaroth(PokemonBase):
    _species='Moltaroth'
    _types=['Fire','Steel']
    _gender='Neutral'
    _ability=['Magma Armor']
    _move_1=('Molten Breath',110,85,'Special','Fire',0,[])
    _move_2=('Gold Meltdown',90,100,'Special','Steel',0,[])
    def __init__(self):
        super().__init__()

    def set_status(self,x):
        if self['status'] or self.env.get('Misty Terrain'):
            return
        if x=='BRN':
            if self.istype('Fire'):
                return
        elif x=='PAR':
            if self.istype('Electric'):
                return
        elif x=='PSN':
            if self.istype('Poison') or self.istype('Steel'):
                return
        elif x=='TOX':
            if self.istype('Poison') or self.istype('Steel'):
                return
        elif x=='FRZ':
            return
        elif x=='SLP':
            if self.env.get("Electric Terrain"):
                return
        self._set_status(x)

    def get_power(self):
        power=self['act']['power']
        if self['act']['type']=='Fire' and self['hp']<self['max_hp']//2:
            power=int(power*1.3)
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Molten Breath
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<30/100:
                self.target.set_status('BRN')

    def move_2(self): # Gold Meltdown
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Moltaroth,'_move_3')
def value():
    return ('Fury Charge',130,100,'Physical','Steel',0,[])

@Increment(Moltaroth)
def move_3(self): # Fury Charge
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.take_damage(int(0.33*damage),'recoil')

# ----------

@Increment(Moltaroth,'_move_4')
def value():
    return ('Enrage',0,100,'Status','Normal',0,[])

@Increment(Moltaroth)
def move_4(self): # Enrage
    self.set_boost('atk',+1,'self')
    self.set_boost('spe',+1,'self')

# ----------

@Increment(Moltaroth,'_ability')
def value():
    return ['Magma Armor','Proten']

@Increment(Moltaroth)
def type_change(self):
    self.state['types']=[self['act']['type']]

@Increment(Moltaroth)
def move_1(self): # Molten Breath
    self.type_change()
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if rnd()<30/100:
            self.target.set_status('BRN')

@Increment(Moltaroth)
def move_2(self): # Gold Meltdown
    self.type_change()
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)

@Increment(Moltaroth)
def move_3(self): # Fury Charge
    self.type_change()
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.take_damage(int(0.33*damage),'recoil')

@Increment(Moltaroth)
def move_4(self): # Enrage
    self.type_change()
    self.set_boost('atk',+1,'self')
    self.set_boost('spe',+1,'self')
