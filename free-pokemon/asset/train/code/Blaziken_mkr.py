from engine import *


class Blaziken(PokemonBase):
    _species='Blaziken'
    _types=['Fire','Fighting']
    _gender='Male'
    _ability=['Blaze Rush']
    _move_1=('Inferno Kick',100,100,'Physical','Fire',0,[])
    _move_2=('Flaming Charge',80,100,'Physical','Fire',0,['contact'])
    def __init__(self):
        super().__init__()
        
    def endturn(self):
        if self.get_env('Sunlight'):
            self.set_boost('atk',1,'self')

    def get_crit(self):
        if self['act']['id']=='Inferno Kick':
            if self.get_env('Sunlight'):
                return True
            elif self.get_env('Rain'):
                return False
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit

    def move_1(self): # Inferno Kick
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:self.target.set_status('BRN')
    
    def move_2(self): # Flaming Charge
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('spd',1,'self')
