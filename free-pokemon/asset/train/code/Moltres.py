from engine import *


class Moltres(PokemonBase):
    _species='Moltres'
    _types=['Dark','Flying']
    _gender='Neutral'
    _ability=['Berserk']
    _move_1=('Fiery Wrath',90,100,'Special','Dark',0,[])
    _move_2=('Nasty Plot',0,100000,'Status','Dark',0,[])
    def __init__(self):
        super().__init__()

    def take_damage(self,x,from_='attack'):
        prev_hp=self['hp']
        if from_=='attack':
            self._take_damage_attack(x)
        elif from_=='loss':
            self.take_damage_loss(x)
        elif from_=='recoil':
            self.take_damage_recoil(x)
        if self['hp']==0:
            self._faint()
            return
        if prev_hp>self['max_hp']//2 and self['hp']<=self['max_hp']//2:
            self.set_boost('spa',1,'self')

    def move_1(self): # Fiery Wrath
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('Flinch',counter=0)

    def move_2(self): # Nasty Plot
        self.set_boost('spa',+2,'self')

# ----------

@Increment(Moltres,'_move_3')
def value():
    return ('Air Slash',75,95,'Special','Flying',0,[])

@Increment(Moltres)
def move_3(self): # Air Slash
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Moltres,'_move_4')
def value():
    return ('Protect',0,100000,'Status','Normal',4,[])

@Increment(Moltres)
def move_4(self): # Protect
    if self['last_act'] and self['last_act']['id']=='Protect':
        return
    self.set_condition('Protected',counter=0)

@Increment(Moltres)
def get_immune(self):
    if self['conditions'].get('Protected'):
        del self['conditions']['Protected']
        return True
    return False

@Increment(Moltres)
def endturn(self):
    if self['conditions'].get('Protected'):
        del self['conditions']['Protected']

# ----------

@Increment(Moltres,'_ability')
def value():
    return ['Berserk','Competitive']

@Increment(Moltres)
def set_boost(self,key,x,from_='target'):
    self._set_boost(key,x)
    if from_=='target' and x<0:
        self._set_boost('spa',2)

# ----------

@Increment(Moltres,'_move_5')
def value():
    return ('Roost',0,100000,'Status','Flying',0,[])

@Increment(Moltres)
def move_5(self): # Roost
    self.restore(self['max_hp']//2,'heal')
