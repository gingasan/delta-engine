from engine import *


class Malzeno(PokemonBase):
    _species='Malzeno'
    _types=['Dragon','Dark']
    _gender='Neutral'
    _ability=['Symbiotic Control']
    _move_1=('Bloodblight Strike',90,95,'Physical','Dark',0,[])
    _move_2=('Dragon Breath',80,100,'Special','Dragon',0,[])
    def __init__(self):
        super().__init__()

    def get_power(self):
        power=self['act']['power']
        if self['act']['id'] in ['Bloodblight Strike','Quirio Beam']:
            power*=1.25
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Bloodblight Strike
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.restore(int(self.target['max_hp']*0.125),'drain')
            self.recharge()
    
    def move_2(self): # Dragon Breath
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<20/100:
                self.target.set_status('PAR')

# ----------

@Increment(Malzeno,'_move_3')
def value():
    return ('Quirio Beam',80,100,'Special','Dragon',0,[])

@Increment(Malzeno)
def move_3(self): # Quirio Beam
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        self.restore(int(damage//2),'drain')

# ----------

@Increment(Malzeno,'_ability')
def value():
    return ['Symbiotic Control','Bloodening Surge']

@Increment(Malzeno)
def onswitch(self):
    self.set_condition('RECHARGE',counter=0)

@Increment(Malzeno)
def recharge(self):
    self['conditions']['RECHARGE']['counter']+=1
    if self['conditions']['RECHARGE']['counter']==5:
        self.set_condition('BLOODENING',counter=0)

@Increment(Malzeno)
def _restore_drain(self,x):
    self.state['hp']=min(self['max_hp'],self['hp']+x)
    self.log('{} heals {} HP.'.format(self._species,x))
    self.recharge()

@Increment(Malzeno)
def get_stat(self,key,boost=None):
    stat=self['stats'][key]
    boost=self['boosts'][key] if not boost else boost
    stat_ratio={0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}[min(6,abs(boost))]
    if boost<0:
        stat_ratio=1/stat_ratio
    stat_ratio*=self.get_weather_stat_mult(key)
    if key=='spe' and self.isstatus('PAR'):
        stat_ratio*=0.5
    if key in ['atk','spa'] and self['conditions'].get('BLOODENING'):
        stat_ratio*=1.5
    return int(stat*stat_ratio)
