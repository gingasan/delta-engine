from engine import *


class Muk(PokemonBase):
    _species='Muk'
    _types=['Poison']
    _gender='Male'
    _ability=['Stench']
    _move_1=('Sludge Wave',95,100,'Special','Poison',0,[])
    _move_2=('Lunge',80,100,'Physical','Bug',0,['contact'])
    def __init__(self):
        super().__init__()

    def move_1(self): # Sludge Wave
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_status('PSN')
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_condition('Flinch',counter=0)

    def move_2(self): # Lunge
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint():
                self.target.set_boost('atk',-1)
            if not self.target.isfaint() and rnd()<10/100:
                self.target.set_condition('Flinch',counter=0)
