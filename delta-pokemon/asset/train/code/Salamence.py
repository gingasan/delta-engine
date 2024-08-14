from engine import *


class Salamence(PokemonBase):
    _species='Salamence'
    _types=['Dragon','Flying']
    _gender='Female'
    _ability=['Intimidate']
    _move_1=('Dragon Pulse',85,100,'Special','Dragon',0,[])
    _move_2=('Hurricane',110,70,'Special','Flying',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.target.set_boost('atk',-1)

    def get_accuracy(self):
        acc=self['act']['accuracy']
        if self['act']['id']=='Hurricane':
            if self.env.get('RAINDANCE'):
                acc=1e5
            elif self.env.get('SUNNYDAY'):
                acc=50
        acc_mult=[1.0,1.33,1.67,2.0]
        if self['boosts']['accuracy']>=0:
            acc*=acc_mult[self['boosts']['accuracy']]
        else:
            acc/=acc_mult[self['boosts']['accuracy']]
        acc*=self.target.get_evasion()
        return acc/100
    
    def move_1(self): # Dragon Pulse
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Hurricane
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_condition('CONFUSION',counter=0)