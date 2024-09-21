from engine import *


class Luminarae(PokemonBase):
    _species='Luminarae'
    _types=['Electric','Fairy']
    _gender='Female'
    _ability=['Aegis Shield']
    _move_1=('Thunderbolt',90,100,'Special','Electric',0,[])
    _move_2=('Mystic Gleam',90,95,'Special','Fairy',0,[])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        if self.state['status']:
            x=int(x*0.8)
        self._set_hp(-x)        
    
    def move_1(self): # Thunderbolt
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<10/100:
                self.target.set_status('PAR')

    def move_2(self): # Mystic Gleam
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<20/100:
                self.set_boost('spa', 1)
