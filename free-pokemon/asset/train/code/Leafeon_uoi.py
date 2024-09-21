from engine import *


class Leafeon(PokemonBase):
    _species='Leafeon'
    _types=['Grass']
    _gender='Female'
    _ability=['Verdant Grace']
    _move_1=('Leaf Blade',90,100,'Physical','Grass',0,['contact'])
    _move_2=('Quick Attack',40,100,'Physical','Normal',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_crit(self):
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        if self['act']['id']=='Leaf Blade':
            crit_ratio=min(3,crit_ratio+1)
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit

    def move_1(self): # Leaf Blade
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<20/100: self.restore(self['max_hp']//10,'heal')

    def move_2(self): # Quick Attack
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
