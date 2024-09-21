from engine import *


class Blaziken(PokemonBase):
    _species='Blaziken'
    _types=['Fire','Fighting']
    _gender='Male'
    _ability=['Burn Brace']
    _move_1=('Fire Blast',120,85,'Special','Fire',0,[])
    _move_2=('High Jump Kick',130,90,'Physical','Fighting',0,['contact'])
    def __init__(self):
        super().__init__()

    def set_status(self,x):
        if x=='FRZ' and self['hp']<=self['max_hp']//3:
            return
        if self['status'] or self.env.get('Misty Terrain'):
            return
        if x=='BRN':
            if self.istype('Fire'):
                return
        elif x=='PAR':
            if self.istype('Electric'):
                return
        elif x=='PSN':
            if self.istype('Poison') or self.istype('Steel'):
                return
        elif x=='TOX':
            if self.istype('Poison') or self.istype('Steel'):
                return
        elif x=='FRZ':
            if self.istype('Ice'):
                return
        elif x=='SLP':
            if self.env.get("Electric Terrain"):
                return
        self._set_status(x)

    def move_1(self): # Fire Blast
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('BRN')
    
    def move_2(self): # High Jump Kick
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
        else:
            crash_damage=self['max_hp']//2
            self.take_damage(crash_damage,'recoil')
