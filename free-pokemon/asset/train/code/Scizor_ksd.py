from engine import *


class Scizor(PokemonBase):
    _species='Scizor'
    _types=['Bug','Steel']
    _gender='Female'
    _ability=['Technician']
    _move_1=('Steel Wing',70,90,'Physical','Steel',0,['contact'])
    _move_2=('X-Scissor',80,100,'Physical','Bug',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_power(self):
        power=self['act']['power']
        if power<=60:
            power=int(power*1.5)
        return int(power*self.get_weather_power_mult())
    
    def get_crit(self):
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        if self['act']['id']=='Steel Wing':
            crit_ratio=min(3,crit_ratio+1)
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit
    
    def move_1(self): # Steel Wing
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: 
                self.set_boost('def',1,'self')

    def move_2(self): # X-Scissor
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
        if self['hp']<self['max_hp']//3:
            self.set_boost('spe',1,'self')
