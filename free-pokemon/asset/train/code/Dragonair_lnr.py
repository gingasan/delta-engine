from engine import *


class Dragonair(PokemonBase):
    _species='Dragonair'
    _types=['Dragon']
    _gender='Female'
    _ability=['Shed Skin']
    _move_1=('Dragon Claw',80,100,'Physical','Dragon',0,['contact'])
    _move_2=('Aqua Tail',90,90,'Physical','Water',0,['contact'])
    def __init__(self):
        super().__init__()
    
    def endturn(self):
        if rnd()<1/3:
            self.state['status']=None
            self.restore(int(1/8*self['max_hp']),'heal')
    
    def move_1(self): # Dragon Claw
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Aqua Tail
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Dragonair,'_move_3')
def value():
    return ('Fire Fang',65,95,'Physical','Fire',0,['contact','bite'])

@Increment(Dragonair)
def move_3(self): # Fire Fang
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        if not self.target.isfaint():
            if rnd()<10/100:
                self.target.set_condition('FLINCH',counter=0)
            if rnd()<10/100:
                self.target.set_status('BRN')

# ----------

@Increment(Dragonair,'_move_4')
def value():
    return ('Thunder Wave',0,100000,'Status','Electric',0,[])

@Increment(Dragonair)
def move_4(self): # Thunder Wave
    self.target.set_status('PAR')
