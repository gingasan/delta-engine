from engine import *


class Sandslash(PokemonBase):
    _species='Sandslash'
    _types=['Steel','Ice']
    _gender='Male'
    _ability=['Slush Rush']
    _move_1=('Triple Axel',20,90,'Physical','Ice',0,[])
    _move_2=('Rapid Spin',50,100,'Physical','Normal',0,[])
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
        if key=='spe' and self.get_env('Snow'):
            stat_ratio*=2
        return int(stat*stat_ratio)

    def move_1(self): # Triple Axel
        hit=True; i=0
        while hit and i<3:
            damage_ret=self.get_damage()
            if damage_ret['miss']: break
            damage=damage_ret['damage']
            damage=int(damage*1.5**i)
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True

    def move_2(self): # Rapid Spin
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if self['conditions'].get('LEECH_SEED'):
                del self['conditions']['LEECH_SEED']
            if self['conditions'].get('TRAP'):
                del self['conditions']['TRAP']
            self.set_boost('spe',+1,'self')

# ----------

@Increment(Sandslash,'_move_3')
def value():
    return ('Iron Head',80,100,'Physical','Steel',0,['contact'])

@Increment(Sandslash)
def move_3(self): # Iron Head
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('FLINCH',counter=0)

# ----------

@Increment(Sandslash,'_ability')
def value():
    return ['Slush Rush','Raging Spikes']

@Increment(Sandslash)
def move_1(self): # Triple Axel
    hit=True; i=0
    n_hits=3 if self['hp']>self['max_hp']//2 else 4
    while hit and i<n_hits:
        damage_ret=self.get_damage()
        if damage_ret['miss']: break
        damage=damage_ret['damage']
        damage=int(damage*1.5**i)
        self.target.take_damage(damage)
        i+=1; hit=False if self.target.isfaint() else True
