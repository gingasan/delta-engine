from engine import *


class Pelipper(PokemonBase):
    _species='Pelipper'
    _types=['Water','Flying']
    _gender='Male'
    _ability=['Rain Dish']
    _move_1=('Hydro Pump',110,80,'Special','Water',0,[])
    _move_2=('Hurricane',110,70,'Special','Flying',0,[])
    def __init__(self):
        super().__init__()

    def endturn(self):
        if self.env.get('Rain'):
            self.restore(self['max_hp']//16,'heal')

    def get_accuracy(self):
        acc=self['act']['accuracy']
        if self['act']['id']=='Hurricane':
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

    def move_1(self): # Hydro Pump
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('spe',-1)

    def move_2(self): # Hurricane
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('Confusion',counter=0)

# ----------

@Increment(Pelipper,'_move_3')
def value():
    return ('Psychic',90,100,'Special','Psychic',0,[])

@Increment(Pelipper)
def move_3(self): # Psychic
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_boost('spd',-1)
