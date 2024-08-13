from engine import *


class Darmanitan(PokemonBase):
    _species='Darmanitan'
    _types=['Fire']
    _gender='Male'
    _ability=['Gorilla Tactics']
    _move_1=('Flare Blitz',120,100,'Physical','Fire',0,['contact'])
    _move_2=('Crunch',80,100,'Physical','Dark',0,['contact'])
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
        if key=='atk':
            stat_ratio*=1.5
        return int(stat*stat_ratio)

    def move_1(self): # Flare Blitz
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: self.target.set_status('BRN')
            if damage>0:
                self.take_damage(int(0.33*damage),'recoil')
        self.state['canact']='Flare Blitz'
    
    def move_2(self): # Crunch
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100: self.target.set_boost('def',-1)
        self.state['canact']='Crunch'
