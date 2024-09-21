from engine import *


class Lightning(PokemonBase):
    _species='Lightning'
    _types=['Electric','Fighting']
    _gender='Male'
    _ability=['Ultra-Inductive']
    _move_1=('Lightning Punch',75,100,'Physical','Electric',1,['contact'])
    _move_2=('Drain Punch',75,100,'Physical','Fighting',0,['contact'])
    _base=(108,123,102,80,75,112)
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        if self['conditions'].get('INDUCTIVE'):
            if self['act_taken']['category']=='Special':
                x=int(x*0.5)
        self._set_hp(-x)
        if 'contact' in self['act_taken']['property'] and rnd()<0.3:
            self.target.set_condition('INDUCTIVE',counter=0)

    def move_1(self): # Lightning Punch
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            if self.target['conditions'].get('INDUCTIVE'):
                damage*=2
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<0.3:
                self.target.set_status('PAR')

    def move_2(self): # Drain Punch
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.restore(int(1/2*damage),'drain')

# ----------

@Increment(Lightning,'_move_3')
def value():
    return ('Super Electro Bombardment',0,100000,'Status','Electric',0,[])

@Increment(Lightning)
def move_3(self): # Super Electro Bombardment
    self.target.set_condition('INDUCTIVE',counter=0)
    self.set_condition('INDUCTIVE',counter=0)
    self.set_condition('ELECTRO_SHIELD',counter=0)

@Increment(Lightning)
def take_damage_attack(self,x):
    self.register_act_taken()
    if self['conditions'].get('INDUCTIVE'):
        if self['act_taken']['category']=='Special':
            x=int(x*0.5)
    if self['conditions'].get('ELECTRO_SHIELD'):
        x=int(x*0.5)
        del self['conditions']['ELECTRO_SHIELD']
        self.log("The electro shield mitigates the attack.", color="yellow")
    self._set_hp(-x)
    if 'contact' in self['act_taken']['property'] and rnd()<0.3:
        self.target.set_condition('INDUCTIVE',counter=0)

# ----------

@Increment(Lightning,'_move_4')
def value():
    return ('Meteor Mash',90,90,'Physical','Steel',0,['contact'])

@Increment(Lightning)
def move_4(self): # Meteor Mash
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if rnd()<20/100:
            self.set_boost('atk',1,'self')

# ----------

@Increment(Lightning,'_ability')
def value():
    return ['Ultra-Inductive','Ultra-Recharge']

@Increment(Lightning)
def get_power(self):
    power=self['act']['power']
    if self['act']['id']=='Lightning Punch':
        power+=20*self['boosts']['spe']
        self.log("Lightning is recharging!", color="blue")
    return int(power*self.get_weather_power_mult())

# ----------

@Increment(Lightning,'_move_5')
def value():
    return ('Electro Boost',0,100000,'Status','Electric',0,[])

@Increment(Lightning)
def move_5(self): # Electro Boost
    if self.state['conditions'].get('INDUCTIVE'):
        self.state['conditions'].pop('INDUCTIVE')
        self.set_boost('spe',+2,'self')
