from engine import *


class Lucario(PokemonBase):
    _species='Lucario'
    _types=['Fighting','Steel']
    _gender='Male'
    _ability=['Adaptability']
    _move_1=('Aura Sphere',80,100000,'Special','Fighting',0,[])
    _move_2=('Metal Claw',50,95,'Physical','Steel',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_stab(self):
        stab=1
        if self['act']['type'] in self['types']:
            stab=2
        return stab
    
    def move_1(self): # Aura Sphere
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Metal Claw
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<10/100: self.set_boost('atk',1,'self')
