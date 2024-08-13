from engine import *


class TingLu(PokemonBase):
    _species='Ting-Lu'
    _types=['Dark','Ground']
    _gender='Male'
    _ability=['Vessel of Ruin']
    _move_1=('Ruination',0,90,'Special','Dark',0,[])
    _move_2=('Earthquake',100,100,'Physical','Ground',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.target.set_stat('spa',0.75)

    def move_1(self): # Ruination
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=int(0.5*self.target['hp'])
            self.target.take_damage(damage)
    
    def move_2(self): # Earthquake
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
