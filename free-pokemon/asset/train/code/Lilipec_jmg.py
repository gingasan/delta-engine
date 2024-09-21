from engine import *


class Lilipec(PokemonBase):
    _species='Lilipec'
    _types=['Ground','Water']
    _gender='Neutral'
    _ability=['Harbinger']
    _move_1=('Mudslide',80,100,'Special','Ground',0,[])
    _move_2=('Aqua Pulse',75,100,'Special','Water',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.env.set_weather('Sandstorm',from_=self._species,max_count=5)

    def move_1(self): # Mudslide
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('spe',-1)

    def move_2(self): # Aqua Pulse
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('Confusion',counter=0)

# ----------

@Increment(Lilipec,'_move_3')
def value():
    return ('Earthquake',100,100,'Physical','Ground',0,[])

@Increment(Lilipec)
def move_3(self): # Earthquake
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# ----------

@Increment(Lilipec,'_ability')
def value():
    return ['Harbinger','Industrious Call']

@Increment(Lilipec)
def industrious_call(self):
    if self['act']['category']=='Status':
        self.set_boost('spa',1,'self')

@Increment(Lilipec)
def move_1(self): # Mudslide
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_boost('spe',-1)
    self.industrious_call()

@Increment(Lilipec)
def move_2(self): # Aqua Pulse
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('Confusion',counter=0)
    self.industrious_call()

@Increment(Lilipec)
def move_3(self): # Earthquake
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
    self.industrious_call()
