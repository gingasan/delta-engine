from engine import *


class Hippowdon(PokemonBase):
    _species='Hippowdon'
    _types=['Ground']
    _gender='Male'
    _ability=['Sand Spit']
    _move_1=('Earth Power',90,100,'Special','Ground',0,[])
    _move_2=('Sludge Wave',95,100,'Special','Poison',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_env('SANDSTORM')

    def _take_damage_attack(self,x):
        self.register_act_taken()
        self.state['hp']=max(0,self['hp']-x)
        if self['hp']==0:
            self.state['status']='FNT'
            return
        self.set_env('SANDSTORM')

    def move_1(self): # Earth Power 
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_boost('spd',-1)

    def move_2(self): # Sludge Wave
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: 
                self.target.set_status('PSN')