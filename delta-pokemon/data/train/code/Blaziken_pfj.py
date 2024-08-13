from engine import *


class Blaziken(PokemonBase):
    _species='Blaziken'
    _types=['Fire','Fighting']
    _gender='Male'
    _ability=['Combustion']
    _move_1=('Fire Blast',110,85,'Special','Fire',0,[])
    _move_2=('Sky Uppercut',85,90,'Physical','Fighting',0,['contact'])
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
        if key=='atk' and self['hp']<self['max_hp']//2:
            stat_ratio*=2
        return int(stat*stat_ratio)

    def move_1(self): # Fire Blast
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100: self.target.set_status('BRN')

    def move_2(self): # Sky Uppercut
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: self.target.set_condition('FLINCH',counter=0)

    def get_crit(self):
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        if self['act']['id']=='Sky Uppercut':
            crit_ratio=min(3,crit_ratio+2)
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit
