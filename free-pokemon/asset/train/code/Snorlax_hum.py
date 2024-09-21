from engine import *


class Snorlax(PokemonBase):
    _species='Snorlax'
    _types=['Normal']
    _gender='Male'
    _ability=['Thick Fat']
    _move_1=('Rest',0,1000000,'Status','Psychic',0,[])
    _move_2=('Snore',50,100,'Special','Normal',0,[])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        if self['act_taken']['type'] in ['Ice','Fire']:
            x//=2
        self._set_hp(-x)        

    def move_1(self): # Rest  
        self.state['status']=None
        self.set_status('SLP')
        self.state['hp']=self['max_hp']

    def move_2(self): # Snore
        if not isinstance(self['status'],dict) or not 'SLP' in self['status']: return
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Snorlax,'_move_3')
def value():
    return ('Body Slam',85,100,'Physical','Normal',0,['contact'])

@Increment(Snorlax)
def move_3(self): # Body Slam
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_status('PAR')

# ----------

@Increment(Snorlax,'_move_4')
def value():
    return ('Giga Impact',150,90,'Physical','Normal',0,['contact'])

@Increment(Snorlax)
def move_4(self): # Giga Impact
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
    if not self.target.isfaint():
        self.set_condition('RECHARGE',counter=0)
        self.state['canact']=False

@Increment(Snorlax)
def endturn(self):
    if self['conditions'].get('RECHARGE'):
        if self['conditions']['RECHARGE']['counter']==0:
            self['conditions']['RECHARGE']['counter']+=1
        else:
            del self['conditions']['RECHARGE']
            self.state['canact']=True

# ----------

@Increment(Snorlax,'_ability')
def value():
    return ['Thick Fat','Heavy Sleeper']

@Increment(Snorlax)
def endturn(self):
    if self['conditions'].get('RECHARGE'):
        if self['conditions']['RECHARGE']['counter']==0:
            self['conditions']['RECHARGE']['counter']+=1
        else:
            del self['conditions']['RECHARGE']
            self.state['canact']=True
    if self['status']=='SLP':
        self.restore(self['max_hp']//8,'heal')

# ----------

@Increment(Snorlax,'_move_5')
def value():
    return ('Sleep Talk',0,1000000,'Status','Normal',0,[])

@Increment(Snorlax)
def move_5(self): # Sleep Talk
    if not self.isstatus('SLP'): return
    move_id=rndc([m for m in self.get_moves() if m!='Sleep Talk'])
    self.move2fct[move_id]()
