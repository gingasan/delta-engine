from engine import *


class Graphal(PokemonBase):
    _species='Graphal'
    _types=['Dark','Dragon']
    _gender='Male'
    _ability=['Dark World']
    _move_1=('Dark Rainbow',100,100,'Special','Dark',0,[])
    _move_2=('Flash Cannon',80,100,'Special','Steel',0,[])
    _base=(100,60,80,120,120,120)
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.env.set_side_condition('Dark World',side_id=self.side_id,from_=self._species,counter=0,max_count=5)

    def get_other_mult(self):
        mult=1
        if self.isstatus('BRN') and self['act']['category']=='Physical':
            mult*=0.5
        if self.env.get_side_condition('Dark World',self.side_id) and self['act']['type']=='Dark':
            mult*=1.5
        return mult

    def get_type_effect(self):
        if self['act']['id']=='Dark Rainbow' and self.env.get_side_condition('Dark World',self.side_id):
            return 1
        move_type=self['act']['type']
        target_types=self.target['types']
        effect=1
        for tt in target_types:
            effect*=TYPEEFFECTIVENESS[move_type][tt]
        return effect

    def move_1(self): # Dark Rainbow
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('Flinch',counter=0)

    def move_2(self): # Flash Cannon
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: self.target.set_boost('spd',-1)

# ----------

@Increment(Graphal,'_move_3')
def value():
    return ('Dark Dealings',0,100000,'Status','Dark',0,[])

@Increment(Graphal)
def move_3(self): # Dark Dealings
    self.log('Graphal makes a deal with darkness.',color='blue')
    self.set_boost('atk',+2,'self')
    self.set_boost('spa',+2,'self')
    self.set_boost('spe',+2,'self')
    self.take_damage(self['max_hp']//2,'loss')

# ----------

@Increment(Graphal,'_move_4')
def value():
    return ('Dark World',0,100000,'Status','Dark',0,[])

@Increment(Graphal)
def move_4(self): # Dark World
    self.env.set_side_condition('Dark World',side_id=self.side_id,from_=self._species,counter=0,max_count=5)

# ----------

@Increment(Graphal,'_ability')
def value():
    return ['Dark World','Lord of Dark']

@Increment(Graphal)
def onswitch(self):
    self.env.set_side_condition('Dark World',side_id=self.side_id,from_=self._species,counter=0,max_count=5)
    self.set_condition('REVIVE',counter=1)

@Increment(Graphal)
def take_damage(self,x,from_='attack'):
    if from_=='attack':
        self.take_damage_attack(x)
    elif from_=='loss':
        self.take_damage_loss(x)
    elif from_=='recoil':
        self.take_damage_recoil(x)
    if self['hp']==0:
        if self['conditions'].get('REVIVE'):
            self.state['status']=None
            self.state['hp']=self['max_hp']//2
            del self['conditions']['REVIVE']
            self.log('Revive! Lord of Dark, Graphal.',color='purple')
        else:
            self._faint()

# ----------

@Increment(Graphal,'_move_5')
def value():
    return ('Dark Budokai',0,100000,'Status','Dark',0,[])

@Increment(Graphal)
def move_5(self): # Dark Budokai
    self.env.set_side_condition('Budokai',self.target.side_id,from_=self._species,counter=0,max_counter=3)

@Increment(Graphal)
def endturn(self):
    if self.env.get_side_condition('Budokai',self.target.side_id):
        if self.target['act'] and self.target['act']['category']=='Status':
            self.target.take_damage(self.target['max_hp']//3,'loss')
            self.restore(self['max_hp']//3,'heal')
            self.log('%s is punished by not making attack.'%self.target._species,color='red')

# ----------

@Increment(Graphal,'_move_6')
def value():
    return ('Oblivion Wing',80,100,'Special','Flying',0,[])

@Increment(Graphal)
def move_6(self): # Oblivion Wing
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.restore(int(3/4*damage),'drain')
