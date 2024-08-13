from engine import *


class Basarios(PokemonBase):
    _species='Basarios'
    _types=['Rock','Fire']
    _gender='Female'
    _ability=['Heat Vent','Lava Storm']
    _move_1=('Lava Beam',100,90,'Special','Fire',0,[])
    _move_2=('Earthquake',100,100,'Physical','Ground',0,[])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        self.register_act_taken()
        if self['act_taken']['type'] in ['Water','Grass']:
            x=int(x*0.5)
        self.state['hp']=max(0,self['hp']-x)
        if self['hp']==0:
            self.state['status']='FNT'

    def move_1(self): # Lava Beam
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100: self.target.set_status('BRN')
    
    def move_2(self): # Earthquake
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Basarios,'_move_3')
def value():
    return ('Poison Cloud',0,100,'Status','Poison',0,[])

@Increment(Basarios)
def move_3(self): # Poison Cloud
    self.target.set_status('PSN')

# -------------------------------------------------------------

@Increment(Basarios,'_move_4')
def value():
    return ('Rock Slide',75,90,'Physical','Rock',0,[])

@Increment(Basarios)
def move_4(self): # Rock Slide
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<30/100:
            self.target.set_condition('FLINCH',counter=0)

# -------------------------------------------------------------

@Increment(Basarios,'_ability')
def value():
    return ['Heat Vent','Lava Storm']

@Increment(Basarios)
def release_gas(self):
    def sleeping_gas():
        if rnd()<1/3:
            self.target.set_status('SLP')
    def poison_gas():
        if rnd()<1/3:
            self.target.set_status('PSN')
    def burning_gas():
        if rnd()<1/3:
            self.target.set_status('BRN')
    rndc([sleeping_gas,poison_gas,burning_gas])()

@Increment(Basarios)
def move_1(self): # Lava Beam
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint() and rnd()<20/100: self.target.set_status('BRN')
        self.release_gas()
