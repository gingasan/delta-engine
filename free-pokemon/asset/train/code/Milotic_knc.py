from engine import *


class Milotic(PokemonBase):
    _species='Milotic'
    _types=['Water']
    _gender='Female'
    _ability=['Competitive']
    _move_1=('Scald',80,100,'Special','Water',0,[])
    _move_2=('Leaf Storm',130,90,'Special','Grass',0,[])
    def __init__(self):
        super().__init__()

    def set_boost(self,key,x,from_='target'):
        if x<0:
            self.set_boost('spa',2)
        self._set_boost(key,x)

    def move_1(self): # Scald
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<0.3:
                self.target.set_status('BRN')

    def move_2(self): # Leaf Storm
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self['boosts']['spa']=max(-6,self['boosts']['spa']-2)
