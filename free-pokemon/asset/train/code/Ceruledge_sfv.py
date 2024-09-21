from engine import *


class Ceruledge(PokemonBase):
    _species='Ceruledge'
    _types=['Fire','Ghost']
    _gender='Female'
    _ability=['Inverse Armor']
    _move_1=('Bitter Blade',90,100,'Physical','Fire',0,['contact'])
    _move_2=('Shadow Claw',70,100,'Physical','Ghost',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_type_effect(self):
        move_type=self['act']['type']
        target_types=self.target['types']
        effect=1
        for tt in target_types:
            effect*=TYPEEFFECTIVENESS[move_type][tt]
        if self['act']['category']=='Physical':
            if effect!=0: effect=1/effect
        return effect
    
    def get_crit(self):
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        if self['act']['id']=='Shadow Claw':
            crit_ratio=min(3,crit_ratio+1)
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit

    def move_1(self): # Bitter Blade
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.restore(int(1/2*damage),'drain')
    
    def move_2(self): # Shadow Claw
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
