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
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Dragon Claw
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)

# ----------

@Increment(Tyrantrum,'_move_3')
def value():
    return ('Psychic Fangs',85,100,'Physical','Psychic',0,['contact'])

@Increment(Tyrantrum)
def move_3(self): # Psychic Fangs
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
        for t in ['Reflect','Light Screen','Aurora Veil']:
            if self.env.get_side_condition(t,self.target.side_id):
                self.env.remove(t,self.target.side_id)
