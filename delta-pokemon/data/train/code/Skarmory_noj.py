from engine import *


class Skarmory(PokemonBase):
    _species='Skarmory'
    _types=['Steel','Flying']
    _gender='Male'
    _ability=['Tinted Lens']
    _move_1=('Metal Claw',50,95,'Physical','Steel',0,['contact'])
    _move_2=('Air Slash',75,95,'Special','Flying',0,[])
    def __init__(self):
        super().__init__()

    def get_type_effect(self):
        move_type=self['act']['type']
        target_types=self.target['types']
        effect=1
        for tt in target_types:
            effect*=TYPEEFFECTIVENESS[move_type][tt]
        if effect<1:
            effect*=2
        return effect

    def move_1(self): # Metal Claw
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<50/100:
                self.set_boost('atk',1,'self')

    def move_2(self): # Air Slash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('FLINCH',counter=0)
