from engine import *


class Absol(PokemonBase):
    _species='Absol'
    _types=['Dark']
    _gender='Male'
    _ability=['Super Luck']
    _move_1=('Night Slash',70,100,'Physical','Dark',0,['contact'])
    _move_2=('Thunder Punch',75,100,'Physical','Electric',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_crit(self):
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        crit_ratio=min(3,crit_ratio+1)
        if self['act']['id']=='Night Slash':
            crit_ratio=min(3,crit_ratio+1)
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit

    def move_1(self): # Night Slash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Thunder Punch
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_status('PAR')
