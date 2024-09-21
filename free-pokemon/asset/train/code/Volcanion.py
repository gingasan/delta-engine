from engine import *


class Volcanion(PokemonBase):
    _species='Volcanion'
    _types=['Fire','Water']
    _gender='Female'
    _ability=['Water Absorb']
    _move_1=('Steam Eruption',110,95,'Special','Water',0,[])
    _move_2=('Fire Blast',110,85,'Special','Fire',0,[])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        if self['act_taken']['type']=='Water':
            self.state['hp']=min(self['max_hp'],self['hp']+self['max_hp']//4)
            return
        self._set_hp(-x)        
    
    def move_1(self): # Steam Eruption
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100: self.target.set_status('BRN')
            if self['status']=='FRZ': self.state['status']=None

    def move_2(self): # Fire Blast
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: self.target.set_status('BRN')
