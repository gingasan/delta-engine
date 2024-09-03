from engine import *


class Bladecuga(PokemonBase):
    _species='Bladecuga'
    _types=['Dark','Flying']
    _gender='Female'
    _ability=['Razor Wings']
    _move_1=('Wing Slash',85,95,'Physical','Flying',0,[])
    _move_2=('Tail Spike',100,90,'Physical','Dark',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_boost('accuracy',1,'self')

    def get_power(self):
        power=self['act']['power']
        if self['act']['type']=='Flying':
            power*=1.3
        return int(power*self.get_weather_power_mult())

    def endturn(self):
        if self.target['conditions'].get('BLEED'):
            self.target.take_damage(self.target['max_hp']//16,'loss')
            self.target['conditions']['BLEED']['counter']+=1
            if self.target['conditions']['BLEED']['counter']==3:
                del self.target['conditions']['BLEED']

    def move_1(self): # Wing Slash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('FLINCH',counter=0)

    def move_2(self): # Tail Spike
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('BLEED',counter=0)

# -------------------------------------------------------------

@Increment(Bladecuga,'_move_3')
def value():
    return ('Savage Bite',75,100,'Physical','Dark',0,[])

@Increment(Bladecuga)
def move_3(self): # Savage Bite
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_boost('def',-1)

# -------------------------------------------------------------

@Increment(Bladecuga,'_move_4')
def value():
    return ('Pounce',60,100,'Physical','Normal',0,[])

@Increment(Bladecuga)
def move_4(self): # Pounce
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_boost('spe',+1,'self')

# -------------------------------------------------------------

@Increment(Bladecuga,'_ability')
def value():
    return ['Razor Wings','Spike Rage']

@Increment(Bladecuga)
def get_stat(self,key,boost=None):
    stat=self['stats'][key]
    boost=self['boosts'][key] if not boost else boost
    stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
    if boost<0:
        stat_ratio=1/stat_ratio
    stat_ratio*=self.get_weather_stat_mult(key)
    if key=='spe' and self.isstatus('PAR'):
        stat_ratio*=0.5
    if key=='atk' and self['hp']<=self['max_hp']//3:
        stat_ratio*=1.5
    return int(stat*stat_ratio)

@Increment(Bladecuga)
def set_status(self,x):
    if self['hp']<=self['max_hp']//3:
        return
    if self['status'] or self.env.get('MISTY_TERRAIN'):
        return
    if x=='BRN':
        if not self.istype('Fire'):
            self.state['status']={x:{'counter':0}}
    elif x=='PAR':
        if not self.istype('Electric'):
            self.state['status']={x:{'counter':0}}
    elif x=='PSN':
        if not self.istype('Poison') and not self.istype('Steel'):
            self.state['status']={x:{'counter':0}}
    elif x=='TOX':
        if not self.istype('Poison') and not self.istype('Steel'):
            self.state['status']={x:{'counter':0}}
    elif x=='FRZ':
        if not self.istype('Ice'):
            self.state['status']={x:{'counter':0}}
    elif x=='SLP':
        self.state['status']={x:{'counter':0}}
