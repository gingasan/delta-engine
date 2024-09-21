from engine import *


class Dragonite(PokemonBase):
    _species='Dragonite'
    _types=['Dragon','Flying']
    _gender='Male'
    _ability=['Multiscale']
    _move_1=('Dragon Dance',0,1000000,'Status','Dragon',0,[])
    _move_2=('Aerial Ace',60,1000000,'Physical','Flying',0,[])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        if self['hp']==self['max_hp']:
            x//=2
        self._set_hp(-x)        

    def move_1(self): # Dragon Dance
        self.set_boost('atk',+1,'self')
        self.set_boost('spe',+1,'self')

    def move_2(self): # Aerial Ace
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Dragonite,'_move_3')
def value():
    return ('Earthquake',100,100,'Physical','Ground',0,[])

@Increment(Dragonite)
def move_3(self): # Earthquake
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
