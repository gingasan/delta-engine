from engine import *


class Swampert(PokemonBase):
    _species='Swampert'
    _types=['Water','Ground']
    _gender='Female'
    _ability=['Torrent']
    _move_1=('Liquidation',85,100,'Physical','Water',0,['contact'])
    _move_2=('Earthquake',100,100,'Physical','Ground',0,[])
    def __init__(self):
        super().__init__()

    def clear_boost(self):
        for key in ['atk','def','spa','spd','spe','accuracy','crit']:
            self['boosts'][key]=0

    def start_move(self):
        if self['act']['type']=='Water' and self['max_hp']//2<self['hp']<self['max_hp']:
            self.clear_boost()
            self.set_boost('atk',1,'self')
            self.set_boost('spa',1,'self')
    
    def move_1(self): # Liquidation
        self.start_move()
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100: self.target.set_boost('def',-1)
    
    def move_2(self): # Earthquake
        self.start_move()
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
