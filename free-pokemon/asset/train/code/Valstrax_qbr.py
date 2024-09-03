from engine import *


class Valstrax(PokemonBase):
    _species='Valstrax'
    _types=['Dragon','Fire']
    _gender='Neutral'
    _ability=['Energy Overflow']
    _move_1=('Dragon Laser',120,90,'Special','Dragon',0,[])
    _move_2=('Explosive Blast',100,85,'Special','Fire',0,[])
    def __init__(self):
        super().__init__()
    
    def endturn(self):
        if self['hp']<self['max_hp']//3:
            self.set_boost('spa',2,'self')
        else:
            self.set_boost('spe',1,'self')

    def move_1(self): # Dragon Laser
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('spd',-2)

    def move_2(self): # Explosive Blast
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_status('BRN')

# -------------------------------------------------------------

@Increment(Valstrax,'_move_3')
def value():
    return ('Roost',0,100000,'Status','Flying',0,[])

@Increment(Valstrax)
def move_3(self): # Roost
    self.restore(self['max_hp']//2,'heal')

# -------------------------------------------------------------

@Increment(Valstrax,'_move_4')
def value():
    return ('Flare Cascade',80,100,'Special','Fire',0,[])

@Increment(Valstrax)
def move_4(self): # Flare Cascade
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint():
            if rnd()<30/100:
                self.target.set_status('BRN')
            if rnd()<10/100:
                self.target.set_status('PAR')

# -------------------------------------------------------------

@Increment(Valstrax,'_ability')
def value():
    return ['Energy Overflow','Guts']

@Increment(Valstrax)
def get_stat(self,key,boost=None):
    stat=self['stats'][key]
    boost=self['boosts'][key] if not boost else boost
    stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
    if boost<0:
        stat_ratio=1/stat_ratio
    stat_ratio*=self.get_weather_stat_mult(key)
    if key=='spe' and self.isstatus('PAR'):
        stat_ratio*=0.5
    if key=='spa' and self['status']:
        stat_ratio*=1.5
    return int(stat*stat_ratio)

@Increment(Valstrax)
def get_other_mult(self):
    return 1.
