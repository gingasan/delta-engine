from engine import *


class Blissey(PokemonBase):
    _species='Blissey'
    _types=['Normal']
    _gender='Female'
    _ability=['Serene Grace']
    _move_1=('Seismic Toss',0,100,'Physical','Fighting',0,['contact'])
    _move_2=('Shadow Ball',80,100,'Special','Ghost',0,[])
    def __init__(self):
        super().__init__()

    def get_effect_chance(self,chance):
        return 2*chance if chance<=0.5 else 1
    
    def move_1(self): # Seismic Toss
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage=100
            self.target.take_damage(damage)
    
    def move_2(self): # Shadow Ball
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<self.get_effect_chance(20/100):
                self.target.set_boost('spd',-1)

# ----------

@Increment(Blissey,'_move_3')
def value():
    return ('Calm Mind',0,100000,'Status','Psychic',0,[])

@Increment(Blissey)
def move_3(self): # Calm Mind
    self.set_boost('spa',+1,'self')
    self.set_boost('spd',+1,'self')

# ----------

@Increment(Blissey,'_move_4')
def value():
    return ('Soft-Boiled',0,100000,'Status','Normal',0,[])

@Increment(Blissey)
def move_4(self): # Soft-Boiled
    self.restore(self['max_hp']//2,'heal')
