from engine import *


class Blackwing(PokemonBase):
    _species='Blackwing'
    _types=['Dark','Flying']
    _gender='Male'
    _ability=['Black Feather']
    _move_1=('Dark Tempest',80,100,'Special','Dark',0,[])
    _move_2=('Wing Beat',85,90,'Physical','Flying',0,[])
    def __init__(self):
        super().__init__()
    
    def onswitch(self):
        self.set_condition('BLACK_FEATHER',counter=3)
    
    def _take_damage_attack(self,x):
        self.register_act_taken()
        if self['conditions'].get('BLACK_FEATHER'):
            x=int(x*0.5)
            self['conditions']['BLACK_FEATHER']['counter']-=1
            if self['conditions']['BLACK_FEATHER']['counter']==0:
                del self['conditions']['BLACK_FEATHER']
        self.state['hp']=max(0,self['hp']-x)
        if self['hp']==0:
            self.state['status']='FNT'
    
    def endturn(self):
        if self['conditions'].get('BLACK_FEATHER'):
            self.take_damage(self['max_hp']//8,'loss')
    
    def move_1(self): # Dark Tempest
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('def',-1)
    
    def move_2(self): # Wing Beat
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_condition('FLINCH',counter=0)

# -------------------------------------------------------------

@Increment(Blackwing,'_move_3')
def value():
    return ('Shadow Claw',70,100,'Physical','Dark',0,['contact'])

@Increment(Blackwing)
def move_3(self): # Shadow Claw
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)

@Increment(Blackwing)
def get_crit(self):
    crit_mult=[0,24,8,2,1]
    crit_ratio=self['boosts']['crit']
    if self['act']['id']=='Shadow Claw':
        crit_ratio=min(3,crit_ratio+1)
    crit=False
    if rnd()*crit_mult[crit_ratio+1]<1:
        crit=True
    return crit

# -------------------------------------------------------------

@Increment(Blackwing,'_move_4')
def value():
    return ('Feather Storm',0,100000,'Status','Flying',0,[])

@Increment(Blackwing)
def move_4(self): # Feather Storm
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        self.target.set_boost('accuracy',-2)

# -------------------------------------------------------------

@Increment(Blackwing,'_ability')
def value():
    return ['Black Feather','Shadow Glide']

@Increment(Blackwing)
def _take_damage_attack(self,x):
    self.register_act_taken()
    if self['conditions'].get('BLACK_FEATHER'):
        x=int(x*0.5)
        self['conditions']['BLACK_FEATHER']['counter']-=1
        if self['conditions']['BLACK_FEATHER']['counter']==0:
            del self['conditions']['BLACK_FEATHER']
    self.state['hp']=max(0,self['hp']-x)
    if self['act_taken']['category']=='Physical':
        self.set_boost('spe',+2)
    if self['hp']==0:
        self.state['status']='FNT'

# -------------------------------------------------------------

@Increment(Blackwing,'_move_5')
def value():
    return ('Night Dive',90,95,'Physical','Dark',0,['contact'])

@Increment(Blackwing)
def move_5(self): # Night Dive
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.restore(int(0.5*damage),'drain')
