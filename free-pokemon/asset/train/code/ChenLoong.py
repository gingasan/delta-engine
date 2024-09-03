from engine import *


class ChenLoong(PokemonBase):
    _species='Chen-Loong'
    _types=['Ice','Water']
    _gender='Female'
    _ability=['Tailwind']
    _move_1=('Blizzard',110,70,'Special','Ice',0,[])
    _move_2=('Hydro Pump',90,100,'Special','Water',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_env('SNOW')
        self.set_side_condition('AURORA_VEIL',counter=0,max_count=5)

    def _take_damage_attack(self,x):
        self.register_act_taken()
        if self['side_conditions'].get('AURORA_VEIL'):
            if self['act_taken']['category']=='Physical' or self['act_taken']['category']=='Special':
                x//=2
        self.state['hp']=max(0,self['hp']-x)
        if self['hp']==0:
            self.state['status']='FNT'

    def get_accuracy(self):
        acc=self['act']['accuracy']
        if self['act']['id']=='Blizzard':
            if self.env.get('SNOW'):
                acc=1e5
        acc_mult=[1.0,1.33,1.67,2.0]
        if self['boosts']['accuracy']>=0:
            acc*=acc_mult[self['boosts']['accuracy']]
        else:
            acc/=acc_mult[self['boosts']['accuracy']]
        acc*=self.target.get_evasion()
        return acc/100

    def move_1(self): # Blizzard
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: self.target.set_status('FRZ')
    
    def move_2(self): # Surf
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            if self.target['conditions'].get('DIVE'):
                damage*=2
            self.target.take_damage(damage)
