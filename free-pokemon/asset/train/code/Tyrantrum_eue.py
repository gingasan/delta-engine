from engine import *


class Tyrantrum(PokemonBase):
    _species='Tyrantrum'
    _types=['Rock','Dragon']
    _gender='Male'
    _ability=['Rock Head']
    _move_1=('Head Smash',150,80,'Physical','Rock',0,['contact'])
    _move_2=('Dragon Claw',80,100,'Physical','Dragon',0,['contact'])
    def __init__(self):
        super().__init__()

    def move_1(self): # Head Smash
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Dragon Claw
        damage_ret=self.get_damage()
        if not damage_ret['miss']:
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# -------------------------------------------------------------

@Increment(Tyrantrum,'_move_3')
def value():
    return ('Psychic Fangs',85,100,'Physical','Psychic',0,['contact'])

@Increment(Tyrantrum)
def move_3(self): # Psychic Fangs
    damage_ret=self.get_damage()
    if not damage_ret['miss']:
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        for t in ['REFLECT','LIGHT_SCREEN','AURORA_VEIL']:
            if self.target['side_conditions'].get(t):
                del self.target['side_conditions'][t]
