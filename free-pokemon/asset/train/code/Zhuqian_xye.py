from engine import *


class Zhuqian(PokemonBase):
    _species='Zhuqian'
    _types=['Dark','Steel']
    _gender='Neutral'
    _ability=['Eclipse Guard']
    _move_1=('Thunder Lash',90,95,'Physical','Electric',0,[])
    _move_2=('Shadow Coils',70,100,'Special','Dark',0,[])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        if self['act_taken']['type']=='Dark':
            self.set_boost('def',1,'self')
        self._set_hp(-x)        

    def get_power(self):
        power=self['act']['power']
        if self['act']['id']=='Thunder Lash' and self.target.isstatus('PAR') and rnd()<30/100:
            power*=1.5
        return int(power*self.get_weather_power_mult())
    
    def endturn(self):
        if self.target['conditions'].get('TRAP'):
            self.target.take_damage(self.target['max_hp']//8,'loss')
            self.target['conditions']['TRAP']['counter']+=1
            if self.target['conditions']['TRAP']['counter']==4:
                del self.target['conditions']['TRAP']

    def move_1(self): # Thunder Lash
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.target.set_status('PAR')

    def move_2(self): # Shadow Coils
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                self.target.set_condition('TRAP',counter=0)

# ----------

@Increment(Zhuqian,'_move_3')
def value():
    return ('Steel Howl',60,100000,'Special','Steel',0,[])

@Increment(Zhuqian)
def move_3(self): # Steel Howl
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_boost('spa',1,'self')
        self.set_boost('spd',1,'self')

# ----------

@Increment(Zhuqian,'_move_4')
def value():
    return ('Coiling Guard',0,100000,'Status','Steel',0,[])

@Increment(Zhuqian)
def move_4(self): # Coiling Guard
    self.set_boost('def',2,'self')
    self.restore(self['max_hp']//4,'heal')

# ----------

@Increment(Zhuqian,'_ability')
def value():
    return ['Eclipse Guard','Thunder Roar']

@Increment(Zhuqian)
def take_damage_attack(self,x):
    self.register_act_taken()
    if self['act_taken']['type']=='Dark':
        self.set_boost('def',1,'self')
    self._set_hp(-x)
    if self['hp']==0:
        return
    if self['act_taken'] and rnd()<30/100:
        self.target.set_status('PAR')
