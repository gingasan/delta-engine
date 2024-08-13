from engine import *


class Scizor(PokemonBase):
    _species='Scizor'
    _types=['Bug','Steel']
    _gender='Female'
    _ability=['Technician']
    _move_1=('Bullet Punch',40,100,'Physical','Steel',1,['contact'])
    _move_2=('Bug Tangle',15,90,'Physical','Bug',0,[])
    def __init__(self):
        super().__init__()

    def get_power(self):
        power=self['act']['power']
        if power<=60:
            power=int(power*1.5)
        return int(power*self.get_weather_power_mult())
    
    def move_1(self): # Bullet Punch
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Bug Tangle
        hit=True; i=0
        while hit and i<4:
            damage_ret=self.get_damage()
            if damage_ret['miss']: break
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True
