from engine import *


class Alloraptor(PokemonBase):
    _species='Alloraptor'
    _types=['Dragon','Steel']
    _gender='Male'
    _ability=['Prehistoric Fury']
    _move_1=('Iron Tail',100,75,'Physical','Steel',0,[])
    _move_2=('Fossil Fang',90,100,'Physical','Dragon',0,['contact'])
    def __init__(self):
        super().__init__()
    
    def get_power(self):
        power=self['act']['power']
        if self['act']['type']=='Dragon' and self['hp']<self['max_hp']//2:
            power*=1.5
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Iron Tail
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('def',-1)
    
    def move_2(self): # Fossil Fang
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('FLINCH',counter=0)

# -------------------------------------------------------------

@Increment(Alloraptor,'_move_3')
def value():
    return ('Ancient Roar',0,100000,'Status','Dragon',0,[])

@Increment(Alloraptor)
def move_3(self): # Ancient Roar
    if not self.target.isfaint():
        self.target.set_boost('atk',-1)
        self.target.set_boost('spa',-1)

# -------------------------------------------------------------

@Increment(Alloraptor,'_move_4')
def value():
    return ('Steel Slash',70,100,'Physical','Steel',0,['contact'])

@Increment(Alloraptor)
def move_4(self): # Steel Slash
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.set_boost('spe',+1,'self')

# -------------------------------------------------------------

@Increment(Alloraptor,'_ability')
def value():
    return ['Prehistoric Fury','Metallic Resilience']

@Increment(Alloraptor)
def set_status(self,x):
    if self['hp']>self['max_hp']//2:
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

# -------------------------------------------------------------

@Increment(Alloraptor,'_move_5')
def value():
    return ('Dragon Claw',80,100,'Physical','Dragon',0,['contact'])

@Increment(Alloraptor)
def move_5(self): # Dragon Claw
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
