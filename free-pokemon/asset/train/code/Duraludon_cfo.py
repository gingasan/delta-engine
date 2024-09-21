from engine import *


class Duraludon(PokemonBase):
    _species='Duraludon'
    _types=['Steel','Dragon']
    _gender='Male'
    _ability=['Sniper']
    _move_1=('Flash Cannon',80,100,'Special','Steel',0,[])
    _move_2=('Tri Attack',80,100,'Special','Normal',0,[])
    def __init__(self):
        super().__init__()
    
    def move_1(self): # Flash Cannon
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            if damage_ret['crit']: damage=int(damage*1.5)
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<10/100: self.target.set_boost('spd',-1)
    
    def move_2(self): # Tri Attack
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            if damage_ret['crit']: damage=int(damage*1.5)
            self.target.take_damage(damage)
            if not self.target.isfaint():
                r=rnd()
                if r<20/100: 
                    self.target.set_status('PAR')
                elif r<40/100:
                    self.target.set_status('BRN')
                elif r<60/100:
                    self.target.set_status('FRZ')
