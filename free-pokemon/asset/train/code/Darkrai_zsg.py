from engine import *


class Darkrai(PokemonBase):
    _species='Darkrai'
    _types=['Dark']
    _gender='Male'
    _ability=['Bad Dreams']
    _move_1=('Dark Pulse',80,100,'Special','Dark',0,[])
    _move_2=('Hypnosis',0,60,'Status','Psychic',0,[])
    def __init__(self):
        super().__init__()

    def endturn(self):
        if isinstance(self.target['status'],dict) and self.target['status']=='SLP':
            self.target.take_damage(self.target['max_hp']//8,'loss')

    def move_1(self): # Dark Pulse
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_condition('Flinch',counter=0)

    def move_2(self): # Hypnosis
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            self.target.set_status('SLP')
