from engine import *


class Dragorion(PokemonBase):
    _species='Dragorion'
    _types=['Fire','Dragon']
    _gender='Male'
    _ability=['End Phase Fury']
    _move_1=('Inferno Claw',85,90,'Physical','Fire',0,['contact'])
    _move_2=('Dragon Breath',60,100,'Special','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def endturn(self):
        if self['act'] and self['act']['category']=='Status':
            self.target.take_damage(self['max_hp']//8,'loss')

    def move_1(self):
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_status('BRN')

    def move_2(self):
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('PAR')

# ----------

@Increment(Dragorion,'_move_3')
def value():
    return ('Fiery Roar',0,100,'Status','Fire',0,[])

@Increment(Dragorion)
def move_3(self):
    self.target.set_boost('atk',-1)
    if not self.target.isfaint() and rnd()<50/100:
        self.target.set_status('BRN')

# ----------

@Increment(Dragorion,'_move_4')
def value():
    return ('Heat Wave',95,90,'Special','Fire',0,[])

@Increment(Dragorion)
def move_4(self):
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_status('BRN')

# ----------

@Increment(Dragorion,'_ability')
def value():
    return ['End Phase Fury','Flame Shield']

@Increment(Dragorion)
def _take_damage_attack(self,x):
    if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    self.register_act_taken()
    self.state['hp']=max(0,self['hp']-x)
    self.log(script='attack',species=self._species,x=x,**self['act_taken'])
    if 'property' in self['act_taken'] and 'contact' in self['act_taken']['property']:
        if rnd()<30/100:
            self.target.set_status('BRN')

# ----------

@Increment(Dragorion,'_move_5')
def value():
    return ('Dragon Claw',80,100,'Physical','Dragon',0,['contact'])

@Increment(Dragorion)
def move_5(self):
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
