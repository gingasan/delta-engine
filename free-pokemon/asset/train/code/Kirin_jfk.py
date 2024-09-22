from engine import *


class Kirin(PokemonBase):
    _species='Kirin'
    _types=['Electric','Fairy']
    _gender='Male'
    _ability=['Electric Surge']
    _move_1=('Thunder',110,70,'Special','Electric',0,[])
    _move_2=('Parabolic Charge',65,100,'Special','Electric',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.env.set_terrain('Electric Terrain',from_=self._species)

    def move_1(self): # Thunder
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100: self.target.set_status('PAR')
    
    def move_2(self): # Parabolic Charge
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.restore(int(1/2*damage),'drain')

# ----------

@Increment(Kirin,'_move_3')
def value():
    return ('Deflecting Aura',0,100000,'Status','Fairy',0,[])

@Increment(Kirin)
def move_3(self): # Deflecting Aura
    self.env.set_side_condition('Deflecting Aura',self.side_id,from_=self._species,counter=0)

@Increment(Kirin)
def endturn(self):
    if self.env.get_side_condition('Deflecting Aura',self.side_id):
        self.set_boost('def',1,'self')
        self.set_boost('spd',1,'self')

# ----------

@Increment(Kirin,'_move_4')
def value():
    return ('Raging Horn',100,95,'Special','Fairy',0,[])

@Increment(Kirin)
def move_4(self): # Draco Meteor
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_boost('spa',-2,'self')

# ----------

@Increment(Kirin,'_ability')
def value():
    return ['Electric Surge','Thunderous Rage']

@Increment(Kirin)
def get_accuracy(self):
    if self['conditions'].get('THUNDEROUS_RAGE'):
        return 100000
    acc=self['act']['accuracy']
    if self['act']['id']=='Thunder':
        if self.env.get('Rain'):
            acc=1e5
        elif self.env.get('Sunlight'):
            acc=50
    acc_mult=[1.0,1.33,1.67,2.0]
    if self['boosts']['accuracy']>=0:
        acc*=acc_mult[self['boosts']['accuracy']]
    else:
        acc/=acc_mult[self['boosts']['accuracy']]
    acc*=(1-self.target.get_evasion())
    return acc/100

# ----------

@Increment(Kirin,'_move_5')
def value():
    return ('Draco Meteor',130,90,'Special','Dragon',0,[])

@Increment(Kirin)
def move_5(self): # Raging Horn
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)

@Increment(Kirin)
def get_crit(self):
    if self['act']['id']=='Raging Horn' and self['conditions'].get('THUNDEROUS_RAGE'):
        return True
    crit_mult=[0,24,8,2,1]
    crit_ratio=self['boosts']['crit']
    crit=False
    if rnd()*crit_mult[crit_ratio+1]<1:
        crit=True
    return crit
