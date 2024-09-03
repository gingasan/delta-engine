from engine import *


class Steelix(PokemonBase):
    _species='Steelix'
    _types=['Steel','Ground']
    _gender='Male'
    _ability=['Sturdy']
    _move_1=('Earthquake',100,100,'Physical','Ground',0,[])
    _move_2=('Heavy Slam',120,100,'Physical','Steel',0,['contact'])
    def __init__(self):
        super().__init__()
    
    def _take_damage_attack(self,x):
        self.register_act_taken()
        if self['hp']==self['max_hp']:
            self.state['hp']=max(1,self['hp']-x)
        else:
            self.state['hp']=max(0,self['hp']-x)
        if self['hp']==0:
            self.state['status']='FNT'
    
    def move_1(self): # Earthquake
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Heavy Slam
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('def',-1)
            self.set_boost('spd',-1)
