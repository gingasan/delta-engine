from engine import *


class Rhyperior(PokemonBase):
    _species='Rhyperior'
    _types=['Ground','Rock']
    _gender='Female'
    _ability=['Solid Fortification']
    _move_1=('Quake Impact',100,100,'Physical','Ground',0,[])
    _move_2=('Protect',0,100000,'Status','Normal',4,[])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        if self['act_taken']['type_effect']>1:
            x=int(x*0.7)
        self._set_hp(-x)        

    def move_1(self): # Quake Impact
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('def',-1)

    def move_2(self): # Protect
        if self['last_act'] and self['last_act']['id']=='Protect':
            return
        self.set_condition('Protected',counter=0)

    def get_immune(self):
        if self['conditions'].get('Protected'):
            del self['conditions']['Protected']
            return True
        return False

# ----------

@Increment(Rhyperior,'_move_3')
def value():
    return ('Rock Blast',25,90,'Physical','Rock',0,['contact'])

@Increment(Rhyperior)
def move_3(self): # Rock Blast
    hit=True; i=0
    r=rnd()
    if r<0.35:
        n_hits=2
    elif r<0.7:
        n_hits=3
    elif r<0.85:
        n_hits=4
    else:
        n_hits=5
    while hit and i<n_hits:
        attack_ret=self.attack()
        if attack_ret['miss'] or attack_ret['immune']: break
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        i+=1; hit=False if self.target.isfaint() else True

# ----------

@Increment(Rhyperior,'_move_4')
def value():
    return ('Earthen Barrier',0,100000,'Status','Ground',0,[])

@Increment(Rhyperior)
def move_4(self): # Earthen Barrier
    self.set_boost('def',+1,'self')
    self.set_boost('spd',+1,'self')

# ----------

@Increment(Rhyperior,'_ability')
def value():
    return ['Solid Fortification','Stone Resolve']

@Increment(Rhyperior)
def endturn(self):
    if self.env.get('Sandstorm'):
        self.set_boost('spd',1,'self')
    if self['conditions'].get('Protected'):
        del self['conditions']['Protected']

# ----------

@Increment(Rhyperior,'_move_5')
def value():
    return ('Ice Punch',75,100,'Physical','Ice',0,['contact'])

@Increment(Rhyperior)
def move_5(self): # Ice Punch
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_status('FRZ')
