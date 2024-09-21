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

    def take_damage_attack(self,x):
        self.register_act_taken()
        if self.env.get_side_condition('Mud Wall',self.side_id):
            if self['act_taken']['category']=='Special':
                x//=2
        self._set_hp(-x)        

    def move_1(self): # Mud Wave
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
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
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
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
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_boost('spe',-1)
        self.restore(self['max_hp']//8,'heal')
