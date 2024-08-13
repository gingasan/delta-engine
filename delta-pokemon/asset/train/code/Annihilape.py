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
        bar=6 if key in ['atk','def','spa','spd','spe'] else 3
        if x>0:
            self['boosts'][key]=min(bar,self['boosts'][key]+x)
        else:
            self['boosts'][key]=max(-bar,self['boosts'][key]+x)
            if from_=='target':
                for _ in range(x):
                    self.set_boost('spa',2,'self')
    
    def get_power(self):        
        power=self['act']['power']
        if self['act']['id']=='Rage Fist':
            power=min(350,50+50*self['conditions']['RAGE_FIST']['counter'])
        return int(power*self.get_weather_power_mult())
    
    def move_1(self): # Rage Fist
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self['conditions']['RAGE_FIST']['counter']+=1

    def move_2(self): # Close Combat
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('def',-1,'self')
            self.set_boost('spd',-1,'self')

# -------------------------------------------------------------

@Increment(Annihilape,'_move_3')
def value():
    return ('Final Gambit',0,100,'Special','Fighting',0,[])

@Increment(Annihilape)
def move_3(self): # Final Gambit
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        self.target.take_damage(self['hp'])
        self.take_damage(self['hp'],'loss')
