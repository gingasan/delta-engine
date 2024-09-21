from engine import *


class Kangaskhan(PokemonBase):
    _species='Kangaskhan'
    _types=['Normal']
    _gender='Female'
    _ability=['Scrappy']
    _move_1=('Double-Edge',120,100,'Physical','Normal',0,['contact'])
    _move_2=('Fire Punch',75,100,'Physical','Fire',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_type_effect(self):
        move_type=self['act']['type']
        target_types=self.target['types']
        effect=1
        for tt in target_types:
            if tt=='Ghost' and (self['act']['type']=='Normal' or self['act']['type']=='Fighting'):
                effect*=1
            else:
                effect*=TYPEEFFECTIVENESS[move_type][tt]
        return effect

    def move_1(self): # Double-Edge
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.take_damage(int(0.33*damage),'recoil')

    def move_2(self): # Fire Punch
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: self.target.set_status('BRN')

# ----------

@Increment(Kangaskhan,'_move_3')
def value():
    return ('Earthquake',100,100,'Physical','Ground',0,[])

@Increment(Kangaskhan)
def move_3(self): # Earthquake
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)

# ----------

@Increment(Kangaskhan,'_move_4')
def value():
    return ('Rock Slide',75,90,'Physical','Rock',0,[])

@Increment(Kangaskhan)
def move_4(self): # Rock Slide
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Kangaskhan,'_ability')
def value():
    return ['Scrappy','Parental Bond']

@Increment(Kangaskhan)
def move_1(self): # Double-Edge
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.take_damage(int(0.33*damage),'recoil')
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']//4
        self.target.take_damage(damage)
        self.take_damage(int(0.33*damage),'recoil')

@Increment(Kangaskhan)
def move_2(self): # Fire Punch
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100: self.target.set_status('BRN')
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']//4
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100: self.target.set_status('BRN')

@Increment(Kangaskhan)
def move_3(self): # Earthquake
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']//4
        self.target.take_damage(damage)

@Increment(Kangaskhan)
def move_4(self): # Rock Slide
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('Flinch',counter=0)
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']//4
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('Flinch',counter=0)

# ----------

@Increment(Kangaskhan,'_move_5')
def value():
    return ('Power-Up Punch',40,100,'Physical','Fighting',0,['contact'])

@Increment(Kangaskhan)
def move_5(self): # Power-Up Punch
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_boost('atk',1,'self')
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']//4
        self.target.take_damage(damage)
        self.set_boost('atk',1,'self')
