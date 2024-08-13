from engine import *


class Tyranitar(PokemonBase):
    _species='Tyranitar'
    _types=['Rock','Dark']
    _gender='Male'
    _ability=['Sand Stream']
    _move_1=('Roar of Rock',120,90,'Physical','Rock',0,[])
    _move_2=('Earthquake',100,100,'Physical','Ground',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_env('SANDSTORM')

    def get_type_effect(self):
        move_type=self['act']['type']
        target_types=self.target['types']
        effect=1
        for tt in target_types:
            if tt in ['Fighting','Fairy'] and self['act']['id']=='Roar of Rock':
                effect*=2
            else:
                effect*=TYPEEFFECTIVENESS[move_type][tt]
        return effect

    def move_1(self): # Roar of Rock
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Earthquake
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Tyranitar,'_move_3')
def value():
    return ('Wild Release',0,100000,'Status','Dark',0,[])

@Increment(Tyranitar)
def move_3(self): # Wild Release
    self.set_boost('atk',1,'self')
    self.set_boost('spe',1,'self')
    if self.env.get('SANDSTORM'):
        self.set_boost('atk',1,'self')
        self.set_boost('spe',1,'self')

# -------------------------------------------------------------

@Increment(Tyranitar,'_move_4')
def value():
    return ('Fire Fang',65,95,'Physical','Fire',0,['contact'])

@Increment(Tyranitar)
def move_4(self): # Fire Fang
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint():
            if rnd()<0.1:
                self.target.set_status('BRN')
            if rnd()<0.1:
                self.target.set_condition('FLINCH',counter=0)

# -------------------------------------------------------------

@Increment(Tyranitar,'_ability')
def value():
    return ['Sand Stream','Sturdy']

@Increment(Tyranitar)
def _take_damage_attack(self,x):
    self.register_act_taken()
    if self['hp']==self['max_hp'] and x>=self['hp']:
        self.state['hp']=max(1,self['hp']-x)
    else:
        self.state['hp']=max(0,self['hp']-x)
    if self['hp']==0:
        self.state['status']='FNT'

# -------------------------------------------------------------

@Increment(Tyranitar,'_move_5')
def value():
    return ('Taunt',0,100,'Status','Dark',0,[])

@Increment(Tyranitar)
def move_5(self): # Taunt
    self.target.set_condition('TAUNT',counter=0)

@Increment(Tyranitar)
def disable_moves(self,moves):
    disabled = []
    for m in moves:
        if self.target['conditions'].get('TAUNT') and moves[m]['category']=='Status':
            disabled += [m]
    return disabled

@Increment(Tyranitar)
def endturn(self):
    if self.target['conditions'].get('TAUNT'):
        self.target['conditions']['TAUNT']['counter']+=1
        if self.target['conditions']['TAUNT']['counter']==3:
            del self.target['conditions']['TAUNT']
