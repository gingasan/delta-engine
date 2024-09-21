from engine import *


class Charizard(PokemonBase):
    _species='Charizard'
    _types=['Fire','Flying']
    _gender='Male'
    _ability=['Solar Power']
    _move_1=('Fire Blast',110,85,'Special','Fire',0,[])
    _move_2=('Hurricane',110,70,'Special','Flying',0,[])
    def __init__(self):
        super().__init__()
    
    def get_weather_stat_mult(self, key):
        if self.env.get('Sandstorm') and key=='spd' and 'Rock' in self['types']:
            return 1.5
        if self.env.get('Snow') and key=='def' and 'Ice' in self['types']:
            return 1.5
        if self.env.get('Sunlight') and key=='spa':
            return 1.5
        return 1.
    
    def endturn(self):
        if self.env.get('Sunlight'):
            self.take_damage(self['max_hp']//8,'loss')
    
    def get_accuracy(self):
        acc=self['act']['accuracy']
        if self['act']['id']=='Hurricane':
            if self.env.get('Rain'):
                acc=1e5
            elif self.env.get('Sunlight'):
                acc=50
        acc_mult=[1.0,1.33,1.67,2.0]
        if self['boosts']['accuracy']>=0:
            acc*=acc_mult[self['boosts']['accuracy']]
        else:
            acc/=acc_mult[self['boosts']['accuracy']]
        acc*=self.target.get_evasion()
        return acc/100

    def move_1(self): # Fire Blast
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: self.target.set_status('BRN')
    
    def move_2(self): # Hurricane
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('Confusion',counter=0)
