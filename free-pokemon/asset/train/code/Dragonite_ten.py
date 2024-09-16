from engine import *


class Dragonite(PokemonBase):
    _species='Dragonite'
    _types=['Dragon','Flying']
    _gender='Male'
    _ability=['Multiscale']
    _move_1=('Dragon Dance',0,1000000,'Status','Dragon',0,[])
    _move_2=('Aerial Ace',60,1000000,'Physical','Flying',0,[])
    def __init__(self):
        super().__init__()

    def _take_damage_attack(self,x):
        if 'type_effect' in self.target['act'] and self.target['act']['type_effect']<0.1:
            self.logger.log('It is immune by %s.'%self._species)
            return
        self.register_act_taken()
        if self['hp']==self['max_hp']:
            x//=2
        self.state['hp']=max(0,self['hp']-x)
        self.log(script='attack',species=self._species,x=x,**self['act_taken'])

    def move_1(self): # Dragon Dance
        self.set_boost('atk',+1,'self')
        self.set_boost('spe',+1,'self')

    def move_2(self): # Aerial Ace
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Dragonite,'_move_3')
def value():
    return ('Earthquake',100,100,'Physical','Ground',0,[])

@Increment(Dragonite)
def move_3(self): # Earthquake
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
