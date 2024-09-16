from engine import *


class Barraskewda(PokemonBase):
    _species='Barraskewda'
    _types=['Water']
    _gender='Male'
    _ability=['Swift Swim']
    _move_1=('Liquidation',85,100,'Physical','Water',0,['contact'])
    _move_2=('Close Combat',120,100,'Physical','Fighting',0,['contact'])
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
        if key=='spe' and self.env.get('Rain'):
            stat_ratio*=2
        return int(stat*stat_ratio)

    def move_1(self): # Liquidation
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('def',-1)

    def move_2(self): # Close Combat
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('def',-1,'self')
            self.set_boost('spd',-1,'self')

# ----------

@Increment(Barraskewda,'_move_3')
def value():
    return ('Crunch',80,100,'Physical','Dark',0,['contact'])

@Increment(Barraskewda)
def move_3(self): # Crunch
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_boost('def',-1)
