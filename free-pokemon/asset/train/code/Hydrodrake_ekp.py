from engine import *


class Hydrodrake(PokemonBase):
    _species='Hydrodrake'
    _types=['Water','Poison']
    _gender='Neutral'
    _ability=['Regenerative Scales']
    _move_1=('Hydra Surge',100,90,'Special','Water',0,[])
    _move_2=('Venomous Strike',80,100,'Physical','Poison',0,[])
    def __init__(self):
        super().__init__()

    def endturn(self):
        if self['act_taken'] and self['act_taken'].get('damage'):
            self.restore(self['max_hp']//8,'heal')

    def move_1(self): # Hydra Surge
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            if self.target['conditions'].get('Confusion'):
                damage=int(damage*1.5)
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('Confusion',counter=0)

    def move_2(self): # Venomous Strike
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            if self.target.isstatus('PSN') or self.target.isstatus('TOX'):
                damage=int(damage*2)
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<40/100:
                self.target.set_status('PSN')

# ----------

@Increment(Hydrodrake,'_move_3')
def value():
    return ('Head Rebirth',0,100000,'Status','Water',0,[])

@Increment(Hydrodrake)
def move_3(self): # Head Rebirth
    if self['hp']<self['max_hp']:
        self.restore(self['max_hp']//4,'heal')
        self.set_boost('def',+1,'self')

# ----------

@Increment(Hydrodrake,'_move_4')
def value():
    return ('Serpents Wrath',90,85,'Physical','Water',0,[])

@Increment(Hydrodrake)
def move_4(self): # Serpent's Wrath
    self.set_condition('IGNORE_ATTACKS',counter=0)

@Increment(Hydrodrake)
def _take_damage_attack(self,x):
    if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    if self['conditions'].get('IGNORE_ATTACKS'):
        return
    self.register_act_taken()
    self.state['hp']=max(0,self['hp']-x)
    self.log(script='attack',species=self._species,x=x,**self['act_taken'])

@Increment(Hydrodrake)
def endturn(self):
    if self['act_taken'] and self['act_taken'].get('damage'):
        self.restore(self['max_hp']//8,'heal')
    if self['conditions'].get('IGNORE_ATTACKS'):
       self['conditions']['IGNORE_ATTACKS']['counter']+=1
       if self['conditions']['IGNORE_ATTACKS']['counter']==2:
           del self['conditions']['IGNORE_ATTACKS']

# ----------

@Increment(Hydrodrake,'_ability')
def value():
    return ['Regenerative Scales','Toxic Resilience']

@Increment(Hydrodrake)
def _take_damage_attack(self,x):
    if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    if self['conditions'].get('IGNORE_ATTACKS'):
        return
    self.register_act_taken()
    if self['act_taken']['type']=='Poison':
        x=int(x*0.5)
    self.state['hp']=max(0,self['hp']-x)
    if self['hp']==0:
        self.state['status']='FNT'
