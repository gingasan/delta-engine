from engine import *


class Hoopa(PokemonBase):
    _species='Hoopa'
    _types=['Psychic','Dark']
    _gender='Neutral'
    _ability=['Contrary']
    _move_1=('Hyperspace Fury',100,100,'Special','Dark',0,[])
    _move_2=('Psychic Combat',120,100,'Physical','Psychic',0,['contact'])
    def __init__(self):
        super().__init__()

    def set_boost(self,key,x,from_='target'):
        x=-x
        bar=6 if key in ['atk','def','spa','spd','spe'] else 3
        if x>0:
            self['boosts'][key]=min(bar,self['boosts'][key]+x)
        else:
            self['boosts'][key]=max(-bar,self['boosts'][key]+x)
        self.log("{}'s {} is {} by {}.".format(self._species,{
            'atk':'Attack','def':'Defense','spa':'Special Attack','spd':'Special Defense','spe':'Speed'}[key],'raised' if x>0 else 'lowered',x))

    def move_1(self): # Hyperspace Fury
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=int(0.5*self.target['hp'])
            self.target.take_damage(damage)
    
    def move_2(self): # Psychic Combat
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self.set_boost('def',-1)
            self.set_boost('spd',-1)
