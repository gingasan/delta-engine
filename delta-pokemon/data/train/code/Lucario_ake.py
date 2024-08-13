from engine import *


class Lucario(PokemonBase):
    _species='Lucario'
    _types=['Fighting','Steel']
    _gender='Male'
    _ability=['Adaptability']
    _move_1=('Aura Blade',90,100,'Physical','Fighting',0,['contact'])
    _move_2=('Bullet Punch',40,100,'Physical','Steel',1,['contact'])
    def __init__(self):
        super().__init__()

    def get_stab(self):
        stab=1
        if self['act']['type'] in self['types']:
            stab=2
        return stab
    
    def get_crit(self):
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        if self['act']['id']=='Aura Blade':
            crit_ratio=min(3,crit_ratio+1)
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit
    
    def move_1(self): # Aura Blade
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100: 
                self.target.set_condition('FLINCH',counter=0)
    
    def move_2(self): # Bullet Punch
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_boost('def',-1)
