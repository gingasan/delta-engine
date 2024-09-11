from engine import *


class Venusaur(PokemonBase):
    _species='Venusaur'
    _types=['Grass','Poison']
    _gender='Female'
    _ability=['Chlorophyll']
    _move_1=('Growth',0,100000,'Status','Normal',0,[])
    _move_2=('Giga Drain',75,100,'Special','Grass',0,[])
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
        if key=='spe' and self.get_env('Sunlight'):
            stat_ratio*=2
        return int(stat*stat_ratio)

    def move_1(self): # Growth
        self.set_boost('atk',+1,'self')
        self.set_boost('spa',+1,'self')
        if self.get_env('Sunlight'):
            self.set_boost('atk',+1,'self')
            self.set_boost('spa',+1,'self')

    def move_2(self): # Giga Drain
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.restore(int(1/2*damage),'drain')

# -------------------------------------------------------------

@Increment(Venusaur,'_move_3')
def value():
    return ('Earth Power',90,100,'Special','Ground',0,[])

@Increment(Venusaur)
def move_3(self): # Earth Power
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_boost('spd',-1)

# -------------------------------------------------------------

@Increment(Venusaur,'_move_4')
def value():
    return ('Leech Seed',0,90,'Status','Grass',0,[])

@Increment(Venusaur)
def move_4(self): # Leech Seed
    self.target.set_condition('LEECH_SEED',counter=0)

@Increment(Venusaur)
def endturn(self):
    if self.target['conditions'].get('LEECH_SEED'):
        self.target.take_damage(self.target['max_hp']//8,'loss')
        self.restore(self.target['max_hp']//8,'drain')
        self.target['conditions']['LEECH_SEED']['counter']+=1
