from engine import *


class Greninja(PokemonBase):
    _species='Greninja'
    _types=['Water','Dark']
    _gender='Male'
    _ability=['Proten']
    _move_1=('Hydro Pump',110,80,'Special','Water',0,[])
    _move_2=('Dark Pulse',80,100,'Special','Dark',0,[])
    def __init__(self):
        super().__init__()
    
    def move_1(self): # Hydro Pump
        self.state['types']=[self['act']['type']]
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Dark Pulse
        self.state['types']=[self['act']['type']]
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('Flinch',counter=0)
