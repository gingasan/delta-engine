from engine import *


class Kecleon(PokemonBase):
    _species='Kecleon'
    _types=['Normal']
    _gender='Neutral'
    _ability=['Color Change']
    _move_1=('Liquidation',85,100,'Physical','Water',0,['contact'])
    _move_2=('Lick',30,100,'Physical','Ghost',0,['contact'])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        self._set_hp(-x)        
        if self['hp']==0:
            return
        self.state['types']=[self['act_taken']['type']]
    
    def move_1(self): # Liquidation
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('def',-1)

    def move_2(self): # Lick
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('PAR')

# ----------

@Increment(Kecleon,'_move_3')
def value():
    return ('Dizzy Punch',70,100,'Physical','Normal',0,['contact'])

@Increment(Kecleon)
def move_3(self): # Dizzy Punch
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('Confusion',counter=0)
