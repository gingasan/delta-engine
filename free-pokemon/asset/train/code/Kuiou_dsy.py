from engine import *


class Kuiou(PokemonBase):
    _species='Kuiou'
    _types=['Dragon','Electric']
    _gender='Neutral'
    _ability=['Storm Command']
    _move_1=('Celestial Roar',100,90,'Special','Electric',0,[])
    _move_2=('Ruler Strike',90,100,'Physical','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def get_power(self):
        power=self['act']['power']
        if self['act']['type']=='Electric':
            power*=1.5
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Celestial Roar
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            if self.target.isstatus('PAR'):
                damage=int(damage*1.5)
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('PAR')
    
    def move_2(self): # Ruler Strike
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            if self.target['hp']>self['hp']:
                damage=int(damage*2)
            self.target.take_damage(damage)

# ----------

@Increment(Kuiou,'_move_3')
def value():
    return ('Guardian Shield',0,100000,'Status','Dragon',0,[])

@Increment(Kuiou)
def move_3(self): # Guardian Shield
    self.set_boost('def',1,'self')
    self.set_boost('spd',1,'self')

# ----------

@Increment(Kuiou,'_ability')
def value():
    return ['Storm Command','Celestial Guard']

@Increment(Kuiou)
def take_damage_attack(self,x):
    self.register_act_taken()
    if self['act_taken']['type']=='Dragon':
        x=int(x*0.5)
        self.state['hp']=min(self['max_hp'],self['hp']+self['max_hp']//8)
    self._set_hp(-x)
