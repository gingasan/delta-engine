from engine import *


class Blaziken(PokemonBase):
    _species='Blaziken'
    _types=['Fire','Fighting']
    _gender='Male'
    _ability=['Blaze']
    _move_1=('Blaze Kick II',85,90,'Physical','Fire',1,['contact'])
    _move_2=('Close Combat',120,100,'Physical','Fighting',0,['contact'])
    _base=(80,160,80,80,80,120)
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
        if (key=='atk' or key=='spa') and self['act']['type']=='Fire' and self['hp']<=self['max_hp']//3:
            stat_ratio*=1.5
        return int(stat*stat_ratio)

    def get_crit(self):
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        if self['act']['id']=='Blaze Kick II':
            crit_ratio=min(3,crit_ratio+1)
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit

    def move_1(self): # Blaze Kick II
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: self.target.set_status('BRN')

    def move_2(self): # Close Combat
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('def',-1,'self')
            self.set_boost('spd',-1,'self')

# -------------------------------------------------------------

@Increment(Blaziken,'_move_3')
def value():
    return ('Brave Bird',120,100,'Physical','Flying',0,['contact'])

@Increment(Blaziken)
def move_3(self): # Brave Bird
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.take_damage(int(0.33*damage),'recoil')

# -------------------------------------------------------------

@Increment(Blaziken,'_move_4')
def value():
    return ('Swords Dance',0,100000,'Status','Normal',0,[])

@Increment(Blaziken)
def move_4(self): # Swords Dance
    self.set_boost('atk',+2,'self')

# -------------------------------------------------------------

@Increment(Blaziken,'_ability')
def value():
    return ['Blaze','Speed Boost']

@Increment(Blaziken)
def endturn(self):
    self.log('Blaziken speeds up.',color='red')
    self.set_boost('spe',1,'self')

# -------------------------------------------------------------

@Increment(Blaziken,'_move_5')
def value():
    return ('Drain Punch',75,100,'Physical','Fighting',0,['contact','punch'])

@Increment(Blaziken)
def move_5(self): # Drain Punch
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.restore(int(1/2*damage),'drain')
