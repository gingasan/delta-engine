from engine import *


class Grovyle(PokemonBase):
    _species='Grovyle'
    _types=['Grass']
    _gender='Male'
    _ability=['Seed Sower']
    _move_1=('Leech Seed',0,90,'Status','Grass',0,[])
    _move_2=('Seed Flare',120,85,'Special','Grass',0,[])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        self._set_hp(-x)        
        if self['hp']==0:
            return
        self.env.set_terrain('Grassy Terrain',from_=self._species)
    
    def endturn(self):
        if self.target['conditions'].get('LEECH_SEED'):
            self.target.take_damage(self.target['max_hp']//8,'loss')
            self.restore(self.target['max_hp']//8,'drain')

    def move_1(self): # Leech Seed
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            self.target.set_condition('LEECH_SEED',counter=0)

    def move_2(self): # Seed Flare 
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                self.target.set_boost('spd',-2)
