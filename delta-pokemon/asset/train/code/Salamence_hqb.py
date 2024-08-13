from engine import *


class Salamence(PokemonBase):
    _species='Salamence'
    _types=['Dragon','Flying']
    _gender='Female'
    _ability=['Fast Recovery']
    _move_1=('Dragon Claw',80,100,'Physical','Dragon',0,[])
    _move_2=('Dual Wingbeat',40,90,'Physical','Flying',0,['contact'])
    def __init__(self):
        super().__init__()

    def take_damage(self,x,from_='attack'):
        if from_=='attack':
            self._take_damage_attack(x)
        elif from_=='loss':
            self._take_damage_loss(x)
        elif from_=='recoil':
            self._take_damage_recoil(x)
        if self['hp']>0 and x>=200:
            self.set_boost('atk',2,'self')
    
    def move_1(self): # Dragon Claw
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Dual Wingbeat
        hit=True; i=0
        while hit and i<2:
            damage_ret=self.get_damage()
            if damage_ret['miss']: break
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True
