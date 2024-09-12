from engine import *


class Graphal(PokemonBase):
    _species='Graphal'
    _types=['Dark','Dragon']
    _gender='Male'
    _ability=['Dark World']
    _move_1=('Dark Rainbow',100,100,'Special','Dark',0,[])
    _move_2=('Dragon Pulse',85,100,'Special','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_env('DARK_WORLD',side='self',counter=0,max_count=5)

    def get_other_mult(self):
        mult=1
        if self.isstatus('BRN') and self['act']['category']=='Physical':
            mult*=0.5
        if self.get_env('DARK_WORLD',side='self'):
            mult=mult*1.5 if self['act']['type']=='Dark' else mult*0.75
        return mult

    def get_type_effect(self):
        if self['act']['id']=='Dark Rainbow' and self.get_env('DARK_WORLD',side='self'):
            return 1
        move_type=self['act']['type']
        target_types=self.target['types']
        effect=1
        for tt in target_types:
            effect*=TYPEEFFECTIVENESS[move_type][tt]
        return effect

    def move_1(self): # Dark Rainbow
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('FLINCH',counter=0)

    def move_2(self): # Dragon Pulse
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Graphal,'_move_3')
def value():
    return ('Dark Dealings',0,100000,'Status','Dark',0,[])

@Increment(Graphal)
def move_3(self): # Dark Dealings
    self.log("Graphal makes a deal with the dark world.", color="grey")
    self.set_boost('atk',+2,'self')
    self.set_boost('spa',+2,'self')
    self.set_boost('spe',+2,'self')
    self.take_damage(self['max_hp']//2,'loss')

# ----------

@Increment(Graphal,'_move_4')
def value():
    return ('Flash Cannon',80,100,'Special','Steel',0,[])

@Increment(Graphal)
def move_4(self): # Flash Cannon
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100: self.target.set_boost('spd',-1)

# ----------

@Increment(Graphal,'_ability')
def value():
    return ['Dark World','Lord of Dark']

@Increment(Graphal)
def onswitch(self):
    self.set_env('DARK_WORLD',side='self',counter=0,max_count=5)
    self.set_condition('REVIVE',counter=1)

@Increment(Graphal)
def take_damage(self,x,from_='attack'):
    if from_=='attack':
        self._take_damage_attack(x)
    elif from_=='loss':
        self._take_damage_loss(x)
    elif from_=='recoil':
        self._take_damage_recoil(x)
    if self['hp']==0:
        if self['conditions'].get('REVIVE'):
            self.state['status']=None
            self.state['hp']=self['max_hp']//2
            del self['conditions']['REVIVE']
            self.log('Revive! Lord of Dark, Graphal.',color='purple')
        else:
            self.state['status']='FNT'
            self.log('%s faints.'%self._species)

# ----------

@Increment(Graphal,'_move_5')
def value():
    return ('Dark World',0,100000,'Status','Dark',0,[])

@Increment(Graphal)
def move_5(self): # Dark World
    self.set_env('DARK_WORLD',side='self',counter=0,max_count=5)
