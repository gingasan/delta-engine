from engine import *


class Duraludon(PokemonBase):
    _species='Duraludon'
    _types=['Steel','Dragon']
    _gender='Male'
    _ability=['Stamina']
    _move_1=('Thunder Wave',0,90,'Status','Electric',0,[])
    _move_2=('Flash Cannon',80,100,'Special','Steel',0,[])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        self._set_hp(-x)        
        if self['hp']==0:
            return
        self.set_boost('def',+1,'self')
    
    def move_1(self): # Thunder Wave
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                self.target.set_status('PAR')
    
    def move_2(self): # Flash Cannon
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_boost('spd',-1)
