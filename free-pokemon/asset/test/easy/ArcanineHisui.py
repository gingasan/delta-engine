from engine import *


class ArcanineHisui(PokemonBase):
    _species='Arcanine-Hisui'
    _types=['Fire','Rock']
    _gender='Male'
    _ability=['Rock Head']
    _move_1=('Head Smash',150,80,'Physical','Rock',0,['contact'])
    _move_2=('Flare Blitz',120,100,'Physical','Fire',0,['contact'])
    def __init__(self):
        super().__init__()

    def move_1(self): # Head Smash
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
    
    def move_2(self): # Flare Blitz
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                if rnd()<10/100: self.target.set_status('BRN')

# ----------

@Increment(ArcanineHisui,'_move_3')
def value():
    return ('Extreme Speed',80,100,'Physical','Normal',2,['contact'])

@Increment(ArcanineHisui)
def move_3(self): # Extreme Speed
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
