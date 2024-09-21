from engine import *


class Gardevoir(PokemonBase):
    _species='Gardevoir'
    _types=['Psychic','Fairy']
    _gender='Female'
    _ability=['Synchronize']
    _move_1=('Psychic',90,100,'Special','Psychic',0,[])
    _move_2=('Moon Blast',95,100,'Special','Fairy',0,[])
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
            if self.istype('Ice'):
                return
        elif x=='SLP':
            if self.env.get("Electric Terrain"):
                return
        self._set_status(x)
        self.target.set_status(x)

    def move_1(self): # Psychic
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: self.target.set_boost('spd',-1)

    def move_2(self): # Moon Blast
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100: self.target.set_boost('spa',-1)

# ----------

@Increment(Gardevoir,'_move_3')
def value():
    return ('Thunderbolt',90,100,'Special','Electric',0,[])

@Increment(Gardevoir)
def move_3(self): # Thunderbolt
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100: self.target.set_status('PAR')

# ----------

@Increment(Gardevoir,'_move_4')
def value():
    return ('Shadow Ball',80,100,'Special','Ghost',0,[])

@Increment(Gardevoir)
def move_4(self): # Shadow Ball
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100: self.target.set_boost('spd',-1)

# ----------

@Increment(Gardevoir,'_ability')
def value():
    return ['Synchronize','Mind Shield']

@Increment(Gardevoir)
def take_damage_attack(self,x):
    self.register_act_taken()
    if self['act_taken']['category']=='Special':
        x//=2
    self._set_hp(-x)    

# ----------

@Increment(Gardevoir,'_move_5')
def value():
    return ('Ethereal Shield',0,100000,'Status','Psychic',0,[])

@Increment(Gardevoir)
def move_5(self): # Ethereal Shield
    self.set_boost('spd',+2)
