from engine import *


class Greninja(PokemonBase):
    _species='Greninja'
    _types=['Water','Dark']
    _gender='Male'
    _ability=['Proten']
    _move_1=('Water Shuriken',20,100,'Special','Water',0,[])
    _move_2=('Night Slash',70,100,'Physical','Dark',0,['contact'])
    def __init__(self):
        super().__init__()

    def get_crit(self):
        crit_mult=[0,24,8,2,1]
        crit_ratio=self['boosts']['crit']
        if self['act']['id']=='Night Slash':
            crit_ratio=min(3,crit_ratio+1)
        crit=False
        if rnd()*crit_mult[crit_ratio+1]<1:
            crit=True
        return crit
    
    def move_1(self): # Water Shuriken
        hit=True; i=0
        while hit and i<5:
            self.state['types']=[self['act']['type']]
            damage_ret=self.get_damage()
            if damage_ret['miss']: break
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            i+=1; hit=False if self.target.isfaint() else True
            if i<5 and rnd()<50/100: break

    def move_2(self): # Night Slash
        self.state['types']=[self['act']['type']]
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
