from engine import *


class WeezingGalar(PokemonBase):
    _species='Weezing-Galar'
    _types=['Steel','Poison']
    _gender='Female'
    _ability=['Levitate']
    _move_1=('Strange Steam',90,95,'Special','Fairy',0,[])
    _move_2=('Pain Split',0,100000,'Status','Normal',0,[])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        self.register_act_taken()
        if self['act_taken']['type']=='Ground':
            return
        self.state['hp']=max(0,self['hp']-x)
        if self['hp']==0:
            self.state['status']='FNT'

    def move_1(self): # Strange Steam
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('CONFUSION',counter=0)

    def move_2(self): # Pain Split
        hp=(self['hp']+self.target['hp'])//2
        self.target.state['hp']=hp
        self.state['hp']=hp

# -------------------------------------------------------------

@Increment(WeezingGalar,'_move_3')
def value():
    return ('Will-O-Wisp',0,85,'Status','Fire',0,[])

@Increment(WeezingGalar)
def move_3(self): # Will-O-Wisp
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        self.target.set_status('BRN')
