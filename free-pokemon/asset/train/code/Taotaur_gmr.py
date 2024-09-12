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

    def _take_damage_attack(self,x):
        if 'type_efc' in self.target['act'] and self.target['act']['type_efc']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])
        if self['hp']==0:
            return
        self.set_boost('atk',+1,'self')
        self.set_boost('spa',+1,'self')

    def move_1(self): # Devouring Bite
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('FLINCH',counter=0)
    
    def move_2(self): # Ancient Power
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
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
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
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
