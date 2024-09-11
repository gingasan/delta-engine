from engine import *


class Milotic(PokemonBase):
    _species='Milotic'
    _types=['Water']
    _gender='Female'
    _ability=['Competitive']
    _move_1=('Scald',80,100,'Special','Water',0,[])
    _move_2=('Leaf Storm',130,90,'Special','Grass',0,[])
    def __init__(self):
        super().__init__()

    def set_boost(self,key,x,from_='target'):
        if x<0:
            self.set_boost('spa',2)
        bar=6 if key in ['atk','def','spa','spd','spe'] else 3
        if x>0:
            self['boosts'][key]=min(bar,self['boosts'][key]+x)
        else:
            self['boosts'][key]=max(-bar,self['boosts'][key]+x)
        self.log("{}'s {} is {} by {}.".format(self._species,{
            'atk':'Attack','def':'Defense','spa':'Special Attack','spd':'Special Defense','spe':'Speed'}[key],'raised' if x>0 else 'lowered',x))

    def move_1(self): # Scald
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<0.3:
                self.target.set_status('BRN')

    def move_2(self): # Leaf Storm
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            self['boosts']['spa']=max(-6,self['boosts']['spa']-2)
