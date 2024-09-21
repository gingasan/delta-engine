from engine import *


class Annihilape(PokemonBase):
    _species='Annihilape'
    _types=['Fighting','Ghost']
    _gender='Male'
    _ability=['Defiant']
    _move_1=('Rage Fist',50,100,'Physical','Ghost',0,['contact','punch'])
    _move_2=('Close Combat',120,100,'Physical','Fighting',0,['contact'])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_condition('RAGE_FIST',counter=0)

    def set_boost(self,key,x,from_='target'):
        self._set_boost(key,x)
        if from_=='target' and x<0:
            self._set_boost('atk',2)
    
    def get_power(self):        
        power=self['act']['power']
        if self['act']['id']=='Rage Fist':
            power=min(350,50+50*self['conditions']['RAGE_FIST']['counter'])
        return int(power*self.get_weather_power_mult())
    
    def move_1(self): # Rage Fist
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self['conditions']['RAGE_FIST']['counter']+=1

    def move_2(self): # Close Combat
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('def',-1,'self')
            self.set_boost('spd',-1,'self')

# ----------

@Increment(Annihilape,'_move_3')
def value():
    return ('Final Gambit',0,100,'Special','Fighting',0,[])

@Increment(Annihilape)
def move_3(self): # Final Gambit
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        self.target.take_damage(self['hp'])
        self._faint()
