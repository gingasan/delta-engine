from engine import *


class Dodrio(PokemonBase):
    _species='Dodrio'
    _types=['Normal','Flying']
    _gender='Male'
    _ability=['Tangled Feet']
    _move_1=('Drill Peck',80,100,'Physical','Flying',0,['contact'])
    _move_2=('Tri Attack',80,100,'Special','Normal',0,[])
    def __init__(self):
        super().__init__()

    def get_evasion(self):
        if self['status']:
            return 0.5
        return 1

    def move_1(self): # Drill Peck
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)

    def move_2(self): # Tri Attack
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                if rnd()<20/100:self.target.set_status('BRN')
                elif rnd()<40/100:self.target.set_status('PAR')
                elif rnd()<60/100:self.target.set_status('FRZ')

# ----------

@Increment(Dodrio,'_move_3')
def value():
    return ('Jump Kick',100,95,'Physical','Fighting',0,['contact'])

@Increment(Dodrio)
def move_3(self): # Jump Kick
    attack_ret=self.attack()
    if not (attack_ret['miss'] or attack_ret['immune']):
        damage_ret=self.get_damage()
        damage=damage_ret['damage']
        self.target.take_damage(damage)
    else:
        self.take_damage(self['max_hp']//2,'recoil')
