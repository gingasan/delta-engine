from engine import *


class Huashe(PokemonBase):
    _species='Huashe'
    _types=['Ghost','Flying']
    _gender='Neutral'
    _ability=['Wailing Echo']
    _move_1=('Phantom Cry',85,90,'Special','Ghost',0,[])
    _move_2=('Flood Surge',100,95,'Special','Water',0,[])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        if self['act_taken']['category']=='Special' and rnd()<30/100:
            self.target.set_boost('spa',-1)
        self._set_hp(-x)        

    def move_1(self): # Phantom Cry
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('Confusion',counter=0)
    
    def move_2(self): # Flood Surge
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('spe',-1)

# ----------

@Increment(Huashe,'_move_3')
def value():
    return ('Spectral Glide',0,100000,'Status','Flying',0,[])

@Increment(Huashe)
def move_3(self): # Spectral Glide
    self.set_condition('GHOST_IMMUNE',counter=0)

@Increment(Huashe)
def take_damage_attack(self,x):
    self.register_act_taken()
    if self['conditions'].get('GHOST_IMMUNE') and self['act_taken']['type']=='Ghost':
        return
    if self['act_taken']['category']=='Special' and rnd()<30/100:
        self.target.set_boost('spa',-1)
    self._set_hp(-x)    

@Increment(Huashe)
def endturn(self):
    if self['conditions'].get('GHOST_IMMUNE'):
        self['conditions']['GHOST_IMMUNE']['counter']+=1
        if self['conditions']['GHOST_IMMUNE']['counter']==3:
            del self['conditions']['GHOST_IMMUNE']

# ----------

@Increment(Huashe,'_move_4')
def value():
    return ('Serpent Strike',90,100,'Physical','Ghost',0,['contact'])

@Increment(Huashe)
def move_4(self): # Serpent Strike
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Huashe,'_ability')
def value():
    return ['Wailing Echo','Flood Herald']

@Increment(Huashe)
def endturn(self):
    if self.env.get('Rain'):
        self.set_boost('spd',1,'self')
        self.target.set_boost('accuracy',-1)
    if self['conditions'].get('GHOST_IMMUNE'):
        self['conditions']['GHOST_IMMUNE']['counter']+=1
        if self['conditions']['GHOST_IMMUNE']['counter']==3:
            del self['conditions']['GHOST_IMMUNE']
