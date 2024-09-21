from engine import *


class Spectreon(PokemonBase):
    _species='Spectreon'
    _types=['Ghost','Dark']
    _gender='Male'
    _ability=['Spectral Aura']
    _move_1=('Shadow Ball',80,100,'Special','Ghost',0,[])
    _move_2=('Void Pulse',90,100,'Special','Dark',0,[])
    def __init__(self):
        super().__init__()

    def take_damage_attack(self,x):
        self.register_act_taken()
        if self['boosts']['def']>=0:
            x=int(x*(1-0.1*self['boosts']['def']))
        self._set_hp(-x)        

    def move_1(self): # Shadow Ball
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<20/100:
                self.target.set_boost('spd',-1)

    def move_2(self): # Void Pulse
        attack_ret=self.attack()
        if not (attack_ret['miss'] or attack_ret['immune']):
            damage_ret=self.get_damage()
            damage=damage_ret['damage']
            self.target.take_damage(damage)
            if not self.target.isfaint() and rnd()<30/100:
                self.target.set_boost('atk',-1)
