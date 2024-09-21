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
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('Flinch',counter=0)

    def move_2(self): # Tail Spike
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('BLEED',counter=0)

# ----------

@Increment(Bladecuga,'_move_3')
def value():
    return ('Savage Bite',75,100,'Physical','Dark',0,[])

@Increment(Bladecuga)
def move_3(self): # Savage Bite
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_boost('def',-1)

# ----------

@Increment(Bladecuga,'_move_4')
def value():
    return ('Pounce',60,100,'Physical','Normal',0,[])

@Increment(Bladecuga)
def move_4(self): # Pounce
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_boost('spe',+1,'self')

# ----------

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
    if self['status'] or self.env.get('Misty Terrain'):
        return
    if x=='BRN':
        if self.istype('Fire'):
            return
    elif x=='PAR':
        if self.istype('Electric'):
            return
    elif x=='PSN':
        if self.istype('Poison') or self.istype('Steel'):
            return
    elif x=='TOX':
        if self.istype('Poison') or self.istype('Steel'):
            return
    elif x=='FRZ':
        if self.istype('Ice'):
            return
    elif x=='SLP':
        if self.env.get("Electric Terrain"):
            return
    self._set_status(x)
