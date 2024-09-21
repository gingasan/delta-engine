from engine import *


class Furfrou(PokemonBase):
    _species='Furfrou'
    _types=['Normal']
    _gender='Male'
    _ability=['Fur Coat']
    _move_1=('Thunder Fang',65,95,'Physical','Electric',0,['contact'])
    _move_2=('Ice Fang',65,95,'Physical','Ice',0,['contact'])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        if self['act_taken']['category']=='Physical':
            x//=2
        self._set_hp(-x)        

    def move_1(self): # Thunder Fang
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: 
                self.target.set_status('PAR')
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_condition('Flinch',counter=0)

    def move_2(self): # Ice Fang
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_status('FRZ')
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_condition('Flinch',counter=0)
