from engine import *


class Zephyra(PokemonBase):
    _species='Zephyra'
    _types=['Flying']
    _gender='Mele'
    _ability=['Speedy Recovery']
    _move_1=('Brave Bird',120,100,'Physical','Flying',0,['contact'])
    _move_2=('Steel Wing',70,90,'Physical','Steel',0,['contact'])
    def __init__(self):
        super().__init__()
    
    def endturn(self):
        if self['hp']<self['max_hp']//3:
            self.set_boost('spe',2)
            self.restore(self['max_hp']//6,'heal')
    
    def move_1(self): # Brave Bird
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if damage>0:
                self.take_damage(int(0.33*damage),'recoil')
    
    def move_2(self): # Steel Wing
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<10/100:
                self.set_boost('def',1,'self')
