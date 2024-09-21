from engine import *


class Arceus(PokemonBase):
    _species='Arceus'
    _types=['Normal']
    _gender='Neutral'
    _ability=['Wonder Guard']
    _move_1=('Thousand Arrows',90,100,'Physical','Ground',0,[])
    _move_2=('Substitute',0,100000,'Status','Normal',0,[])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        if not self['act_taken'].get('type_effect',0)>1:
            return
        if self['conditions'].get('SUBSTITUTE'):
            self['conditions']['SUBSTITUTE']['hp']-=x
            if self['conditions']['SUBSTITUTE']['hp']<1:
                del self['conditions']['SUBSTITUTE']
        else:
            self._set_hp(-x)            

    def move_1(self): # Thousand Arrows
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Substitute
        if self['hp']>self['max_hp']//4 and not self['conditions'].get('SUBSTITUTE'):
            self.take_damage(self['max_hp']//4,'loss')
            self.set_condition('SUBSTITUTE',hp=self['max_hp']//4)

    def get_type_effect(self):
        move_type=self['act']['type']
        target_types=self.target['types']
        effect=1
        for tt in target_types:
            if tt=='Flying' and self['act']['id']=='Thousand Arrows':
                effect*=1
            else:
                effect*=TYPEEFFECTIVENESS[move_type][tt]
        return effect

# ----------

@Increment(Arceus,'_move_3')
def value():
    return ('Toxic',0,90,'Status','Poison',0,[])

@Increment(Arceus)
def move_3(self): # Toxic
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        self.target.set_status('TOX')

# ----------

@Increment(Arceus,'_move_4')
def value():
    return ('Protect',0,100000,'Status','Normal',4,[])

@Increment(Arceus)
def move_4(self): # Protect
    if self['last_act'] and self['last_act']['id']=='Protect':
        return
    self.set_condition('Protected',counter=0)

@Increment(Arceus)
def get_immune(self):
    if self['conditions'].get('Protected'):
        del self['conditions']['Protected']
        return True
    return False

@Increment(Arceus)
def take_damage_attack(self,x):
    self.register_act_taken()
    if not self['act_taken'].get('type_effect',0)>1:
        return
    if self['conditions'].get('SUBSTITUTE'):
        self['conditions']['SUBSTITUTE']['hp']-=x
        if self['conditions']['SUBSTITUTE']['hp']<1:
            del self['conditions']['SUBSTITUTE']
    else:
        self._set_hp(-x)        

@Increment(Arceus)
def endturn(self):
    if self['conditions'].get('Protected'):
        del self['conditions']['Protected']

# ----------

@Increment(Arceus,'_ability')
def value():
    return ['Wonder Guard','Corrosion']

@Increment(Arceus)
def set_status(self,x):
    if self['status'] or self.env.get('Misty Terrain'):
        return
    if x=='BRN':
        if self.istype('Fire'):
            return
    elif x=='PAR':
        if self.istype('Electric'):
            return
    elif x=='FRZ':
        if self.istype('Ice'):
            return
    elif x=='SLP':
        if self.env.get("Electric Terrain"):
            return
    self._set_status(x)
