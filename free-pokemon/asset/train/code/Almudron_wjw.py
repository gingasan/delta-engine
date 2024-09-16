from engine import *


class Almudron(PokemonBase):
    _species='Almudron'
    _types=['Ground','Water']
    _gender='Female'
    _ability=['Muddy Secretion']
    _move_1=('Mud Wave',85,100,'Special','Ground',0,[])
    _move_2=('Mud Wall',0,100000,'Status','Ground',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.target.set_stat('spe',0.7)

    def _take_damage_attack(self,x):
        if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        if self.env.get_side_condition('Mud Wall',self.side_id):
            if self['act_taken']['category']=='Special':
                x//=2
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])

    def move_1(self): # Mud Wave
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('spe',-1)

    def move_2(self): # Mud Wall
        self.env.set_side_condition('Mud Wall',self.side_id,from_=self._species,counter=0,max_count=5)

# ----------

@Increment(Almudron,'_move_3')
def value():
    return ('Golden Mire',90,100,'Special','Water',0,[])

@Increment(Almudron)
def move_3(self): # Golden Mire
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('TRAP',counter=0,max_count=rndc([2,3,4,5]))

@Increment(Almudron)
def endturn(self):
    if self.target['conditions'].get('TRAP'):
        self.target.take_damage(self.target['max_hp']//16,'loss')
        self.target['conditions']['TRAP']['counter']+=1
        if self.target['conditions']['TRAP']['counter']==self.target['conditions']['TRAP']['max_count']:
            del self.target['conditions']['TRAP']

# ----------

@Increment(Almudron,'_ability')
def value():
    return ['Muddy Secretion','Soil Absorption']

@Increment(Almudron)
def move_1(self): # Mud Wave
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_boost('spe',-1)
        self.restore(self['max_hp']//8,'heal')
