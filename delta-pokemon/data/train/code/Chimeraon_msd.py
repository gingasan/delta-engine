from engine import *


class Chimeraon(PokemonBase):
    _species='Chimeraon'
    _types=['Fire','Dragon']
    _gender='Neutral'
    _ability=['Fiery Roar']
    _move_1=('Blazing Breath',100,90,'Special','Fire',0,[])
    _move_2=('Dragon Fang',85,95,'Physical','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def get_type_effect(self):
        move_type=self['act']['type']
        target_types=self.target['types']
        effect=1
        for tt in target_types:
            if move_type=='Fire' and tt=='Water':
                effect*=2
            else:
                effect*=TYPEEFFECTIVENESS[move_type][tt]
        return effect

    def get_power(self):
        power=self['act']['power']
        if self['act']['type']=='Fire':
            power*=1.5
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Blazing Breath
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<0.3:
                self.target.set_status('BRN')

    def move_2(self): # Dragon Fang
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<0.2:
                self.target.set_boost('def',-1)

# -------------------------------------------------------------

@Increment(Chimeraon,'_move_3')
def value():
    return ('Goat Rush',90,100,'Physical','Normal',0,[])

@Increment(Chimeraon)
def move_3(self): # Goat Rush
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_boost('spe',+1,'self')

# -------------------------------------------------------------

@Increment(Chimeraon,'_move_4')
def value():
    return ('Serpent Venom',70,100,'Special','Poison',0,[])

@Increment(Chimeraon)
def move_4(self): # Serpent Venom
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint():
            if self.target.isstatus('PSN'):
                damage*=2
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<0.5:
                self.target.set_status('PSN')

# -------------------------------------------------------------

@Increment(Chimeraon,'_ability')
def value():
    return ['Fiery Roar','Venomous Strike']

@Increment(Chimeraon)
def _take_damage_attack(self,x):
    self.register_act_taken()
    self.state['hp']=max(0,self['hp']-x)
    if self['act_taken'] and 'contact' in self['act_taken']['property']:
        if rnd()<0.3:
            self.target.set_status('PSN')
    if self['hp']==0:
        self.state['status']='FNT'
