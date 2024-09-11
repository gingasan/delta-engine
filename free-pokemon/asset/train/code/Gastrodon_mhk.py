from engine import *


class Gastrodon(PokemonBase):
    _species='Gastrodon'
    _types=['Water','Ground']
    _gender='Female'
    _ability=['Storm Drain']
    _move_1=('Earth Power',90,100,'Special','Ground',0,[])
    _move_2=('Surf',90,100,'Special','Water',0,[])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        if self['act_taken'] and self['act_taken']['type']=='Water':
            self.set_boost('spa',1)
            return
        self.state['hp']=max(0,self['hp']-x)
        self.log('{} loses {} HP.'.format(self._species,x),act_taken=self['act_taken'])

    def move_1(self): # Earth Power
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_boost('spd',-1)

    def move_2(self): # Surf
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Gastrodon,'_move_3')
def value():
    return ('Pain Split',0,100000,'Status','Normal',0,[])

@Increment(Gastrodon)
def move_3(self): # Pain Split
    hp=(self['hp']+self.target['hp'])//2
    self.target.state['hp']=hp
    self.state['hp']=hp

# -------------------------------------------------------------

@Increment(Gastrodon,'_move_4')
def value():
    return ('Protect',0,100000,'Status','Normal',4,[])

@Increment(Gastrodon)
def move_4(self): # Protect
    if self['last_act'] and self['last_act']['id']=='Protect':
        return
    self.set_condition('PROTECT',counter=0)

@Increment(Gastrodon)
def _take_damage_attack(self,x):
    if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    if self['conditions'].get('PROTECT'):
        del self['conditions']['PROTECT']
        return
    self.register_act_taken()
    if self['act_taken'] and self['act_taken']['type']=='Water':
        self.set_boost('spa',1)
        return
    self.state['hp']=max(0,self['hp']-x)
    if self['hp']==0:
        self.state['status']='FNT'

@Increment(Gastrodon)
def endturn(self):
    if self['conditions'].get('PROTECT'):
        del self['conditions']['PROTECT']

# -------------------------------------------------------------

@Increment(Gastrodon,'_move_5')
def value():
    return ('Ice Beam',90,100,'Special','Ice',0,[])

@Increment(Gastrodon)
def move_5(self): # Ice Beam
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_status('FRZ')
