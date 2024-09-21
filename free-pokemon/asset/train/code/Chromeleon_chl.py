from engine import *


class Chromeleon(PokemonBase):
    _species='Chromeleon'
    _types=['Normal']
    _gender='Unknown'
    _ability=['Adaptive Camouflage']
    _move_1=('Aqua Slash',80,100,'Physical','Water',0,[])
    _move_2=('Ghostly Claw',70,100,'Physical','Ghost',0,['contact'])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        self._set_hp(-x)        
        if rnd()<0.5:
            self.state['types']=[self['act_taken']['type']]
    
    def move_1(self): # Aqua Slash
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<0.3:
                self.target.set_condition('Flinch',counter=0)

    def move_2(self): # Ghostly Claw  
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<0.2:
                self.target.set_boost('spe',-1)
