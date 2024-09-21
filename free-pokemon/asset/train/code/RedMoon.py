from engine import *


class RedMoon(PokemonBase):
    _species='Red-Moon'
    _types=['Dragon','Flying']
    _gender='Male'
    _ability=['Intimidate']
    _move_1=('Red Dragon',110,90,'Physical','Dragon',0,['contact'])
    _move_2=('Brave Bird',120,100,'Physical','Flying',0,['contact'])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.target.set_boost('atk',-1)
    
    def move_1(self): # Red Dragon
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100: self.target.set_status('BRN')
    
    def move_2(self): # Brave Bird
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if damage>0:
                self.take_damage(int(0.33*damage),'recoil')

# ----------

@Increment(RedMoon,'_move_3')
def value():
    return ('Dragon Dance',0,100000,'Status','Dragon',0,[])

@Increment(RedMoon)
def move_3(self): # Dragon Dance
    self.set_boost('atk',+1,'self')
    self.set_boost('spe',+1,'self')

# ----------

@Increment(RedMoon,'_move_4')
def value():
    return ('Iron Head',80,100,'Physical','Steel',0,['contact'])

@Increment(RedMoon)
def move_4(self): # Iron Head
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(RedMoon,'_ability')
def value():
    return ['Intimidate','Red-Moon Defense']

@Increment(RedMoon)
def take_damage_attack(self,x):
    self.register_act_taken()
    self._set_hp(-x)    
    if self['hp']>0 and self['act_taken']:
        self.target.take_damage(self.target['max_hp']//8 if self.target.isstatus('BRN') else self.target['max_hp']//16,'loss')

# ----------

@Increment(RedMoon,'_move_5')
def value():
    return ('Roost',0,100000,'Status','Flying',0,[])

@Increment(RedMoon)
def move_5(self): # Roost
    self.restore(self['max_hp']//2,'heal')
