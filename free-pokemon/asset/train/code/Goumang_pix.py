from engine import *


class Goumang(PokemonBase):
    _species='Goumang'
    _types=['Grass','Flying']
    _gender='Male'
    _ability=['Verdant Growth']
    _move_1=('Fusang Flame',90,100,'Special','Fire',0,[])
    _move_2=('Willow Whip',80,100,'Physical','Grass',0,[])
    def __init__(self):
        super().__init__()

    def endturn(self):
        if self.env.get('Sunlight'):
            self.restore(self['max_hp']//16,'heal')

    def move_1(self): # Fusang Flame
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_status('BRN')

    def move_2(self): # Willow Whip
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('spe',-1)

# ----------

@Increment(Goumang,'_move_3')
def value():
    return ('Dragon Ride',100,95,'Physical','Flying',2,[])

@Increment(Goumang)
def move_3(self): # Dragon Ride
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# ----------

@Increment(Goumang,'_move_4')
def value():
    return ('Spring Renewal',0,100000,'Status','Grass',0,[])

@Increment(Goumang)
def move_4(self): # Spring Renewal
    self.restore(self['max_hp']//2,'heal')
    self.state['status']=None

# ----------

@Increment(Goumang,'_ability')
def value():
    return ['Verdant Growth','Spring Guardian']

@Increment(Goumang)
def get_power(self):
    power=self['act']['power']
    if self.env.get('Sunlight') and self['act']['type']=='Grass':
        power*=1.3
    return int(power*self.get_weather_power_mult())
