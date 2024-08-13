from engine import *


class Togekiss(PokemonBase):
    _species='Togekiss'
    _types=['Fairy','Flying']
    _gender='Female'
    _ability=['Serene Grace']
    _move_1=('Air Slash',75,95,'Special','Flying',0,[])
    _move_2=('Dazzling Gleam',80,100,'Special','Fairy',0,[])
    def __init__(self):
        super().__init__()
    
    def get_effect_chance(self,effect):
        return 2*effect if effect<=0.5 else 1
    
    def move_1(self): # Air Slash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<self.get_effect_chance(30/100):
                self.target.set_condition('FLINCH',counter=0)
    
    def move_2(self): # Dazzling Gleam
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
