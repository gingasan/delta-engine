from engine import *


class Hippowdon(PokemonBase):
    _species='Hippowdon'
    _types=['Ground']
    _gender='Male'
    _ability=['Sand Armor']
    _move_1=('Earthquake',100,100,'Physical','Ground',0,[])
    _move_2=('Iron Head',80,100,'Physical','Steel',0,['contact'])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        self._set_hp(-x)        
        if self['hp']>0 and rnd()<25/100:
            self.set_boost('atk',1,'self')

    def move_1(self): # Earthquake
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Iron Head
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Hippowdon,'_move_3')
def value():
    return ('Sandstorm',0,100000,'Status','Rock',0,[])

@Increment(Hippowdon)
def move_3(self): # Sandstorm
    self.env.set_weather('Sandstorm',from_=self._species)

# ----------

@Increment(Hippowdon,'_ability')
def value():
    return ['Sand Armor','Earthquake Shield']

@Increment(Hippowdon)
def take_damage_attack(self,x):
    self.register_act_taken()
    if self['act_taken']['id']=='Earthquake':
        x=int(x*0.5)
        self.state['hp']=min(self['max_hp'],self['hp']+self['max_hp']//4)
    self._set_hp(-x)
    if self['hp']==0:
        return
    if rnd()<25/100:
        self.set_boost('atk',1,'self')
