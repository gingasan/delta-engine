from engine import *


class Bubblifur(PokemonBase):
    _species='Bubblifur'
    _types=['Water','Fairy']
    _gender='Female'
    _ability=['Soapy Grace']
    _move_1=('Bubble Slide',75,100,'Physical','Water',0,['contact'])
    _move_2=('Soothing Mist',0,100000,'Status','Fairy',0,[])
    def __init__(self):
        super().__init__()

    def move_1(self): # Bubble Slide
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('spe',-1)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('accuracy',-1)

    def move_2(self): # Soothing Mist
        self.restore(self['max_hp']//2,'heal')
        self.state['status']=None

# ----------

@Increment(Bubblifur,'_move_3')
def value():
    return ('Aqua Jet',40,100,'Physical','Water',1,['contact'])

@Increment(Bubblifur)
def move_3(self): # Aqua Jet
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_boost('accuracy',-1)

# ----------

@Increment(Bubblifur,'_move_4')
def value():
    return ('Pressurized Jet',110,85,'Special','Water',0,[])

@Increment(Bubblifur)
def move_4(self): # Pressurized Jet
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if rnd()<10/100:
            self.target.set_condition('Confusion',counter=0)

# ----------

@Increment(Bubblifur,'_ability')
def value():
    return ['Soapy Grace','Bubble Cloak']

@Increment(Bubblifur)
def take_damage_attack(self,x):
    self.register_act_taken()
    if 'contact' in self['act_taken']['property'] and rnd()<30/100:
        self.target.set_boost('accuracy',-1)
    if self['act_taken']['category']=='Special':
        x=int(x*0.75)
    self._set_hp(-x)    
    if self['hp']>0 and rnd()<20/100:
        self.target.set_boost('spa',-1)
