from engine import *


class Lunala(PokemonBase):
    _species='Lunala'
    _types=['Psychic','Ghost']
    _gender='Female'
    _ability=['Shadow Shield']
    _move_1=('Psychic',90,100,'Special','Psychic',0,[])
    _move_2=('Moonblast',95,100,'Special','Fairy',0,[])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        if self['hp']==self['max_hp']:
            x//=2
        self._set_hp(-x)        

    def move_1(self): # Psychic
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_boost('spe',-1)

    def move_2(self): # Moonblast
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('spa',-1)

# ----------

@Increment(Lunala,'_move_3')
def value():
    return ('Phantom Wave',80,100,'Special','Ghost',0,[])

@Increment(Lunala)
def move_3(self): # Phantom Wave
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('Confusion',counter=0)

# ----------

@Increment(Lunala,'_move_4')
def value():
    return ('Lunar Barrier',0,100000,'Status','Psychic',0,[])

@Increment(Lunala)
def move_4(self): # Lunar Barrier
    self.set_boost('spd',+1,'self')
    self.set_boost('def',+1,'self')

# ----------

@Increment(Lunala,'_ability')
def value():
    return ['Shadow Shield','Spectral Boost']

@Increment(Lunala)
def land_hit_effect(self):
    self.set_boost('spa',+1,'self')

@Increment(Lunala)
def move_1(self): # Psychic
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.land_hit_effect()
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_boost('spe',-1)

@Increment(Lunala)
def move_2(self): # Moonblast
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.land_hit_effect()
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_boost('spa',-1)

@Increment(Lunala)
def move_3(self): # Phantom Wave
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.land_hit_effect()
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('Confusion',counter=0)

# ----------

@Increment(Lunala,'_move_5')
def value():
    return ('Soul Drain',70,100,'Special','Ghost',0,[])

@Increment(Lunala)
def move_5(self): # Soul Drain
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.land_hit_effect()
        self.restore(damage//2,'drain')
