from engine import *


class Zaochi(PokemonBase):
    _species='Zaochi'
    _types=['Ground','Steel']
    _gender='Male'
    _ability=['Chisel Guard']
    _move_1=('Gleaming Spear',90,95,'Physical','Steel',0,['contact'])
    _move_2=('Shield Bash',80,100,'Physical','Steel',0,['contact'])
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
        if self['act_taken'] and self['act_taken']['category']=='Physical':
            self.set_boost('def',1,'self')
    
    def move_1(self): # Gleaming Spear
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('FLINCH')
    
    def move_2(self): # Shield Bash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Zaochi,'_move_3')
def value():
    return ('Muddy Assault',100,85,'Special','Ground',0,[])

@Increment(Zaochi)
def move_3(self): # Muddy Assault
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_boost('spe',-1)

# ----------

@Increment(Zaochi,'_move_4')
def value():
    return ('Feral Roar',0,100,'Status','Ground',0,[])

@Increment(Zaochi)
def move_4(self): # Feral Roar
    self.target.set_condition('LOWER_ATTACKS',counter=0)

@Increment(Zaochi)
def endturn(self):
    if self.target['conditions'].get('LOWER_ATTACKS'):
        self.target.set_boost('atk',-1)
        self.target['conditions']['LOWER_ATTACKS']['counter']+=1
        if self.target['conditions']['LOWER_ATTACKS']['counter']==3:
           del self.target['conditions']['LOWER_ATTACKS']

# ----------

@Increment(Zaochi,'_ability')
def value():
    return ['Chisel Guard','Spear Strike']

@Increment(Zaochi)
def move_1(self): # Gleaming Spear
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint():
            if rnd()<20/100:
                self.target.set_condition('FLINCH')
            if rnd()<30/100:
                self.target.set_boost('def',-1)

@Increment(Zaochi)
def move_2(self): # Shield Bash
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_boost('def',1,'self')
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_boost('def',-1)
