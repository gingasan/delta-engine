from engine import *


class Grimmsnarl(PokemonBase):
    _species='Grimmsnarl'
    _types=['Dark','Fairy']
    _gender='Male'
    _ability=['Prankster']
    _move_1=('Spirit Break',75,100,'Physical','Fairy',0,['contact'])
    _move_2=('Bulk Up',0,100000,'Status','Fighting',0,[])
    def __init__(self):
        super().__init__()

    def get_priority(self,move_id):
        if self._moves[move_id]['category']=='Status':
            return 1
        return self._moves[move_id]['priority']

    def move_1(self): # Spirit Break
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                self.target.set_boost('spa',-1)

    def move_2(self): # Bulk Up
        self.set_boost('atk',+1,'self')
        self.set_boost('def',+1,'self')
