from engine import *


class Gholdengo(PokemonBase):
    _species='Gholdengo'
    _types=['Steel','Ghost']
    _gender='Neutral'
    _ability=['Good as Gold']
    _move_1=('Make It Rain',120,100,'Special','Steel',0,[])
    _move_2=('Shadow Ball',80,100,'Special','Ghost',0,[])
    def __init__(self):
        super().__init__()

    def get_immune(self):
        if self.target['act']['category']=='Status':
            return True
        return False
    
    def move_1(self): # Make It Rain
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('spa',-1,'self')
    
    def move_2(self): # Shadow Ball
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('spd',-1)

# ----------

@Increment(Gholdengo,'_move_3')
def value():
    return ('Thunder Wave',0,90,'Status','Electric',0,[])

@Increment(Gholdengo)
def move_3(self): # Thunder Wave
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        self.target.set_status('PAR')

# ----------

@Increment(Gholdengo,'_move_4')
def value():
    return ('Recover',0,100000,'Status','Normal',0,[])

@Increment(Gholdengo)
def move_4(self): # Recover
    self.restore(self['max_hp']//2,'heal')
