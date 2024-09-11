from engine import *


class ChenLoong(PokemonBase):
    _species='Chen-Loong'
    _types=['Ice','Water']
    _gender='Female'
    _ability=['Snow Warning']
    _move_1=('Blizzard',110,70,'Special','Ice',0,[])
    _move_2=('Hydro Pump',110,80,'Special','Water',0,[])
    _base=(150,85,90,105,110,60)
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_env('Snow','weather')

    def get_accuracy(self):
        acc=self['act']['accuracy']
        if self['act']['id']=='Blizzard' and self.get_env('Snow'):
            acc=1e5
        acc_mult=[1.0,1.33,1.67,2.0]
        if self['boosts']['accuracy']>=0:
            acc*=acc_mult[self['boosts']['accuracy']]
        else:
            acc/=acc_mult[self['boosts']['accuracy']]
        acc*=self.target.get_evasion()
        return acc/100

    def move_1(self): # Blizzard
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: self.target.set_status('FRZ')
    
    def move_2(self): # Surf
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            if self.target['conditions'].get('DIVE'):
                damage*=2
            self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(ChenLoong,'_move_3')
def value():
    return ('Calm Mind',0,100000,'Status','Psychic',0,[])

@Increment(ChenLoong)
def move_3(self): # Calm Mind
    self.set_boost('spa',+1,'self')
    self.set_boost('spd',+1,'self')

# -------------------------------------------------------------

@Increment(ChenLoong,'_move_4')
def value():
    return ('Thunderbolt',90,100,'Special','Electric',0,[])

@Increment(ChenLoong)
def move_4(self): # Thunderbolt
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100: self.target.set_status('PAR')

# -------------------------------------------------------------

@Increment(ChenLoong,'_ability')
def value():
    return ['Snow Warning','Aurora Bless']

@Increment(ChenLoong)
def onswitch(self):
    self.set_env('Snow','weather')
    self.set_env('Aurora Veil',side='self',counter=0,max_count=5)

@Increment(ChenLoong)
def _take_damage_attack(self,x):
    self.register_act_taken()
    if self.get_env('Aurora Veil',side='self'):
        if self['act_taken']['category']=='Physical' or self['act_taken']['category']=='Special':
            x//=2
    self.state['hp']=max(0,self['hp']-x)
    if self['hp']==0:
        self.state['status']='FNT'

# -------------------------------------------------------------

@Increment(ChenLoong,'_move_5')
def value():
    return ('Rest',0,100000,'Status','Psychic',0,[])

@Increment(ChenLoong)
def move_5(self): # Rest
    if not self.isstatus('SLP') and self['hp']<self['max_hp']:
        self.state['status']=None
        self.set_status('SLP')
        self.state['hp']=self['max_hp']
        self.log("ChenLoong gets into sleep and restores all its HP.")
