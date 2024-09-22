from engine import *


class Zapdos(PokemonBase):
    _species='Zapdos'
    _types=['Electric','Flying']
    _gender='Neutral'
    _ability=['Laser Eye']
    _move_1=('Hurricane',110,70,'Special','Flying',0,[])
    _move_2=('Zap Cannon',120,50,'Special','Electric',0,[])
    _base=(90,90,85,125,90,120)
    def __init__(self):
        super().__init__()

    def get_accuracy(self):
        acc=self['act']['accuracy']
        if self.env.get('Rain') and self['act']['id']=='Hurricane':
            acc=1e5
        elif self.env.get('Sunlight') and self['act']['id']=='Hurricane':
            acc=50
        if acc<=70:
            acc=int(acc*1.5)
        acc_mult=[1.0,1.33,1.67,2.0]
        if self['boosts']['accuracy']>=0:
            acc*=acc_mult[self['boosts']['accuracy']]
        else:
            acc/=acc_mult[self['boosts']['accuracy']]
        acc*=(1-self.target.get_evasion())
        return acc/100

    def move_1(self): # Hurricane
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('Confusion',counter=0)

    def move_2(self): # Zap Cannon
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                self.target.set_status('PAR')

# ----------

@Increment(Zapdos,'_move_3')
def value():
    return ('Focus Blast',120,70,'Special','Fighting',0,[])

@Increment(Zapdos)
def move_3(self): # Focus Blast
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_boost('spd',-1)

# ----------

@Increment(Zapdos,'_move_4')
def value():
    return ('Energy Recycle',0,100000,'Status','Electric',0,[])

@Increment(Zapdos)
def move_4(self): # Energy Recycle
    if self['last_act'] and self['last_act']['type']=='Electric':
        self.set_boost('spa',1,'self')
        self.set_boost('spd',1,'self')
        self.set_boost('spe',1,'self')
        self.log('Zapdos recycles energy from surrounding ions.',color='yellow')

# ----------

@Increment(Zapdos,'_ability')
def value():
    return ['Laser Eye','Blunder Policy']

@Increment(Zapdos)
def move_1(self): # Hurricane
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('Confusion',counter=0)
    else:
        self.restore(self['max_hp']//5,'heal')
        self.log('Zapdos recycles energy from missing attack.',color='yellow')

@Increment(Zapdos)
def move_2(self): # Zap Cannon
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint():
            self.target.set_status('PAR')
    else:
        self.restore(self['max_hp']//5,'heal')
        self.log('Zapdos recycles energy from missing attack.',color='yellow')

@Increment(Zapdos)
def move_3(self): # Focus Blast
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_boost('spd',-1)
    else:
        self.restore(self['max_hp']//5,'heal')
        self.log('Zapdos recycles energy from missing attack.',color='yellow')

# ----------

@Increment(Zapdos,'_move_5')
def value():
    return ('Inferno',100,50,'Special','Fire',0,[])

@Increment(Zapdos)
def move_5(self): # Inferno
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint():
            self.target.set_status('BRN')
    else:
        self.restore(self['max_hp']//5,'heal')
        self.log('Zapdos recycles energy from missing attack.',color='yellow')
