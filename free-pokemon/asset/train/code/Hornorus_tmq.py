from engine import *


class Hornorus(PokemonBase):
    _species='Hornorus'
    _types=['Steel','Ground']
    _gender='Neutral'
    _ability=['Iron Hide']
    _move_1=('Horn Smash',90,85,'Physical','Steel',0,['contact'])
    _move_2=('Steel Guard',0,100000,'Status','Steel',0,[])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        self.register_act_taken()
        if self['act_taken']['category']=='Physical':
            x=int(x*0.75)
        self.state['hp']=max(0,self['hp']-x)
        if self['hp']==0:
            self.state['status']='FNT'

    def move_1(self): # Horn Smash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('def',-1)

    def move_2(self): # Steel Guard
        self.set_boost('def',+1,'self')
        self.set_boost('spd',+1,'self')

# -------------------------------------------------------------

@Increment(Hornorus,'_move_3')
def value():
    return ('Groundquake',100,90,'Special','Ground',0,[])

@Increment(Hornorus)
def move_3(self): # Groundquake
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('FLINCH',counter=0)

# -------------------------------------------------------------

@Increment(Hornorus,'_move_4')
def value():
    return ('Armored Strike',80,100000,'Physical','Steel',0,[])

@Increment(Hornorus)
def move_4(self): # Armored Strike
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_condition('TEMP_SHIELD',counter=0)

@Increment(Hornorus)
def _take_damage_attack(self,x):
    self.register_act_taken()
    if self['conditions'].get('TEMP_SHIELD'):
        x=int(x*0.75)
    if self['act_taken']['category']=='Physical':
        x=int(x*0.75)
    self.state['hp']=max(0,self['hp']-x)
    if self['hp']==0:
        self.state['status']='FNT'

@Increment(Hornorus)
def endturn(self):
    if self['conditions'].get('TEMP_SHIELD'):
       self['conditions']['TEMP_SHIELD']['counter']+=1
       if self['conditions']['TEMP_SHIELD']['counter']==2:
           del self['conditions']['TEMP_SHIELD']

# -------------------------------------------------------------

@Increment(Hornorus,'_ability')
def value():
    return ['Iron Hide','Horn Charge']

@Increment(Hornorus)
def move_1(self): # Horn Smash
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_boost('def',-1)
        self.set_boost('atk',+1,'self')

@Increment(Hornorus)
def move_4(self): # Armored Strike
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_condition('TEMP_SHIELD',counter=0)
        self.set_boost('atk',+1,'self')
