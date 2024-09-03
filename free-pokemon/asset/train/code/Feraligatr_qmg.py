from engine import *


class Feraligatr(PokemonBase):
    _species='Feraligatr'
    _types=['Water']
    _gender='Male'
    _ability=['Sheer Force']
    _move_1=('Aqua Tail',90,90,'Physical','Water',0,['contact'])
    _move_2=('Storm Punch',75,100,'Physical','Fighting',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_power(self):
        power=self['act']['power']
        if self['act']['id'] in ['Crunch']:
            power*=1.3
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Aqua Tail
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Crunch
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
