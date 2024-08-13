from engine import *


class Blazorus(PokemonBase):
    _species='Blazorus'
    _types=['Fire','Fighting']
    _gender='Male'
    _ability=['Blaze Soul']
    _move_1=('Inferno Fist',90,85,'Physical','Fire',0,['contact'])
    _move_2=('Triple Strike',25,100,'Physical','Fighting',0,['contact'])
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
        if key in['atk','spa'] and self['hp']<self['max_hp']//2:
            stat_ratio*=2
        return int(stat*stat_ratio)

    def move_1(self): # Inferno Fist
        self.set_boost('crit',+2)
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('BRN')
        self.set_boost('crit',-2)

    def move_2(self): # Triple Strike
        hit=True; i=0
        while hit and i<3:
            damage_ret=self.get_damage()
            if damage_ret['miss']: break
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True
