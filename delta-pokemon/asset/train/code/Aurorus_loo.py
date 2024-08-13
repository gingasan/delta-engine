from engine import *


class Aurorus(PokemonBase):
    _species='Aurorus'
    _types=['Rock','Ice']
    _gender='Female'
    _ability=['Refrigerate']
    _move_1=('Earth Power',90,100,'Special','Ground',0,[])
    _move_2=('Hyper Beam',150,90,'Special','Normal',0,[])
    def __init__(self):
        super().__init__()

    def get_power(self):
        power=self['act']['power']
        if self['act']['type']=='Normal':
            self['act']['type']='Ice'
            power*=1.3
        return int(power*self.get_weather_power_mult())

    def endturn(self):
        if self['conditions'].get('RECHARGE'):
            if self['conditions']['RECHARGE']['counter']==0:
                self['conditions']['RECHARGE']['counter']+=1
            else:
                del self['conditions']['RECHARGE']
                self.state['canact']=True
    
    def move_1(self): # Earth Power
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_boost('spd',-1)
    
    def move_2(self): # Hyper Beem
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
        if not self.target.isfaint():
            self.set_condition('RECHARGE',counter=0)
            self.state['canact']=False
