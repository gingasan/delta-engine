from engine import *


class Alomomola(PokemonBase):
    _species='Alomomola'
    _types=['Water']
    _gender='Male'
    _ability=['Hydration']
    _move_1=('Scald',80,100,'Special','Water',0,[])
    _move_2=('Protect',0,100000,'Status','Normal',4,[])
    def __init__(self):
        super().__init__()

    def endturn(self):
        if self.env.get('Rain'):
            self.state['status']=None
        if self['conditions'].get('Protected'):
            del self['conditions']['Protected']

    def move_1(self): # Scald
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('BRN')
                if self.target['status']=='FRZ':
                    self.target.state['status']=None

    def move_2(self): # Protect
        if self['last_act'] and self['last_act']['id']=='Protect':
            return
        self.set_condition('Protected',counter=0)
    
    def take_damage_attack(self,x):
        if self['conditions'].get('Protected'):
            del self['conditions']['Protected']
            return
        self.register_act_taken()
        self._set_hp(-x)
