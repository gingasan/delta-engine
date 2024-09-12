from engine import *


class Glimmerine(PokemonBase):
    _species='Glimmerine'
    _types=['Fairy','Water']
    _gender='Female'
    _ability=['Dream Weaver']
    _move_1=('Lunar Ray',70,100,'Special','Fairy',0,[])
    _move_2=('Aqua Veil',80,95,'Special','Water',0,[])
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
        if key=='spa' and self.target.isstatus('SLP'):
            stat_ratio*=1.5
        return int(stat*stat_ratio)
    
    def move_1(self):  # Lunar Ray
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self):  # Aqua Veil
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.restore(int(1/4*damage),'drain')

# ----------

@Increment(Glimmerine,'_move_3')
def value():
    return ('Hypnotic Pulse',0,75,'Status','Psychic',0,[])

@Increment(Glimmerine)
def move_3(self):  # Hypnotic Pulse
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        self.target.set_status('SLP')

# ----------

@Increment(Glimmerine,'_move_4')
def value():
    return ('Fairy Shield',0,100000,'Status','Fairy',0,[])

@Increment(Glimmerine)
def move_4(self):  # Fairy Shield
    self.set_boost('def',+1,'self')
    self.set_boost('spd',+1,'self')

# ----------

@Increment(Glimmerine,'_ability')
def value():
    return ['Dream Weaver','Aqua Spirit']

@Increment(Glimmerine)
def move_2(self):  # Aqua Veil
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_condition('CONFUSION',counter=0)
        self.restore(int(1/4*damage),'drain')

# ----------

@Increment(Glimmerine,'_move_5')
def value():
    return ('Mystic Wave',90,100,'Special','Water',0,[])

@Increment(Glimmerine)
def move_5(self):  # Mystic Wave
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_condition('CONFUSION',counter=0)
