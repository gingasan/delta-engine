from engine import *


class Garchomp(PokemonBase):
    _species='Garchomp'
    _types=['Dragon','Ground']
    _gender='Female'
    _ability=['Rough Skin']
    _move_1=('Sand Tomb',35,85,'Physical','Ground',0,[])
    _move_2=('Dragon Claw',80,100,'Physical','Dragon',0,['contact'])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        self._set_hp(-x)        
        if self['act_taken'] and 'property' in self['act_taken'] and 'contact' in self['act_taken']['property']:
            self.target.take_damage(self.target['max_hp']//8,'loss')

    def endturn(self):
        if self.target['conditions'].get('TRAP'):
            if self.target['conditions']['TRAP']['counter']<5:
                self.target.take_damage(self.target['max_hp']//8,'loss')
                self.target['conditions']['TRAP']['counter']+=1
            else:
                del self.target['conditions']['TRAP']

    def move_1(self): # Sand Tomb
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('TRAP',counter=0)
    
    def move_2(self): # Dragon Claw
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Garchomp,'_move_3')
def value():
    return ('Protect',0,100000,'Status','Normal',4,[])

@Increment(Garchomp)
def get_immune(self):
    if self['conditions'].get('Protected'):
        del self['conditions']['Protected']
        return True
    return False

@Increment(Garchomp)
def take_damage_attack(self,x):
    self.register_act_taken()
    self._set_hp(-x)    
    if self['act_taken'] and 'property' in self['act_taken'] and 'contact' in self['act_taken']['property']:
        self.target.take_damage(self.target['max_hp']//8,'loss')

@Increment(Garchomp)
def endturn(self):
    if self.target['conditions'].get('TRAP'):
        if self.target['conditions']['TRAP']['counter']<5:
            self.target.take_damage(self.target['max_hp']//8,'loss')
            self.target['conditions']['TRAP']['counter']+=1
        else:
            del self.target['conditions']['TRAP']
    if self['conditions'].get('Protected'):
        del self['conditions']['Protected']

@Increment(Garchomp)
def move_3(self): # Protect
    if self['last_act'] and self['last_act']['id']=='Protect':
        return
    self.set_condition('Protected',counter=0)
