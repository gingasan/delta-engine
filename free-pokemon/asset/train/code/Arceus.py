from engine import *


class Arceus(PokemonBase):
    _species='Arceus'
    _types=['Normal']
    _gender='Neutral'
    _ability=['Wonder Guard']
    _move_1=('Thousand Arrows',90,100,'Physical','Ground',0,[])
    _move_2=('Substitute',0,100000,'Status','Normal',0,[])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        if not self['act_taken'].get('type_effect',0)>1:
            return
        if self['conditions'].get('SUBSTITUTE'):
            self['conditions']['SUBSTITUTE']['hp']-=x
            if self['conditions']['SUBSTITUTE']['hp']<1:
                del self['conditions']['SUBSTITUTE']
        else:
            self.state['hp']=max(0,self['hp']-x)
            self.log(script='attack',species=self._species,x=x,**self['act_taken'])

    def move_1(self): # Thousand Arrows
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Substitute
        if self['hp']>self['max_hp']//4 and not self['conditions'].get('SUBSTITUTE'):
            self.take_damage(self['max_hp']//4,'loss')
            self.set_condition('SUBSTITUTE',hp=self['max_hp']//4)

    def get_type_effect(self):
        move_type=self['act']['type']
        target_types=self.target['types']
        effect=1
        for tt in target_types:
            if tt=='Flying' and self['act']['id']=='Thousand Arrows':
                effect*=1
            else:
                effect*=TYPEEFFECTIVENESS[move_type][tt]
        return effect

# ----------

@Increment(Arceus,'_move_3')
def value():
    return ('Toxic',0,90,'Status','Poison',0,[])

@Increment(Arceus)
def move_3(self): # Toxic
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        self.target.set_status('TOX')

# ----------

@Increment(Arceus,'_move_4')
def value():
    return ('Protect',0,100000,'Status','Normal',4,[])

@Increment(Arceus)
def move_4(self): # Protect
    if self['last_act'] and self['last_act']['id']=='Protect':
        return
    self.set_condition('PROTECT',counter=0)

@Increment(Arceus)
def _take_damage_attack(self,x):
    if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    if self['conditions'].get('PROTECT'):
        del self['conditions']['PROTECT']
        return
    self.register_act_taken()
    if not self['act_taken'].get('type_effect',0)>1:
        return
    if self['conditions'].get('SUBSTITUTE'):
        self['conditions']['SUBSTITUTE']['hp']-=x
        if self['conditions']['SUBSTITUTE']['hp']<1:
            del self['conditions']['SUBSTITUTE']
    else:
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])

@Increment(Arceus)
def endturn(self):
    if self['conditions'].get('PROTECT'):
        del self['conditions']['PROTECT']

# ----------

@Increment(Arceus,'_ability')
def value():
    return ['Wonder Guard','Corrosion']

@Increment(Arceus)
def set_status(self,x):
    if self['status'] or self.env.get('Misty Terrain'):
        return
    if x=='BRN':
        if not self.istype('Fire'):
            self.state['status']={x:{'counter':0}}
            self.log('%s is burned.'%self._species)
    elif x=='PAR':
        if not self.istype('Electric'):
            self.state['status']={x:{'counter':0}}
            self.log('%s is paralyzed.'%self._species)
    elif x=='PSN':
        self.state['status']={x:{'counter':0}}
        self.log('%s is poisoned.'%self._species)
    elif x=='TOX':
        self.state['status']={x:{'counter':0}}
        self.log('%s is badly poisoned.'%self._species)
    elif x=='FRZ':
        if not self.istype('Ice'):
            self.state['status']={x:{'counter':0}}
            self.log('%s is frozen.'%self._species)
    elif x=='SLP':
        if not self.env.get("Electric Terrain"):
            self.state['status']={x:{'counter':0}}
            self.log('%s falls asleep.'%self._species)
