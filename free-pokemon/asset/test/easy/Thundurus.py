from engine import *


class Thundurus(PokemonBase):
    _species='Thundurus'
    _types=['Electric','Flying']
    _gender='Male'
    _ability=['Prankster']
    _move_1=('Nasty Plot',0,100000,'Status','Dark',0,[])
    _move_2=('Thunderbolt',90,100,'Special','Electric',0,[])
    def __init__(self):
        super().__init__()

    def get_priority(self,move_id):
        if self._moves[move_id]['category']=='Status':
            return 1
        return self._moves[move_id]['priority']

    def move_1(self): # Nasty Plot
        self.set_boost('spa',+2,'self')

    def move_2(self): # Thunderbolt
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_status('PAR')

# ----------

@Increment(Thundurus,'_move_3')
def value():
    return ('Sludge Bomb',90,100,'Special','Poison',0,[])

@Increment(Thundurus)
def move_3(self): # Sludge Bomb
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_status('PSN')
