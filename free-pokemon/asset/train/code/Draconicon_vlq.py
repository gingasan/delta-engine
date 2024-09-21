from engine import *


class Draconicon(PokemonBase):
    _species='Draconicon'
    _types=['Dragon','Poison']
    _gender='Female'
    _ability=['Poisonous Skin']
    _move_1=('Draconic Beam',80,100,'Special','Dragon',0,[])
    _move_2=('Venoshock',65,100,'Special','Poison',0,[])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        self._set_hp(-x)        
        if self['hp']==0:
            return
        if self['act_taken'] and 'property' in self['act_taken'] and 'contact' in self['act_taken']['property']:
            if rnd()<20/100:
                self.target.set_condition('Confusion',counter=0)
    
    def get_power(self):
        power=self['act']['power']
        if self.target.isstatus('PSN') or self.target.isstatus('TOX'):
            power*=2
        return int(power*self.get_weather_power_mult())

    def move_1(self): # Draconic Beam
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_boost('def',-1)
                self.target.set_boost('spd',-1)
    
    def move_2(self): # Venoshock
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
