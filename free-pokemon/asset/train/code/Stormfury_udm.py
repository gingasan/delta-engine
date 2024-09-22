from engine import *


class Stormfury(PokemonBase):
    _species='Stormfury'
    _types=['Electric','Flying']
    _gender='Female'
    _ability=['Storm Surge']
    _move_1=('Thunder Strike',90,70,'Special','Electric',0,[])
    _move_2=('Aerial Slash',75,95,'Physical','Flying',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.env.set_side_condition('Storm Surge',self.side_id,from_=self._species,counter=0,max_count=3)

    def get_accuracy(self):
        acc=self['act']['accuracy']
        if self.env.get_side_condition('Storm Surge',self.side_id) and self['act']['type']=='Electric':
            acc=100
        acc_mult=[1.0,1.33,1.67,2.0]
        if self['boosts']['accuracy']>=0:
            acc*=acc_mult[self['boosts']['accuracy']]
        else:
            acc/=acc_mult[self['boosts']['accuracy']]
        acc*=(1-self.target.get_evasion())
        return acc/100

    def move_1(self): # Thunder Strike
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('PAR')

    def move_2(self): # Aerial Slash
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('spe',-1)

# ----------

@Increment(Stormfury,'_move_3')
def value():
    return ('Storm Burst',100,80,'Special','Electric',0,[])

@Increment(Stormfury)
def move_3(self): # Storm Burst
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('Confusion',counter=0)

# ----------

@Increment(Stormfury,'_move_4')
def value():
    return ('Gale Wing',85,90,'Special','Flying',0,[])

@Increment(Stormfury)
def move_4(self): # Gale Wing
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Stormfury,'_ability')
def value():
    return ['Storm Surge','Aircurrent']

@Increment(Stormfury)
def get_power(self):
    power=self['act']['power']
    if self['act']['type']=='Flying':
        power*=1.2
    return int(power*self.get_weather_power_mult())

# ----------

@Increment(Stormfury,'_move_5')
def value():
    return ('Volt Shield',0,100,'Status','Electric',0,[])

@Increment(Stormfury)
def move_5(self): # Volt Shield
    self.set_boost('def',1,'self')
