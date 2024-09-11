from engine import *


class Aerodactyl(PokemonBase):
    _species='Aerodactyl'
    _types=['Rock','Flying']
    _gender='Male'
    _ability=['Tough Claws']
    _move_1=('Rock Slide',75,90,'Physical','Rock',0,[])
    _move_2=('Dual Wingbeat',40,90,'Physical','Flying',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_power(self):        
        power=self['act']['power']
        if 'property' in self['act'] and 'contact' in self['act']['property']:
            power*=1.3
        return int(power*self.get_weather_power_mult())
    
    def move_1(self): # Rock Slide
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('FLINCH',counter=0)

    def move_2(self): # Dual Wingbeat
        hit=True; i=0
        while hit and i<2:
            damage_ret=self.get_damage()
            if damage_ret['miss']: break
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True