from engine import *


class Magnamalo(PokemonBase):
    _species='Magnamalo'
    _types=['Fire','Poison']
    _gender='Male'
    _ability=['Hellfire Metabolism']
    _move_1=('Hellfire Blast',100,90,'Special','Fire',0,[])
    _move_2=('Poison Vents',70,100,'Special','Poison',0,[])
    def __init__(self):
        super().__init__()

    def move_1(self): # Hellfire Blast
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('spa',+1,'self')
            self.take_damage(self['max_hp']//16,'loss')

    def move_2(self): # Poison Vents
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('PSN')

# ----------

@Increment(Magnamalo,'_move_3')
def value():
    return ('Explosive Strike',80,100,'Physical','Fire',0,[])

@Increment(Magnamalo)
def move_3(self): # Explosive Strike
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.target.take_damage(self.target['max_hp']//10,'loss')
        self.take_damage(self['max_hp']//10,'recoil')
        self.set_boost('spa',+1,'self')
        self.take_damage(self['max_hp']//16,'loss')

# ----------

@Increment(Magnamalo,'_move_4')
def value():
    return ('Gas Cloud',0,100000,'Status','Poison',0,[])

@Increment(Magnamalo)
def move_4(self): # Gas Cloud
    self.env.set_side_condition('Gas Cloud',self.target.side_id,from_=self._species,counter=0,max_count=2)

@Increment(Magnamalo)
def endturn(self):
    if self.env.get_side_condition('Gas Cloud',self.target.side_id):
        if not self.target.istype('Poison'):
            self.target.set_boost('accuracy',-1)

# ----------

@Increment(Magnamalo,'_ability')
def value():
    return ['Hellfire Metabolism','Volatile Flame']

@Increment(Magnamalo)
def move_1(self): # Hellfire Blast
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<50/100:
            self.target.take_damage(self.target['max_hp']//16,'loss')
        self.set_boost('spa',+1,'self')
        self.take_damage(self['max_hp']//16,'loss')

@Increment(Magnamalo)
def move_3(self): # Explosive Strike
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.target.take_damage(self.target['max_hp']//10,'loss')
        self.take_damage(self['max_hp']//10,'recoil')
        if not self.target.isfaint() and rnd()<50/100:
            self.target.take_damage(self.target['max_hp']//16,'loss')
        self.set_boost('spa',+1,'self')
        self.take_damage(self['max_hp']//16,'loss')
