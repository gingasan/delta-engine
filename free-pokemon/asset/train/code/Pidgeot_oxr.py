from engine import *


class Pidgeot(PokemonBase):
    _species='Pidgeot'
    _types=['Normal','Flying']
    _gender='Male'
    _ability=['Keen Eye']
    _move_1=('Steel Wing',70,90,'Physical','Steel',0,['contact'])
    _move_2=('Hyper Beam',150,90,'Special','Normal',0,[])
    def __init__(self):
        super().__init__()

    def set_boost(self,key,x,from_='target'):
        if key=='accuracy' and x<0:
            return
        self._set_boost(key,x)

    def endturn(self):
        if self['conditions'].get('RECHARGE'):
            if self['conditions']['RECHARGE']['counter']==0:
                self['conditions']['RECHARGE']['counter']+=1
            else:
                del self['conditions']['RECHARGE']
                self.state['canact']=True
    
    def move_1(self): # Steel Wing
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<10/100: self.set_boost('def',1,'self')
    
    def move_2(self): # Hyper Beem
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
        if not self.target.isfaint():
            self.set_condition('RECHARGE',counter=0)
            self.state['canact']=False
