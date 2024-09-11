from engine import *


class Charizard(PokemonBase):
    _species='Charizard'
    _types=['Fire','Flying']
    _gender='Male'
    _ability=['Desolate Land']
    _move_1=('Flamethrower',90,100,'Special','Fire',0,[])
    _move_2=('Air Slash',75,95,'Special','Flying',0,[])
    def __init__(self):
        super().__init__()

    def get_weather_stat_mult(self,key):
        if self.get_env('Sandstorm') and key=='spd' and 'Rock' in self['types']:
            return 1.5
        if self.get_env('Snow') and key=='def' and 'Ice' in self['types']:
            return 1.5
        if self.get_env('Sunlight') and key=='spa':
            return 1.5
        return 1.
    
    def endturn(self):
        if self.get_env('Sunlight'):
            self.take_damage(self['max_hp']//8,'loss')
    
    def move_1(self): # Flamethrower
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                if self.get_env('Sunlight') or rnd()<10/100:
                    self.target.set_status('BRN')
    
    def move_2(self): # Air Slash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('FLINCH',counter=0)
