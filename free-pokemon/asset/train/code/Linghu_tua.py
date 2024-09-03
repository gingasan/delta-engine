from engine import *


class Linghu(PokemonBase):
    _species='Linghu'
    _types=['Grass','Steel']
    _gender='Neutral'
    _ability=['Gourd Resilience']
    _move_1=('Verdant Goad',90,100,'Physical','Grass',0,[])
    _move_2=('Metallic Rampart',0,100,'Status','Steel',0,[])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        self.register_act_taken()
        if self['hp']>self['max_hp']//2:
            x=int(x*0.75)
        self.state['hp']=max(0,self['hp']-x)
        if self['hp']==0:
            self.state['status']='FNT'

    def move_1(self): # Verdant Goad
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('spa',-1)

    def move_2(self): # Metallic Rampart
        self.set_boost('def',+1,'self')
        self.set_boost('spd',+1,'self')
        if self['act_taken'] and self['act_taken']['category']=='Physical':
            self.target.take_damage(int(self['act_taken']['damage']*0.25))

# -------------------------------------------------------------

@Increment(Linghu,'_move_3')
def value():
    return ('Bovine Crush',120,90,'Physical','Steel',0,[])

@Increment(Linghu)
def move_3(self): # Bovine Crush
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100:
            self.target.set_condition('FLINCH',counter=0)

# -------------------------------------------------------------

@Increment(Linghu,'_ability')
def value():
    return ['Gourd Resilience','Enduring Energy']

@Increment(Linghu)
def move_1(self): # Verdant Goad
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_boost('spa',-1)
    if self.env.get('HAIL') or self.env.get('SNOW'):
        self.restore(self['max_hp']//16,'heal')
