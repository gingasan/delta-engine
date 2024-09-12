from engine import *


class Wangtianhou(PokemonBase):
    _species='Wangtianhou'
    _types=['Dark','Dragon']
    _gender='Neutral'
    _ability=['Dragon Bane']
    _move_1=('Heavenly Bite',100,90,'Physical','Dark',0,['contact'])
    _move_2=('Dragon Fury',120,85,'Special','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def get_other_mult(self):
        mult=1
        if self.target['type']=='Fairy':
            mult*=1.3
        return mult

    def move_1(self): # Heavenly Bite
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('spd',-1)

    def move_2(self): # Dragon Fury
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('CONFUSION',counter=0)

# ----------

@Increment(Wangtianhou,'_move_3')
def value():
    return ('Celestial Roar',0,100,'Status','Dark',0,[])

@Increment(Wangtianhou)
def move_3(self): # Celestial Roar
    self.target.set_boost('atk',-1)

# ----------

@Increment(Wangtianhou,'_move_4')
def value():
    return ('Heaven Shield',0,100000,'Status','Dragon',0,[])

@Increment(Wangtianhou)
def move_4(self): # Heaven Shield
    self.set_boost('def',+1,'self')
    self.set_boost('spd',+1,'self')

# ----------

@Increment(Wangtianhou,'_ability')
def value():
    return ['Dragon Bane','Celestial Watch']

@Increment(Wangtianhou)
def set_status(self,x):
    return
