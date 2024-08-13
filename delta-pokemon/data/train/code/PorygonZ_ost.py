from engine import *


class PorygonZ(PokemonBase):
    _species='Porygon-Z'
    _types=['Normal']
    _gender='Genderless'
    _ability=['Download']
    _move_1=('Thunderbolt',90,100,'Special','Electric',0,[])
    _move_2=('Ice Beam',90,100,'Special','Ice',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        if self.target['stats']['def']<self.target['stats']['spd']:
            self.set_boost('atk',1,'self')
        else:
            self.set_boost('spa',1,'self')

    def move_1(self): # Thunderbolt
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage'] 
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_status('PAR')

    def move_2(self): # Ice Beam
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_status('FRZ')
