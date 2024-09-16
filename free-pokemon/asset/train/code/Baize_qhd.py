from engine import *


class Baize(PokemonBase):
    _species='Baize'
    _types=['Dragon','Fairy']
    _gender='Genderless'
    _ability=['Divine Insight']
    _move_1=('Dragon Pulse',85,100,'Special','Dragon',0,[])
    _move_2=('Mystic Shield',0,100000,'Status','Fairy',0,[])
    def __init__(self):
        super().__init__()

    def get_accuracy(self):
        acc=1e5
        acc*=self.target.get_evasion()
        return acc/100

    def move_1(self): # Dragon Pulse
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Mystic Shield
        self.set_boost('def',1,'self')
        self.set_boost('spd',1,'self')
        self.target.set_boost('atk',-1)

# ----------

@Increment(Baize,'_move_3')
def value():
    return ('Celestial Voice',70,100,'Special','Normal',0,[])

@Increment(Baize)
def move_3(self): # Celestial Voice
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('CONFUSION',counter=0)

# ----------

@Increment(Baize,'_ability')
def value():
    return ['Divine Insight','Purifying Presence']

@Increment(Baize)
def onswitch(self):
    self.set_condition('PURE_ZONE',counter=0)

@Increment(Baize)
def _take_damage_attack(self,x):
    if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
        self.logger.log('It is immune by %s.'%self._species)
        return
    if self['conditions'].get('PURE_ZONE'):
        return
    self.register_act_taken()
    self.state['hp']=max(0,self['hp']-x)
    self.log(script='attack',species=self._species,x=x,**self['act_taken'])

@Increment(Baize)
def endturn(self):
    if self['conditions'].get('PURE_ZONE'):
        self['conditions']['PURE_ZONE']['counter']+=1
        if self['conditions']['PURE_ZONE']['counter']==3:
            del self['conditions']['PURE_ZONE']
