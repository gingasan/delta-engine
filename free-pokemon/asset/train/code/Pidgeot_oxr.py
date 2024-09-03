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
        bar=6 if key in ['atk','def','spa','spd','spe'] else 3
        if x>0:
            self['boosts'][key]=min(bar,self['boosts'][key]+x)
        else:
            self['boosts'][key]=max(-bar,self['boosts'][key]+x)

    def endturn(self):
        if self['conditions'].get('RECHARGE'):
            if self['conditions']['RECHARGE']['counter']==0:
                self['conditions']['RECHARGE']['counter']+=1
            else:
                del self['conditions']['RECHARGE']
                self.state['canact']=True
    
    def move_1(self): # Steel Wing
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<10/100: self.set_boost('def',1,'self')
    
    def move_2(self): # Hyper Beem
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
        if not self.target.isfaint():
            self.set_condition('RECHARGE',counter=0)
            self.state['canact']=False
