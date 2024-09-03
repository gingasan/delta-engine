from engine import *


class Hippowdon(PokemonBase):
    _species='Hippowdon'
    _types=['Ground']
    _gender='Male'
    _ability=['Toxic Boost']
    _move_1=('Earthquake',100,100,'Physical','Ground',0,[])
    _move_2=('Iron Head',80,100,'Physical','Steel',0,['contact'])
    def __init__(self):
        super().__init__()
    
    def get_stat(self,key,boost=None):
        stat=self['stats'][key]
        boost=self['boosts'][key] if not boost else boost
        stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
        if boost<0:
            stat_ratio=1/stat_ratio
        stat_ratio*=self.get_weather_stat_mult(key)
        if key=='spe' and self.isstatus('PAR'):
            stat_ratio*=0.5
        if key=='atk' and self['status']=='PSN':
            stat_ratio*=1.5
        return int(stat*stat_ratio)

    def move_1(self): # Earthquake
        damage_ret=self.get_damage() 
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Iron Head
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('FLINCH',counter=0)
