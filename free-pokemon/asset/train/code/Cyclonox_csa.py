from engine import *


class Cyclonox(PokemonBase):
    _species='Cyclonox'
    _types=['Rock','Fighting']
    _gender='Male'
    _ability=['Titan Gaze','Single Mind']
    _move_1=('Cyclone Smash',120,85,'Physical','Rock',0,[])
    _move_2=('Titanic Roar',100,90,'Special','Fighting',0,[])
    def __init__(self):
        super().__init__()

    def endturn(self):
        if self['conditions'].get('TITAN_GAZE'):
            self['conditions']['TITAN_GAZE']['counter']+=1
            if self['conditions']['TITAN_GAZE']['counter']==2:
                del self['conditions']['TITAN_GAZE']

    def take_damage_attack(self,x):
        self.register_act_taken()
        if self['act_taken']['category']=='Special':
            self.set_condition('TITAN_GAZE',counter=0)
        self._set_hp(-x)        

    def get_power(self):
        power=self['act']['power']
        if self['act']['type']=='Rock':
            if self['conditions'].get('TITAN_GAZE') and self['conditions']['TITAN_GAZE']['counter']==1:
                power*=1.5
                del self['conditions']['TITAN_GAZE']
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Cyclone Smash
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('def',-1)
    
    def move_2(self): # Titanic Roar
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('Confusion',counter=0)

# ----------

@Increment(Cyclonox,'_move_3')
def value():
    return ('Crafted Strike',90,100000,'Physical','Rock',0,[])

@Increment(Cyclonox)
def move_3(self): # Crafted Strike
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.set_boost('def',+1,'self')

# ----------

@Increment(Cyclonox,'_move_4')
def value():
    return ('Mighty Stomp',80,100,'Physical','Fighting',0,[])

@Increment(Cyclonox)
def move_4(self): # Mighty Stomp
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<10/100:
            self.target.set_condition('Flinch',counter=0)
