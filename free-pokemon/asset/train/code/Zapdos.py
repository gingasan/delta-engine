from engine import *


class Zapdos(PokemonBase):
    _species='Zapdos'
    _types=['Electric','Flying']
    _gender='Neutral'
    _ability=['Laser Eye']
    _move_1=('Hurricane',110,70,'Special','Flying',0,[])
    _move_2=('Zap Cannon',120,50,'Special','Electric',0,[])
    def __init__(self):
        super().__init__()

    def get_accuracy(self):
        acc=self['act']['accuracy']
        if self.get_env('Rain') and self['act']['id']=='Hurricane':
            acc=1e5
        elif self.get_env('Sunlight') and self['act']['id']=='Hurricane':
            acc=50
        if acc<=70:
            acc=int(acc*1.5)
        acc_mult=[1.0,1.33,1.67,2.0]
        if self['boosts']['accuracy']>=0:
            acc*=acc_mult[self['boosts']['accuracy']]
        else:
            acc/=acc_mult[self['boosts']['accuracy']]
        acc*=self.target.get_evasion()
        return acc/100

    def move_1(self): # Hurricane
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('CONFUSION',counter=0)

    def move_2(self): # Zap Cannon
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
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
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_boost('spd',-1)

# ----------

@Increment(Zapdos,'_move_4')
def value():
    return ('Energy recovery',0,100000,'Status','Electric',0,[])

@Increment(Zapdos)
def move_4(self): # Energy recovery
    if self['last_act'] and self['last_act']['type']=='Electric':
        self.set_boost('spa',1,'self')
        self.set_boost('spd',1,'self')
        self.set_boost('spe',1,'self')

# ----------

@Increment(Zapdos,'_ability')
def value():
    return ['Laser Eye','Competitive']

@Increment(Zapdos)
def set_boost(self,key,x,from_='target'):
    bar=6 if key in ['atk','def','spa','spd','spe'] else 3
    if x>0:
        self['boosts'][key]=min(bar,self['boosts'][key]+x)
    else:
        self['boosts'][key]=max(-bar,self['boosts'][key]+x)
    self.log(script='boost',species=self._species,key=key,x=x)
    if from_=='target' and x<0:
        for _ in range(x):
            self['boosts']['spa']=min(bar,self['boosts'][key]+2)
        self.log('Due to Competitive, Zapdos further raises its SpA. by {}.'.format(2*x))

# ----------

@Increment(Zapdos,'_move_5')
def value():
    return ('Inferno',100,50,'Special','Fire',0,[])

@Increment(Zapdos)
def move_5(self): # Inferno
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint():
            self.target.set_status('BRN')
