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
        if self['status'] or self.env.get('MISTY_TERRAIN'):
            return
        if x=='BRN':
            if not self.istype('Fire'):
                self.state['status']={x:{'counter':0}}
        elif x=='PAR':
            if not self.istype('Electric'):
                self.state['status']={x:{'counter':0}}
        elif x=='PSN':
            if not self.istype('Poison') and not self.istype('Steel'):
                self.state['status']={x:{'counter':0}}
        elif x=='TOX':
            if not self.istype('Poison') and not self.istype('Steel'):
                self.state['status']={x:{'counter':0}}
        elif x=='FRZ':
            if not self.istype('Ice'):
                self.state['status']={x:{'counter':0}}
        elif x=='SLP':
            self.state['status']={x:{'counter':0}}

    def move_1(self): # Fire Blast
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('BRN')
    
    def move_2(self): # High Jump Kick
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
        else:
            crash_damage=self['max_hp']//2
            self.take_damage(crash_damage,'recoil')
