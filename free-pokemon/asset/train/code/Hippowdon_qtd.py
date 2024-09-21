from engine import *


class Hippowdon(PokemonBase):
    _species='Hippowdon'
    _types=['Ground']
    _gender='Male'
    _ability=['Sand Spit']
    _move_1=('Earth Power',90,100,'Special','Ground',0,[])
    _move_2=('Sludge Wave',95,100,'Special','Poison',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.env.set_weather('Sandstorm',from_=self._species)

    def take_damage_attack(self,x):
        self.register_act_taken()
        self._set_hp(-x)        
        if self['hp']==0:
            return
        self.env.set_weather('Sandstorm',from_=self._species)

    def move_1(self): # Earth Power 
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_boost('spd',-1)

    def move_2(self): # Sludge Wave
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: 
                self.target.set_status('PSN')
