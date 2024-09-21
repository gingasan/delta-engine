from engine import *


class Taotaur(PokemonBase):
    _species='Taotaur'
    _types=['Dark','Normal']
    _gender='Neutral'
    _ability=['Insatiable Hunger']
    _move_1=('Devouring Bite',90,100,'Physical','Dark',0,[])
    _move_2=('Ancient Power',60,100,'Special','Rock',0,[])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        self._set_hp(-x)        
        if self['hp']==0:
            return
        self.set_boost('atk',+1,'self')
        self.set_boost('spa',+1,'self')

    def move_1(self): # Devouring Bite
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('Flinch',counter=0)
    
    def move_2(self): # Ancient Power
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_status('SLP')

# ----------

@Increment(Taotaur,'_move_3')
def value():
    return ('Ritual Stomp',80,95,'Physical','Normal',0,[])

@Increment(Taotaur)
def move_3(self): # Ritual Stomp
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.target.set_boost('def',-1)

# ----------

@Increment(Taotaur,'_move_4')
def value():
    return ('Gluttonous Maw',0,100000,'Status','Dark',0,[])

@Increment(Taotaur)
def move_4(self): # Gluttonous Maw
    self.restore(self['max_hp']//2,'heal')
    self.set_boost('atk',+1,'self')

# ----------

@Increment(Taotaur,'_ability')
def value():
    return ['Insatiable Hunger','Intimidating Gaze']

@Increment(Taotaur)
def onswitch(self):
    self.target.set_boost('atk',-1)
