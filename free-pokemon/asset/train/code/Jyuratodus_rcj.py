from engine import *


class Jyuratodus(PokemonBase):
    _species='Jyuratodus'
    _types=['Water','Ground']
    _gender='Neutral'
    _ability=['Mud Armor']
    _move_1=('Sludge Spit',70,95,'Special','Water',0,[])
    _move_2=('Mud Roll',80,100,'Physical','Ground',0,[])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        if self['act_taken']['category']=='Physical' and self['hp']<self['max_hp']//2:
            x=int(x*0.5)
        self._set_hp(-x)        

    def endturn(self):
        if self.target['conditions'].get('TRAP'):
            self.target.take_damage(self.target['max_hp']//8,'loss')
            self.target['conditions']['TRAP']['counter']+=1
            if self.target['conditions']['TRAP']['counter']==self.target['conditions']['TRAP']['max_count']:
                del self.target['conditions']['TRAP']

    def move_1(self): # Sludge Spit
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                self.target.set_condition('TRAP',counter=0,max_count=5)
    
    def move_2(self): # Mud Roll
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('def',+1,'self')

# ----------

@Increment(Jyuratodus,'_move_3')
def value():
    return ('Swamp Wave',0,100000,'Status','Water',0,[])

@Increment(Jyuratodus)
def move_3(self): # Swamp Wave
    for t in [self,self.target]:
        if not t.istype('Ground'):
            t.set_boost('spe',-2)
        if t.istype('Water'):
            t.restore(t['max_hp']//4,'heal')

# ----------

@Increment(Jyuratodus,'_ability')
def value():
    return ['Mud Armor','Sludge Trap']

@Increment(Jyuratodus)
def take_damage_attack(self,x):
    self.register_act_taken()
    if self['act_taken']['category']=='Physical' and self['hp']<self['max_hp']//2:
        x=int(x*0.5)
    self._set_hp(-x)
    if self['hp']==0:
        self._faint()
        return
    if self['act_taken']['type']=='Water':
        self.target.set_boost('spe',-1)
