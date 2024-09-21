from engine import *


class Hoopa(PokemonBase):
    _species='Hoopa'
    _types=['Psychic','Dark']
    _gender='Neutral'
    _ability=['Contrary']
    _move_1=('Hyperspace Fury',100,100,'Special','Dark',0,[])
    _move_2=('Psychic Combat',120,100,'Physical','Psychic',0,['contact'])
    def __init__(self):
        super().__init__()

    def set_boost(self,key,x,from_='target'):
        x=-x
        self._set_boost(key,x)

    def move_1(self): # Hyperspace Fury
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage=int(0.5*self.target['hp'])
            self.target.take_damage(damage)
    
    def move_2(self): # Psychic Combat
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('def',-1)
            self.set_boost('spd',-1)
