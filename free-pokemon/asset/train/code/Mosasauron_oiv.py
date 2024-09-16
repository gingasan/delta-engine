from engine import *


class Mosasauron(PokemonBase):
    _species='Mosasauron'
    _types=['Water','Dragon']
    _gender='Female'
    _ability=['Marine Apex']
    _move_1=('Tidal Fang',80,100,'Physical','Water',0,[])
    _move_2=('Fierce Gaze',70,100,'Special','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def get_other_mult(self):
        mult=1
        if self.isstatus('BRN') and self['act']['category']=='Physical':
            mult*=0.5
        if self.target.istype('Water'):
            mult*=1.2
        return mult

    def move_1(self): # Tidal Fang
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('def',-1)

    def move_2(self): # Fierce Gaze
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def get_power(self):
        power=self['act']['power']
        if self.target.isstatus('PAR') and self['act']['id']=='Fierce Gaze':
            power*=2
        return int(power*self.get_weather_power_mult())

# ----------

@Increment(Mosasauron,'_move_3')
def value():
    return ('Scale Shield',0,100000,'Status','Dragon',0,[])

@Increment(Mosasauron)
def move_3(self): # Scale Shield
    self.set_boost('def',+1,'self')
    self.set_boost('spd',+1,'self')

# ----------

@Increment(Mosasauron,'_move_4')
def value():
    return ('Ancient Tide',100,90,'Special','Water',0,[])

@Increment(Mosasauron)
def move_4(self): # Ancient Tide
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_boost('spe',-1)

# ----------

@Increment(Mosasauron,'_ability')
def value():
    return ['Marine Apex','Amphibious Armor']

@Increment(Mosasauron)
def get_stat(self,key,boost=None):
    stat=self['stats'][key]
    boost=self['boosts'][key] if not boost else boost
    stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
    if boost<0:
        stat_ratio=1/stat_ratio
    stat_ratio*=self.get_weather_stat_mult(key)
    if key=='spe' and self.isstatus('PAR'):
        stat_ratio*=0.5
    if key in ['def','spd'] and self.env.get('Rain'):
        stat_ratio*=1.5
    return int(stat*stat_ratio)
