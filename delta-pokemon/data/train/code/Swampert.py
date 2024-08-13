from engine import *


class Swampert(PokemonBase):
    _species='Swampert'
    _types=['Water','Ground']
    _gender='Female'
    _ability=['Torrent']
    _move_1=('Liquidation',85,100,'Physical','Water',0,['contact'])
    _move_2=('Earthquake',100,100,'Physical','Ground',0,[])
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
        if key=='atk' or key=='spa' and self.move['type']=='Water' and self['hp']<self['max_hp']//3:
            stat_ratio*=1.5
        return int(stat*stat_ratio)

    def move_1(self): # Liquidation
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100: self.target.set_boost('def',-1)
    
    def move_2(self): # Earthquake
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
