from engine import *


class Brontogon(PokemonBase):
    _species='Brontogon'
    _types=['Grass','Rock']
    _gender='Male'
    _ability=['Tail Whip']
    _move_1=('Herbivore Slam',100,90,'Physical','Grass',0,['contact'])
    _move_2=('Rock Crush',80,95,'Physical','Rock',0,['contact'])
    def __init__(self):
        super().__init__()

    def random_stat_boost(self):
        if rnd()<50/100:
            stat=rndc(['atk','def','spa','spd','spe'])
            self.set_boost(stat,+1)

    def move_1(self): # Herbivore Slam
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('def',-1)
        self.random_stat_boost()

    def move_2(self): # Rock Crush
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<25/100:
                self.target.set_condition('Flinch',counter=0)
        self.random_stat_boost()

# ----------

@Increment(Brontogon,'_move_3')
def value():
    return ('Tail Lash',60,100,'Physical','Normal',0,['contact'])

@Increment(Brontogon)
def move_3(self): # Tail Lash
    for _ in range(2):
        attack_ret=self.attack()
        if attack_ret['miss'] or attack_ret['immune']:
            break
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if self.target.isfaint():
            break
    self.random_stat_boost()

# ----------

@Increment(Brontogon,'_move_4')
def value():
    return ('Stone Garden',0,100000,'Status','Rock',0,[])

@Increment(Brontogon)
def move_4(self): # Stone Garden
    self.set_boost('def',2,'self')
    self.restore(self['max_hp']//4,'heal')

# ----------

@Increment(Brontogon,'_ability')
def value():
    return ['Tail Whip','Boulder Shield']

@Increment(Brontogon)
def take_damage_attack(self,x):
    self.register_act_taken()
    if self['act_taken']['category']=='Physical':
        x=int(x*(2/3))
    self._set_hp(-x)

# ----------

@Increment(Brontogon,'_move_5')
def value():
    return ('Leaf Surge',90,100,'Special','Grass',0,[])

@Increment(Brontogon)
def move_5(self): # Leaf Surge
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_status('PAR')
    self.random_stat_boost()
