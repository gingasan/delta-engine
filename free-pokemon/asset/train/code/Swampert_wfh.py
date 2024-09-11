from engine import *


class Swampert(PokemonBase):
    _species='Swampert'
    _types=['Water','Ground']
    _gender='Female'
    _ability=['Mist Mirage']
    _move_1=('Aqua Jet',40,100,'Physical','Water',1,['contact'])
    _move_2=('Mud Bomb',65,85,'Special','Ground',0,[])
    def __init__(self):
        super().__init__()

    def onswitch(self):
        self.set_env('Mist Mirage',side='self',counter=0,max_count=3)

    def endturn(self):
        if self.get_env('Mist Mirage',side='self'):
            self.restore(self['max_hp']//16,'heal')

    def move_1(self): # Aqua Jet
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if rnd()<30/100:  # 30% chance to increase Speed by 1 stage
                self.set_boost('spe',1,'self')
    
    def move_2(self): # Mud Bomb
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:  # 20% chance to lower target's Accuracy by 1 stage
                self.target.set_boost('accuracy',-1)
