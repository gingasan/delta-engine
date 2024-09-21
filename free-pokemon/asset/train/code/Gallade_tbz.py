from engine import *


class Gallade(PokemonBase):
    _species='Gallade'
    _types=['Psychic','Fighting']
    _gender='Male'
    _ability=['Neuroforce']
    _move_1=('Psychic',90,100,'Special','Psychic',0,[])
    _move_2=('Drain Punch',75,100,'Physical','Fighting',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_type_effect(self):
        move_type=self['act']['type']
        target_types=self.target['types']
        effect=1
        for tt in target_types:
            effect*=TYPEEFFECTIVENESS[move_type][tt]
        if effect>1: effect*=1.25
        return effect

    def move_1(self): # Psychic
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<0.1: self.target.set_boost('spd',-1)
    
    def move_2(self): # Drain Punch
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.restore(int(1/2*damage),'drain')
