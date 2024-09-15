from engine import *


class Oricorio(PokemonBase):
    _species='Oricorio'
    _types=['Electric','Flying']
    _gender='Female'
    _ability=['Dancer']
    _move_1=('Revelation Dance',90,100,'Special','Electric',0,[])
    _move_2=('Fleeting Moon',120,80,'Special','Flying',0,[])
    _base=(99,80,80,128,90,123)
    def __init__(self):
        super().__init__()

    def get_priority(self,move_id):
        if self._moves[move_id] in ['Revelation Dance']:
            return self._moves[move_id]['priority']+1
        return self._moves[move_id]['priority']

    def move_1(self): # Revelation Dance
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_status('PAR')
    
    def move_2(self): # Fleeting Moon
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.restore(int(0.3*damage),'drain')

# ----------
@Increment(Oricorio,'_move_3')
def value():
    return ('Calm Mind',0,100000,'Status','Psychic',0,[])

@Increment(Oricorio)
def move_3(self): # Calm Mind
    self.set_boost('spa',+1,'self')
    self.set_boost('spd',+1,'self')

# ----------

@Increment(Oricorio,'_move_4')
def value():
    return ('Roost',0,100000,'Status','Flying',0,[])

@Increment(Oricorio)
def move_4(self): # Roost
    self.restore(self['max_hp']//2,'heal')

# ----------

@Increment(Oricorio,'_ability')
def value():
    return ['Dancer','Swirling Winds']

@Increment(Oricorio)
def get_stat(self,key,boost=None):
    stat=self['stats'][key]
    boost=self['boosts'][key] if not boost else boost
    stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
    if boost<0:
        stat_ratio=1/stat_ratio
    stat_ratio*=self.get_weather_stat_mult(key)
    if key=='spe' and self.isstatus('PAR'):
        stat_ratio*=0.5
    if (key=='spa' or key=='spe') and self['conditions'].get('Hover'):
        stat_ratio*=1.3
    return int(stat*stat_ratio)

@Increment(Oricorio)
def endturn(self):
    if self['conditions'].get('Hover'):
        self['conditions']['Hover']['counter']+=1
        if self['conditions']['Hover']['counter']==1:
            del self['conditions']['Hover']

@Increment(Oricorio)
def move_1(self): # Revelation Dance
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_status('PAR')
        self.set_condition('Hover',counter=0)
        self.log('Oricorio enters the hover state, fully unleashing its power.',color='yellow')

# ----------

@Increment(Oricorio,'_move_5')
def value():
    return ('Teeter Dance',0,100,'Status','Normal',0,[])

@Increment(Oricorio)
def move_5(self): # Teeter Dance
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        self.target.set_condition('CONFUSION',counter=0)
    self.set_condition('Hover',counter=0)
    self.log('Oricorio enters the hover state, fully unleashing its power.',color='yellow')

@Increment(Oricorio)
def get_priority(self,move_id):
    if self._moves[move_id] in ['Revelation Dance','Teeter Dance']:
        return self._moves[move_id]['priority']+1
    return self._moves[move_id]['priority']

# ----------

@Increment(Oricorio,'_move_6')
def value():
    return ('Moonblast',95,100,'Special','Fairy',0,[])

@Increment(Oricorio)
def move_6(self): # Moonblast
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_boost('spa',-1)
