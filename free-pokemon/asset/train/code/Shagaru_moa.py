from engine import *


class Shagaru(PokemonBase):
    _species='Shagaru'
    _types=['Dragon']
    _gender='Neutral'
    _ability=['Frenzy Overload']
    _move_1=('Frenzy Beam',90,100,'Special','Dragon',0,[])
    _move_2=('Virus Eruption',100,90,'Special','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        if self['act_taken']['type'] in ['Dragon','Fairy']:
            return
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])

    def endturn(self):
        if self.target['conditions'].get('FRENZY'):
            self.target.set_boost('def',-1)
            self.target['conditions']['FRENZY']['counter']+=1
            if self.target['conditions']['FRENZY']['counter']==self.target['conditions']['FRENZY']['max_count']:
                del self.target['conditions']['FRENZY']

    def move_1(self): # Frenzy Beam
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('FRENZY',counter=0,max_count=3)

    def move_2(self): # Virus Eruption
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_status('TOX')

# ----------

@Increment(Shagaru,'_move_3')
def value():
    return ('Shadow Pummel',80,100,'Physical','Dark',0,[])

@Increment(Shagaru)
def move_3(self): # Shadow Pummel
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if rnd()<20/100:
            self.target.set_condition('CONFUSION',counter=0)

# ----------

@Increment(Shagaru,'_ability')
def value():
    return ['Frenzy Overload','Virus Mastery']

@Increment(Shagaru)
def move_1(self): # Frenzy Beam
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint():
            self.target.set_condition('FRENZY',counter=0,max_count=3)

@Increment(Shagaru)
def move_2(self): # Virus Eruption
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint():
            self.target.set_status('TOX')
