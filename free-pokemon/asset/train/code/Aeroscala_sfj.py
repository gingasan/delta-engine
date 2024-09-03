from engine import *


class Aeroscala(PokemonBase):
    _species='Aeroscala'
    _types=['Dragon','Flying']
    _gender='Genderless'
    _ability=['Cyclone Shield']
    _move_1=('Wind Vortex',90,100,'Special','Flying',0,[])
    _move_2=('Metallic Scales',0,100000,'Status','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_condition('CYCLONE_SHIELD',counter=0)

    def endturn(self):
        if self['conditions'].get('CYCLONE_SHIELD'):
            self.set_boost('def',1,'self')
            self.set_boost('spd',1,'self')
            self['conditions']['CYCLONE_SHIELD']['counter']+=1
            if self['conditions']['CYCLONE_SHIELD']['counter']==3:
                del self['conditions']['CYCLONE_SHIELD']
        if self.target['conditions'].get('DIZZY'):
            if rnd()<50/100:
                self.target.set_status('SLP')
                del self.target['conditions']['DIZZY']
            else:
                self.target['conditions']['DIZZY']['counter']+=1
                if self.target['conditions']['DIZZY']['counter']==3:
                    del self.target['conditions']['DIZZY']

    def move_1(self): # Wind Vortex
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('DIZZY',counter=0)

    def move_2(self): # Metallic Scales
        self.set_boost('def',1,'self')
        self.set_boost('spd',1,'self')

# -------------------------------------------------------------

@Increment(Aeroscala,'_move_3')
def value():
    return ('Gale Force',110,75,'Special','Flying',0,[])

@Increment(Aeroscala)
def move_3(self): # Gale Force
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

@Increment(Aeroscala)
def get_crit(self):
    crit_mult=[0,24,8,2,1]
    crit_ratio=self['boosts']['crit']
    if self['act']['id']=='Gale Force':
        crit_ratio=min(3,crit_ratio+1)
    crit=True if rnd()*crit_mult[crit_ratio+1]<1 else False
    return crit

# -------------------------------------------------------------

@Increment(Aeroscala,'_move_4')
def value():
    return ('Ancient Wisdom',0,100000,'Status','Dragon',0,[])

@Increment(Aeroscala)
def move_4(self): # Ancient Wisdom
    self.set_boost('spa',1,'self')
    self.set_boost('spd',1,'self')

# -------------------------------------------------------------

@Increment(Aeroscala,'_ability')
def value():
    return ['Cyclone Shield','Tempest Fury']

@Increment(Aeroscala)
def get_power(self):
    power=self['act']['power']
    if self['act']['type']=='Flying' and self['hp']<self['max_hp']//3:
        power*=1.5
    return int(power*self.get_weather_power_mult())
