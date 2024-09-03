from engine import *


class Blastoise(PokemonBase):
    _species='Blastoise'
    _types=['Water']
    _gender='Male'
    _ability=['Torrent']
    _move_1=('Shell Smash',0,100000,'Status','Normal',0,[])
    _move_2=('Hydro Pump',110,80,'Special','Water',0,[])
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
        if key in ['atk','spa'] and self['act']['type']=='Water' and self['hp']<self['max_hp']//3:
            stat_ratio*=1.5
        return int(stat*stat_ratio)

    def move_1(self): # Shell Smash
        self.set_boost('def',-1,'self')
        self.set_boost('spd',-1,'self')
        self.set_boost('atk',+2,'self')
        self.set_boost('spa',+2,'self')
        self.set_boost('spe',+2,'self')

    def move_2(self): # Hydro Pump
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Blastoise,'_move_3')
def value():
    return ('Ice Beam',90,100,'Special','Ice',0,[])

@Increment(Blastoise)
def move_3(self): # Ice Beam
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_status('FRZ')

# -------------------------------------------------------------

@Increment(Blastoise,'_move_4')
def value():
    return ('Aura Sphere',80,100000,'Special','Fighting',0,[])

@Increment(Blastoise)
def move_4(self): # Aura Sphere
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
