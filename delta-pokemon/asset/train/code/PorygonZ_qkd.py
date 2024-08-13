from engine import *


class PorygonZ(PokemonBase):
    _species='Porygon-Z'
    _types=['Normal']
    _gender='Unknown'
    _ability=['Galvanize']
    _move_1=('Tri Attack',80,100,'Special','Normal',0,[])
    _move_2=('Tri Beam',45,100,'Special','Normal',0,[])
    def __init__(self):
        super().__init__()
    
    def get_power(self):        
        power=self['act']['power']
        if self['act']['type']=='Normal':
            self['act']['type']='Electric'
            power*=1.3
        return int(power*self.get_weather_power_mult())
    
    def move_1(self): # Tri Attack
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage'] 
            self.target.take_damage(damage)
            if not self.target.isfaint():
                r=rnd()
                if r<20/100:
                    self.target.set_status(rndc(['PAR','BRN','FRZ']))
    
    def move_2(self): # Tri Beam
        hit=True; i=0
        while hit and i<3:
            damage_ret=self.get_damage()
            if damage_ret['miss']: break
            damage=damage_ret['damage']
            self.target.take_damage(damage)  
            i+=1; hit=False if self.target.isfaint() else True
